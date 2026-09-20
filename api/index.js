const express = require('express');
const path = require('path');
const fs = require('fs');
const mongoose = require('mongoose');
const crypto = require('crypto');
const { SitemapStream, streamToPromise } = require('sitemap');
const rateLimit = require('express-rate-limit');

// Environment variables loading configuration mapping one step back to root directory
if (process.env.NODE_ENV !== 'production') {
    require('dotenv').config({ path: path.join(__dirname, '../.env') });
}

const app = express();

// ======================================================================
// ⚡ 0. PROXY TRUST  (CRITICAL for Render / Vercel)
// ----------------------------------------------------------------------
// Without this, req.ip is the proxy's IP for EVERY visitor, so all users
// share one rate-limit bucket: one spammer would lock out the whole world,
// and a spammer rotating IPs would never be throttled.
// ======================================================================
app.set('trust proxy', 1);

// ======================================================================
// 🛡️ SECURITY & PRE-VALIDATION UTILITIES
// ======================================================================

// ----------------------------------------------------------------------
// HTML ESCAPING — lead data goes straight into an HTML email we read.
// Without this, a submitter can inject markup/links into our own inbox.
// ----------------------------------------------------------------------
function escapeHtml(value) {
    return String(value == null ? '' : value)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

// ----------------------------------------------------------------------
// PHONE VALIDATOR — global-friendly, blocks only obvious fakes.
// ----------------------------------------------------------------------
function isValidGlobalMobile(phone) {
    if (!phone) return false;
    const cleanPhone = String(phone).replace(/\D/g, '');

    // Global E.164 standard: 7 to 15 digits
    if (cleanPhone.length < 7 || cleanPhone.length > 15) return false;

    // All same digit: 0000000000, 1111111111
    if (/^(\d)\1+$/.test(cleanPhone)) return false;

    // Fewer than 4 distinct digits in a 10+ digit number = almost always fake
    if (cleanPhone.length >= 10 && new Set(cleanPhone).size < 4) return false;

    // Sequential runs: 1234567890 / 9876543210
    const asc = '01234567890123456789';
    const desc = '98765432109876543210';
    if (asc.includes(cleanPhone) || desc.includes(cleanPhone)) return false;

    // North-American "555-01xx" reserved fake range (the sample spam used 5550125032)
    if (/^1?555(01\d{2}|\d{4})/.test(cleanPhone) && cleanPhone.length >= 10) return false;

    return true;
}

// ----------------------------------------------------------------------
// HUMAN NAME CHECK — blocks keyboard smash like "Uoiowwd Mhlaurvgl".
//
// DESIGN RULE: a rejected name is a LOST LEAD. So this only hard-rejects
// obvious garbage. Anything merely odd is accepted and tagged `suspicious`
// so you can eyeball it in the sheet instead of never hearing about it.
//
// Indian names carry consonant clusters that naive filters kill
// ("Lakshmi" = k-s-h-m, "Chandrashekhar", "Shubhangi"), so common digraphs
// are stripped before counting consonant runs.
// ----------------------------------------------------------------------
const NAME_DIGRAPHS = /(sh|ch|th|ph|gh|kh|dh|bh|jh|zh|ck|ng|qu|tr|shr|str)/g;

// Keyboard rows — "asdfgh", "qwerty", "zxcvb" are smashes, not names
const KEYBOARD_ROWS = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm', '1234567890'];
const KEYBOARD_RUNS = KEYBOARD_ROWS.flatMap(r => [r, r.split('').reverse().join('')]);

function hasKeyboardRun(word, len = 4) {
    for (let i = 0; i + len <= word.length; i++) {
        const chunk = word.slice(i, i + len);
        if (KEYBOARD_RUNS.some(row => row.includes(chunk))) return true;
    }
    return false;
}

// Strip accents so "Björk" / "José" are analysed as "Bjork" / "Jose"
function deaccent(str) {
    return str.normalize('NFD').replace(/[̀-ͯ]/g, '');
}

function checkHumanName(name) {
    if (!name) return { ok: false, error: 'Please enter your full name.' };

    const cleanName = String(name).trim().replace(/\s+/g, ' ');

    if (cleanName.length < 3 || cleanName.length > 60) {
        return { ok: false, error: 'Please enter a valid full name.' };
    }

    // Any Unicode letter, plus the punctuation real names use.
    // (An ASCII-only rule silently rejects José, Björk, Müller, 田中 …)
    if (!/^\p{L}[\p{L}\p{M}\s.'-]*$/u.test(cleanName)) {
        return { ok: false, error: 'Please enter a valid full name.' };
    }

    const words = cleanName.split(' ').filter(Boolean);
    if (words.length > 6) return { ok: false, error: 'Please enter a valid full name.' };

    let suspicious = false;

    for (const rawWord of words) {
        const word = deaccent(rawWord).replace(/[^a-zA-Z]/g, '').toLowerCase();
        // Non-Latin scripts (Devanagari, CJK, Arabic …) skip the Latin heuristics
        if (!word) continue;

        // Keyboard smash: "asdfgh", "qwerty", "lkjhg"
        if (hasKeyboardRun(word)) {
            return { ok: false, error: 'Please enter a valid full name.' };
        }

        // Same letter 3+ times in a row — "aaargh", "wwwd"
        if (/(.)\1{2,}/.test(word)) {
            return { ok: false, error: 'Please enter a valid full name.' };
        }

        // Consonant runs, measured AFTER removing legitimate digraphs
        const stripped = word.replace(NAME_DIGRAPHS, '');
        if (/[bcdfghjklmnpqrstvwxz]{4,}/.test(stripped)) {
            return { ok: false, error: 'Please enter a valid full name.' };
        }
        // A 3-run in the stripped form is unusual but not impossible — flag it
        if (/[bcdfghjklmnpqrstvwxz]{3,}/.test(stripped)) {
            suspicious = true;
        }

        if (word.length >= 5) {
            const vowels = (word.match(/[aeiouy]/g) || []).length;
            // No vowel at all in a long word, or 4+ vowels jammed together ("uoio")
            if (vowels === 0 || /[aeiou]{4,}/.test(word)) {
                return { ok: false, error: 'Please enter a valid full name.' };
            }
            if (vowels / word.length > 0.75) suspicious = true;
        }
    }

    return { ok: true, name: cleanName, suspicious };
}

// ----------------------------------------------------------------------
// EMAIL VALIDATION — POLICY CHANGE
// We no longer BLOCK personal emails. Real decision-makers (especially in
// India) send the first enquiry from Gmail; blocking them threw away real
// leads to stop spam that OTP verification stops anyway.
// We now: (a) reject malformed + disposable addresses,
//         (b) CLASSIFY the rest as 'corporate' or 'personal' so you can
//             prioritise in the sheet without ever losing a lead.
// ----------------------------------------------------------------------
const PUBLIC_EMAIL_DOMAINS = new Set([
    'gmail.com', 'googlemail.com', 'yahoo.com', 'yahoo.co.in', 'yahoo.in',
    'hotmail.com', 'outlook.com', 'live.com', 'msn.com', 'icloud.com',
    'me.com', 'aol.com', 'rediffmail.com', 'protonmail.com', 'proton.me',
    'gmx.com', 'mail.com', 'yandex.com'
]);

const DISPOSABLE_EMAIL_DOMAINS = new Set([
    'tempmail.com', 'temp-mail.org', '10minutemail.com', 'guerrillamail.com',
    'mailinator.com', 'yopmail.com', 'trashmail.com', 'throwawaymail.com',
    'sharklasers.com', 'getnada.com', 'dispostable.com', 'maildrop.cc',
    'fakeinbox.com', 'tempinbox.com', 'mohmal.com', 'emailondeck.com'
]);

function classifyEmail(email) {
    if (!email || typeof email !== 'string') {
        return { ok: false, error: 'Please enter a valid email address.' };
    }

    const value = email.trim().toLowerCase();

    // Basic RFC-ish shape check
    if (!/^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i.test(value)) {
        return { ok: false, error: 'Please enter a valid email address.' };
    }

    const [localPart, domain] = value.split('@');

    if (DISPOSABLE_EMAIL_DOMAINS.has(domain)) {
        return { ok: false, error: 'Temporary/disposable email addresses are not accepted. Please use a permanent address.' };
    }

    // Gmail dot-alias abuse: "owi.w.il.i.m.7.7@gmail.com" style throwaway aliasing
    const dotCount = (localPart.match(/\./g) || []).length;
    if (dotCount > 3) {
        return { ok: false, error: 'Please enter your email address without extra dots.' };
    }

    // Random-string local parts: no vowels at all in a long local part
    const letters = localPart.replace(/[^a-z]/g, '');
    if (letters.length >= 8 && !/[aeiou]/.test(letters)) {
        return { ok: false, error: 'Please enter a valid email address.' };
    }

    return {
        ok: true,
        email: value,
        type: PUBLIC_EMAIL_DOMAINS.has(domain) ? 'personal' : 'corporate'
    };
}

// ----------------------------------------------------------------------
// BOT TRAPS — invisible to humans, deadly to scripted form-fillers.
//
// FRONTEND (add to every form):
//   <input type="text" name="website" tabindex="-1" autocomplete="off"
//          style="position:absolute;left:-9999px;opacity:0;height:0;width:0"
//          aria-hidden="true">
//   <input type="hidden" name="formLoadedAt" value="">   <!-- set to Date.now() on page load -->
//
//   <script>document.querySelector('[name=formLoadedAt]').value = Date.now();</script>
//
// A human never sees or fills `website`. A bot fills every field it finds.
// A human never submits a form within 3 seconds of it loading. A bot does.
// ----------------------------------------------------------------------
const MIN_HUMAN_FILL_MS = 3000;

function detectBot(body) {
    // 1. Honeypot
    if (body.website || body.url || body.fax) {
        return 'honeypot';
    }
    // 2. Submission speed
    const loadedAt = Number(body.formLoadedAt);
    if (loadedAt && Number.isFinite(loadedAt)) {
        const elapsed = Date.now() - loadedAt;
        if (elapsed >= 0 && elapsed < MIN_HUMAN_FILL_MS) return 'too-fast';
    }
    return null;
}

// ----------------------------------------------------------------------
// RATE LIMITERS — per IP. Previously `express-rate-limit` was installed
// but never applied, so /api/chat (which costs money per call) and
// /api/contact were both wide open to scripted abuse.
// ----------------------------------------------------------------------
const limiterOptions = {
    standardHeaders: true,
    legacyHeaders: false,
};

const otpLimiter = rateLimit({
    ...limiterOptions,
    windowMs: 15 * 60 * 1000,
    max: 3,
    message: { success: false, error: 'Too many requests from this IP. Please try again after 15 minutes.' },
});

const verifyLimiter = rateLimit({
    ...limiterOptions,
    windowMs: 15 * 60 * 1000,
    max: 10, // a 4-digit OTP is only 10,000 guesses — this must be capped
    message: { success: false, error: 'Too many verification attempts. Please request a new code.' },
});

const contactLimiter = rateLimit({
    ...limiterOptions,
    windowMs: 15 * 60 * 1000,
    max: 8, // headroom so a real person who mistypes a few times isn't locked out
    message: { success: false, error: 'Too many submissions from this IP. Please try again later.' },
});

const chatLimiter = rateLimit({
    ...limiterOptions,
    windowMs: 10 * 60 * 1000,
    max: 25, // every call costs Groq credits — cap it
    message: { error: 'Chat rate limit reached. Please try again in a few minutes.' },
});

// ⚡ 1. GLOBAL PAYLOAD PARSERS  (size-capped so a huge body can't stall the server)
app.use(express.json({ limit: '64kb' }));
app.use(express.urlencoded({ extended: true, limit: '64kb' }));

// ⚡ 2. EXPLICIT STATIC DIRECTORIES BYPASS
app.use(express.static(path.join(__dirname, '../public')));
app.use('/images', express.static(path.join(__dirname, '../public/images')));

// ======================================================================
// DATABASE SCHEMA & MODEL SETUP
// Extra fields so you can triage leads instead of blocking them.
// ======================================================================
const contactSchema = new mongoose.Schema({
    name:      { type: String, required: true, trim: true },
    email:     { type: String, required: true, trim: true, lowercase: true },
    phone:     { type: String, required: true, trim: true },
    company:   { type: String, trim: true, default: '' },
    reason:    { type: String, required: true, trim: true },
    emailType: { type: String, enum: ['corporate', 'personal'], default: 'personal' },
    source:    { type: String, default: 'contact-form' },
    flagged:   { type: Boolean, default: false },   // odd-looking, worth a human glance
    verified:  { type: Boolean, default: false },
    ip:        { type: String, default: '' },
    createdAt: { type: Date, default: Date.now }
}, { bufferCommands: true });

const Contact = mongoose.models.Contact || mongoose.model('Contact', contactSchema);

if (process.env.MONGO_URI) {
    mongoose.connect(process.env.MONGO_URI, { serverSelectionTimeoutMS: 8000 })
    .then(() => console.log('🚀 Operational Pipeline: MongoDB Atlas Handshake Secured.'))
    .catch(err => console.error('❌ Pipeline Fault:', err));
}

// ======================================================================
// ⚡ IN-MEMORY OTP STORE (Expires in 10 Mins)
// NOTE: in-memory means OTPs are lost whenever the process restarts.
// Fine on a single always-on Render instance. On Vercel/serverless (multiple
// cold-started instances) send-otp and verify-otp can land on DIFFERENT
// instances and verification will fail — move this to MongoDB if you deploy
// there. A periodic sweep keeps this map from growing forever.
// ======================================================================
const otpStore = new Map();

setInterval(() => {
    const now = Date.now();
    for (const [key, record] of otpStore) {
        if (now > record.expiresAt) otpStore.delete(key);
    }
}, 5 * 60 * 1000).unref?.();

// Constant-time OTP comparison so response timing can't leak the code
function safeCompare(a, b) {
    const bufA = Buffer.from(String(a));
    const bufB = Buffer.from(String(b));
    if (bufA.length !== bufB.length) return false;
    return crypto.timingSafeEqual(bufA, bufB);
}

// ⚡ HELPER FUNCTION: SERVERLESS TIMEOUT PROTECTION (6 SECONDS MAX)
const fetchWithTimeout = async (url, options, timeout = 6000) => {
    const controller = new AbortController();
    const id = setTimeout(() => controller.abort(), timeout);
    try {
        const response = await fetch(url, { ...options, signal: controller.signal });
        clearTimeout(id);
        return response;
    } catch (err) {
        clearTimeout(id);
        throw err;
    }
};

// Fire-and-forget push to the Google Sheet, with the lead-quality columns
function pushToSheet(payload) {
    const sheetWebhook = process.env.GOOGLE_SHEET_WEBHOOK_URL;
    if (!sheetWebhook) return;
    fetchWithTimeout(sheetWebhook, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(() => console.log('✅ [Google Sheet Success]: Lead Row Inserted!'))
    .catch(err => console.error('⚠️ [Google Sheet Error]:', err.message));
}

// ======================================================================
// ✉️ AUTO-ACKNOWLEDGEMENT TO THE ENQUIRER
// ----------------------------------------------------------------------
// Sent from our own domain the moment a valid enquiry lands, so the person
// knows it reached a human and roughly when to expect a reply.
//
// ⚠️ ABUSE GUARD — READ BEFORE CHANGING:
// This mails an address that a stranger typed into a public form. Without a
// cooldown, someone can put a victim's address in and hammer submit, and
// every one of those mails leaves *our* domain — which gets vakratronsys.com
// reported as a spam source and wrecks deliverability for real mail.
// One acknowledgement per address per 30 minutes, regardless of IP.
// ======================================================================
// ----------------------------------------------------------------------
// MAIL ADDRESSING
//
// Sending goes through Resend; the mailbox itself lives on Zoho. These do
// not fight each other: Resend's records sit on the `send` subdomain
// (`send` MX + SPF) and `resend._domainkey`, so the ROOT MX and ROOT SPF
// stay entirely Zoho's. Because the domain is already verified in Resend,
// switching the From address is a config change, not a DNS change.
// (Never enable Resend "Inbound" on this domain — that one *does* claim the
// root MX and would break Zoho delivery.)
//
// NOTIFY_TO is a list on purpose. Zoho's free plan has no forwarding and no
// aliases, so a lead sent only to connect@ sits in a mailbox that has to be
// opened separately. Copying Gmail means nothing waits unseen.
// ----------------------------------------------------------------------
const FROM_ADDRESS = process.env.MAIL_FROM || 'Vakratron Systems <connect@vakratronsys.com>';
const REPLY_TO = process.env.MAIL_REPLY_TO || 'connect@vakratronsys.com';
const NOTIFY_TO = (process.env.MAIL_NOTIFY_TO || 'connect@vakratronsys.com,vakratronsystems@gmail.com')
    .split(',')
    .map(a => a.trim())
    .filter(Boolean);

const WELCOME_COOLDOWN_MS = 30 * 60 * 1000;
const welcomeSentAt = new Map();

setInterval(() => {
    const now = Date.now();
    for (const [addr, at] of welcomeSentAt) {
        if (now - at > WELCOME_COOLDOWN_MS) welcomeSentAt.delete(addr);
    }
}, 10 * 60 * 1000).unref?.();

// Turn "Consultation request — /tec_blueprint/blueprint-disaster-recovery"
// into "Disaster Recovery Blueprints" so the mail sounds like a person who
// actually saw what they were reading.
const TOPIC_MAP = [
    ['/gpu_ai_cluster/',        'AI & GPU cluster infrastructure'],
    ['/ai_agent/',              'agentic AI systems'],
    ['/ent_llm/',               'enterprise LLM deployment'],
    ['/cloud_model/',           'cloud deployment models'],
    ['/dc-dr/',                 'data centre & disaster recovery'],
    ['/tec_blueprint/',         'architecture blueprints'],
    ['/platform_engineering/',  'platform engineering'],
    ['/api_services/',          'API & integration services'],
    ['/sta/',                   'technology assessment'],
];

function topicFromReason(reason) {
    const r = String(reason || '').toLowerCase();
    for (const [needle, label] of TOPIC_MAP) {
        if (r.includes(needle)) return label;
    }
    return null;
}

function sendWelcomeEmail({ name, email, reason }) {
    const apiKey = process.env.RESEND_OTP_API_KEY || process.env.RESEND_API_KEY;
    if (!apiKey) return;

    const now = Date.now();
    const last = welcomeSentAt.get(email);
    if (last && now - last < WELCOME_COOLDOWN_MS) {
        console.log(`⏭️  Welcome mail skipped (cooldown) for ${email}`);
        return;
    }
    welcomeSentAt.set(email, now);

    const firstName = String(name).trim().split(' ')[0];
    const topic = topicFromReason(reason);
    const topicLine = topic
        ? `We can see you were looking at our ${escapeHtml(topic)} material.`
        : '';

    fetchWithTimeout('https://api.resend.com/emails', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${apiKey}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({
            from: FROM_ADDRESS,
            to: [email],
            reply_to: REPLY_TO,
            subject: 'We received your enquiry — Vakratron Systems',
            html: `
                <div style="font-family: Arial, Helvetica, sans-serif; background:#0f172a; color:#e8edf5; padding:30px; border-radius:12px; max-width:560px; margin:0 auto; line-height:1.6;">
                    <h2 style="color:#38bdf8; margin:0 0 4px 0; font-size:1.25rem;">Vakratron Systems</h2>
                    <p style="color:#64748b; font-size:0.78rem; margin:0 0 22px 0; letter-spacing:0.06em; text-transform:uppercase;">Solutions Architecture &amp; Infrastructure Advisory</p>

                    <p style="margin:0 0 14px 0;">Hi <b>${escapeHtml(firstName)}</b>,</p>

                    <p style="margin:0 0 14px 0;">
                        Thanks for reaching out. Your enquiry has reached us and one of our
                        solutions architects will get back to you within one business day.
                        ${topicLine}
                    </p>

                    <p style="margin:0 0 14px 0;">
                        To make that first reply useful, it helps if you can share a little
                        about your environment — current scale, what you are trying to move or
                        build, and any timeline or compliance constraints you are working with.
                        Just reply to this email; it comes straight to us.
                    </p>

                    <div style="background:#1e293b; border-left:3px solid #C2185B; padding:14px 16px; margin:22px 0; border-radius:4px;">
                        <p style="margin:0 0 6px 0; font-size:0.86rem; color:#cbd5e1;"><b>What we do</b></p>
                        <p style="margin:0; font-size:0.86rem; color:#94a3b8;">
                            AI &amp; GPU cluster infrastructure · hybrid and multi-cloud architecture ·
                            disaster recovery design · tender documentation (BoQ / BoM) support.
                        </p>
                        <p style="margin:10px 0 0 0; font-size:0.86rem; color:#94a3b8;">
                            AWS Partner · HPE Silver Partner · Sophos Silver Partner
                        </p>
                    </div>

                    <p style="margin:0 0 4px 0;">Best regards,</p>
                    <p style="margin:0 0 22px 0;"><b style="color:#f8fafc;">Enterprise Architecture Team</b><br>
                    <span style="color:#94a3b8; font-size:0.88rem;">Vakratron Systems LLP · New Delhi</span></p>

                    <hr style="border:0; border-top:1px solid rgba(255,255,255,0.08); margin:0 0 12px 0;">
                    <p style="margin:0; font-size:0.76rem; color:#64748b;">
                        You are receiving this because this address was submitted on
                        <a href="https://vakratronsys.com" style="color:#38bdf8; text-decoration:none;">vakratronsys.com</a>.
                        If that wasn't you, please ignore this email — we won't write again.
                    </p>
                </div>
            `
        })
    })
    .then(() => console.log(`✉️  Welcome mail sent to ${email}`))
    .catch(err => {
        console.error('⚠️ Welcome mail failed:', err.message);
        // Let them try again rather than locking the address out on our error
        welcomeSentAt.delete(email);
    });
}

// ======================================================================
// ⚡ 3. SITEMAP
// FIX: lastmod was `new Date()` on every request, telling Google every page
// changed today, every day. That is a low-trust signal. Now it uses the
// file's real modification time.
// ======================================================================
app.get('/sitemap.xml', async (req, res) => {
    try {
        const smStream = new SitemapStream({ hostname: 'https://vakratronsys.com' });
        const pages = new Map();
        const baseDir = process.env.VERCEL ? process.cwd() : path.join(__dirname, '..');

        function scan(folder) {
            if (!fs.existsSync(folder)) return;
            const files = fs.readdirSync(folder);
            files.forEach(file => {
                if (file === 'header.html' || file === 'footer.html' || file === '404.html') return;
                const full = path.join(folder, file);
                const stat = fs.statSync(full);
                if (stat.isDirectory()) {
                    scan(full);
                } else if (file.endsWith('.html')) {
                    let url = full
                        .replace(path.join(baseDir, 'views'), '')
                        .replace(path.join(baseDir, 'public'), '')
                        .replace(/\\/g, '/');
                    if (url.endsWith('/index.html')) url = url.replace('/index.html', '/');
                    url = url.replace('.html', '');
                    if (url === '/index') url = '/';
                    if (!pages.has(url)) pages.set(url, stat.mtime);
                }
            });
        }

        scan(path.join(baseDir, 'views'));
        scan(path.join(baseDir, 'public'));

        pages.forEach((lastmod, p) => {
            smStream.write({
                url: p,
                lastmod: lastmod,
                changefreq: p === '/' ? 'daily' : 'weekly',
                priority: p === '/' ? 1.0 : 0.8
            });
        });

        smStream.end();
        const sitemap = await streamToPromise(smStream);
        res.header('Content-Type', 'application/xml');
        res.send(sitemap.toString());
    } catch (sitemapError) {
        console.error('❌ Sitemap Stream Fault:', sitemapError.message);
        res.status(500).send('Sitemap generation error');
    }
});

app.get('/robots.txt', (req, res) => {
    res.type('text/plain');
    res.send(`User-agent: *\nAllow: /\n\nSitemap: https://vakratronsys.com/sitemap.xml`);
});

// ======================================================================
// ⚡ 4. CONTACT FORM SUBMISSION ENDPOINT
// ======================================================================
app.post('/api/contact', contactLimiter, async (req, res) => {
    try {
        const { name, email, phone, reason, company } = req.body;

        // 🛡️ Bot traps first — silently accept so the bot never learns why it failed
        const botSignal = detectBot(req.body);
        if (botSignal) {
            console.log(`🤖 Bot submission blocked (${botSignal}) from ${req.ip}`);
            return res.status(200).json({ success: true });
        }

        const nameCheck = checkHumanName(name);
        if (!nameCheck.ok) {
            return res.status(400).json({ success: false, error: nameCheck.error });
        }
        if (!isValidGlobalMobile(phone)) {
            return res.status(400).json({ success: false, error: 'Please enter a valid phone number with country code.' });
        }

        const emailCheck = classifyEmail(email);
        if (!emailCheck.ok) {
            return res.status(400).json({ success: false, error: emailCheck.error });
        }

        if (!reason || !String(reason).trim()) {
            return res.status(400).json({ success: false, error: 'Please tell us what you need.' });
        }

        console.log(`📥 Lead received: ${nameCheck.name} (${emailCheck.type}${nameCheck.suspicious ? ', flagged' : ''})`);

        // NEVER let a database problem lose a lead. If Mongo is down or slow,
        // we log it and still fire the sheet push + the notification email —
        // an enquiry sitting in your inbox is worth more than a clean stack trace.
        try {
            await new Contact({
                name: nameCheck.name,
                email: emailCheck.email,
                phone: String(phone).trim(),
                company: company ? String(company).trim() : '',
                reason: String(reason).trim(),
                emailType: emailCheck.type,
                source: 'contact-form',
                flagged: nameCheck.suspicious,
                verified: false,
                ip: req.ip
            }).save();
        } catch (dbErr) {
            console.error('⚠️ DB save failed, continuing with sheet + email:', dbErr.message);
        }

        pushToSheet({
            name: nameCheck.name,
            email: emailCheck.email,
            phone: String(phone).trim(),
            company: company ? String(company).trim() : 'Direct Contact Form',
            pageRequested: String(reason).trim() || 'Contact Us Page',
            emailType: emailCheck.type,
            flagged: nameCheck.suspicious ? 'REVIEW' : '',
            verified: 'No',
            source: 'contact-form',
            submittedAt: new Date().toISOString()
        });

        res.status(200).json({ success: true });

        // Email Dispatch (after responding — the user never waits on it)
        setImmediate(async () => {
            const apiKey = process.env.RESEND_OTP_API_KEY || process.env.RESEND_API_KEY;
            if (!apiKey) return;

            // 1. Acknowledgement to the enquirer, from our own domain.
            //    Runs only for submissions that already cleared every bot trap
            //    and validator above — a blocked bot never reaches this line.
            sendWelcomeEmail({
                name: nameCheck.name,
                email: emailCheck.email,
                reason: String(reason).trim()
            });

            // 2. Notification to us
            const badge = emailCheck.type === 'corporate'
                ? '<span style="background:#065f46;color:#d1fae5;padding:3px 10px;border-radius:99px;font-size:0.75rem;">CORPORATE EMAIL</span>'
                : '<span style="background:#78350f;color:#fef3c7;padding:3px 10px;border-radius:99px;font-size:0.75rem;">PERSONAL EMAIL</span>';

            try {
                await fetchWithTimeout('https://api.resend.com/emails', {
                    method: 'POST',
                    headers: { 'Authorization': `Bearer ${apiKey}`, 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        from: FROM_ADDRESS,
                        to: NOTIFY_TO,
                        reply_to: emailCheck.email,
                        subject: `🚨 New Enquiry: ${nameCheck.name} — ${topicFromReason(reason) || String(reason).trim()}`,
                        html: `
                            <div style="font-family: Arial, sans-serif; padding: 20px; background: #0f172a; color: #fff; border-radius: 8px;">
                                <h2 style="color: #38bdf8;">⚡ Inbound Lead</h2>
                                <p style="margin:0 0 14px 0;">${badge}</p>
                                <hr style="border-color: rgba(255,255,255,0.1);" />
                                <p><strong>Name:</strong> ${escapeHtml(name)}</p>
                                <p><strong>Email:</strong> ${escapeHtml(emailCheck.email)}</p>
                                <p><strong>Phone:</strong> ${escapeHtml(phone)}</p>
                                <p><strong>Company:</strong> ${escapeHtml(company || 'Not provided')}</p>
                                <p><strong>Interested in:</strong> <span style="color: #f43f5e; font-weight: bold;">${escapeHtml(reason)}</span></p>
                            </div>
                        `
                    })
                });
            } catch (mailError) {
                console.error('❌ Resend HTTP Network Fault:', mailError.message);
            }
        });

    } catch (error) {
        console.error('❌ Runtime Ingestion Defect:', error);
        if (!res.headersSent) {
            return res.status(500).json({ success: false, error: 'Something went wrong. Please try again.' });
        }
    }
});

// ======================================================================
// ⚡ 4.1. OTP ENDPOINTS
// Kept for the downloadable/premium resources — NOT for gating page content.
// OTP is the real anti-spam wall: a bot cannot read the inbox, so a fake
// address never completes verification. That is exactly why we no longer
// need to block Gmail addresses outright.
// ======================================================================
app.post('/api/send-otp', otpLimiter, async (req, res) => {
    try {
        const { name, email, phone, company, pageRequested } = req.body;

        const botSignal = detectBot(req.body);
        if (botSignal) {
            console.log(`🤖 Bot OTP request blocked (${botSignal}) from ${req.ip}`);
            return res.status(200).json({ success: true, message: 'OTP sent successfully.' });
        }

        const nameCheck = checkHumanName(name);
        if (!nameCheck.ok) {
            return res.status(400).json({ success: false, error: nameCheck.error });
        }

        const emailCheck = classifyEmail(email);
        if (!emailCheck.ok) {
            return res.status(400).json({ success: false, error: emailCheck.error });
        }

        if (!isValidGlobalMobile(phone)) {
            return res.status(400).json({
                success: false,
                error: 'Please enter a valid phone number with country code (e.g. +91 9876543210).'
            });
        }

        // 6 digits, cryptographically random — 4 digits was only 10,000 guesses
        const generatedOtp = String(crypto.randomInt(100000, 1000000));

        otpStore.set(emailCheck.email, {
            otp: generatedOtp,
            name: nameCheck.name,
            phone: String(phone).trim(),
            company: company ? String(company).trim() : '',
            pageRequested: pageRequested ? String(pageRequested).trim() : '',
            emailType: emailCheck.type,
            flagged: nameCheck.suspicious,
            attempts: 0,
            expiresAt: Date.now() + 10 * 60 * 1000
        });

        pushToSheet({
            name: nameCheck.name,
            email: emailCheck.email,
            phone: String(phone).trim(),
            company: company ? String(company).trim() : '',
            pageRequested: pageRequested ? String(pageRequested).trim() : '',
            emailType: emailCheck.type,
            flagged: nameCheck.suspicious ? 'REVIEW' : '',
            verified: 'No',
            source: 'resource-request',
            submittedAt: new Date().toISOString()
        });

        const apiKey = process.env.RESEND_OTP_API_KEY || process.env.RESEND_API_KEY;
        if (!apiKey) {
            return res.status(500).json({ success: false, error: 'Server email key missing.' });
        }

        await fetchWithTimeout('https://api.resend.com/emails', {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${apiKey}`, 'Content-Type': 'application/json' },
            body: JSON.stringify({
                from: FROM_ADDRESS,
                to: [emailCheck.email],
                bcc: NOTIFY_TO,
                subject: `🔑 Access Code: ${generatedOtp} - Vakratron Systems`,
                html: `
                    <div style="font-family: Arial, sans-serif; background: #0f172a; color: #ffffff; padding: 24px; border-radius: 12px; max-width: 500px; margin: 0 auto;">
                        <h2 style="color: #38bdf8; margin-top: 0;">Vakratron Systems</h2>
                        <p>Hello <b>${escapeHtml(name)}</b>,</p>
                        <p>Use the following code to verify your access to the requested resource:</p>
                        <div style="text-align: center; margin: 24px 0;">
                            <span style="background: #020617; border: 1px solid #C2185B; padding: 12px 24px; font-size: 2rem; font-weight: bold; letter-spacing: 8px; color: #C2185B; border-radius: 8px; display: inline-block;">${generatedOtp}</span>
                        </div>
                        <p style="color: #94a3b8; font-size: 0.8rem;">This code is valid for 10 minutes. If you didn't request it, you can ignore this email.</p>
                        <div style="margin-top: 30px; padding-top: 15px; border-top: 1px dashed rgba(255,255,255,0.2); font-size: 0.78rem; color: #64748b;">
                            <span>${escapeHtml(name)} | ${escapeHtml(phone)} | ${escapeHtml(company || 'N/A')} | ${escapeHtml(pageRequested || 'N/A')}</span>
                        </div>
                    </div>
                `
            })
        });

        res.status(200).json({ success: true, message: 'OTP sent successfully.' });

    } catch (err) {
        console.error('❌ Send OTP Error:', err);
        res.status(500).json({ success: false, error: 'Email delivery failed or timed out.' });
    }
});

app.post('/api/verify-otp', verifyLimiter, async (req, res) => {
    try {
        const { email, otpCode } = req.body;
        if (!email || !otpCode) {
            return res.json({ success: false, error: 'Missing email or code.' });
        }

        const key = String(email).trim().toLowerCase();
        const record = otpStore.get(key);

        if (!record) return res.json({ success: false, error: 'No OTP request found. Please request a new code.' });

        if (Date.now() > record.expiresAt) {
            otpStore.delete(key);
            return res.json({ success: false, error: 'OTP expired. Please request a new code.' });
        }

        // Per-code attempt cap on top of the IP limiter
        record.attempts += 1;
        if (record.attempts > 5) {
            otpStore.delete(key);
            return res.json({ success: false, error: 'Too many incorrect attempts. Please request a new code.' });
        }

        if (!safeCompare(record.otp, String(otpCode).trim())) {
            return res.json({ success: false, error: 'Invalid OTP code.' });
        }

        const leadData = { ...record };
        otpStore.delete(key);

        // Verified lead — persist it so it is never lost, and mark it verified
        try {
            await Contact.findOneAndUpdate(
                { email: key },
                {
                    $set: {
                        name: leadData.name,
                        phone: leadData.phone,
                        company: leadData.company,
                        reason: leadData.pageRequested || 'Resource request',
                        emailType: leadData.emailType,
                        source: 'resource-request',
                        flagged: !!leadData.flagged,
                        verified: true,
                        ip: req.ip
                    },
                    $setOnInsert: { email: key, createdAt: new Date() }
                },
                { upsert: true, new: true }
            );
        } catch (dbErr) {
            console.error('⚠️ Verified lead save error:', dbErr.message);
        }

        pushToSheet({
            name: leadData.name,
            email: key,
            phone: leadData.phone,
            company: leadData.company,
            pageRequested: leadData.pageRequested,
            emailType: leadData.emailType,
            flagged: leadData.flagged ? 'REVIEW' : '',
            verified: 'YES',
            source: 'resource-request',
            submittedAt: new Date().toISOString()
        });

        const apiKey = process.env.RESEND_OTP_API_KEY || process.env.RESEND_API_KEY;
        if (apiKey) {
            fetchWithTimeout('https://api.resend.com/emails', {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${apiKey}`, 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    from: FROM_ADDRESS,
                    to: [key],
                    reply_to: REPLY_TO,
                    subject: `📄 Access Unlocked: ${escapeHtml(leadData.pageRequested || 'Architecture Blueprint')} - Vakratron Systems`,
                    html: `
                        <div style="font-family: Arial, sans-serif; background: #0f172a; color: #ffffff; padding: 28px; border-radius: 12px; max-width: 550px; margin: 0 auto;">
                            <h2 style="color: #38bdf8; margin-top: 0;">Vakratron Systems</h2>
                            <p style="font-size: 1.05rem;">Dear <b>${escapeHtml(leadData.name || 'Valued Client')}</b>,</p>
                            <p>Thank you for verifying your email. You now have full access to:</p>
                            <div style="background: #1e293b; border-left: 4px solid #38bdf8; padding: 16px; margin: 20px 0; border-radius: 4px;">
                                <h4 style="margin: 0 0 6px 0; color: #f8fafc;">${escapeHtml(leadData.pageRequested || 'Deep-Tech Solution Blueprint')}</h4>
                                <p style="margin: 0; color: #94a3b8; font-size: 0.85rem;">Status: <b>Unlocked &amp; Verified</b></p>
                            </div>
                            <p>If you'd like to discuss deployment or workload sizing with our Principal Solutions Architect, just reply to this email or visit <a href="https://vakratronsys.com" style="color: #38bdf8; text-decoration: none;">vakratronsys.com</a>.</p>
                            <hr style="border: 0; border-top: 1px solid rgba(255,255,255,0.1); margin: 24px 0;" />
                            <p style="color: #64748b; font-size: 0.8rem; margin: 0;">Best Regards,<br><strong style="color: #cbd5e1;">Enterprise Architecture Team</strong><br>Vakratron Systems</p>
                        </div>
                    `
                })
            }).catch(err => console.error('⚠️ Confirmation Email Error:', err.message));
        }

        return res.json({ success: true, message: 'Verification successful!' });

    } catch (err) {
        console.error('❌ Verify OTP Error:', err);
        res.status(500).json({ success: false, error: 'Verification server error.' });
    }
});

// ======================================================================
// ⚡ 5. AI INTERACTION GATEWAY
// ======================================================================
app.post('/api/chat', chatLimiter, async (req, res) => {
    try {
        const { message } = req.body;
        if (!message || typeof message !== 'string' || !message.trim()) {
            return res.status(400).json({ error: 'Missing message.' });
        }
        // Cap input length — long prompts cost more and are a common abuse vector
        if (message.length > 2000) {
            return res.status(400).json({ error: 'Message too long. Please keep it under 2000 characters.' });
        }

        const apiKey = process.env.GROQ_API_KEY;
        if (!apiKey) return res.status(500).json({ error: 'Chat service is not configured.' });

        const systemDirectives = `You are Vakra-Bot, a Principal Cloud & AI Infrastructure Architect at Vakratron Systems. You talk like a real human peer and senior solution architect—NOT an automated template engine or robotic bot.

======================================================================
1. WARM WELCOME & OPTIONAL NAME ONBOARDING
======================================================================
- If a user first greets you (e.g. "hi", "hello"), greet them warmly in 1-2 lines and optionally ask for their name in a frictionless way.

======================================================================
2. HUMAN CONVERSATIONAL DIALOGUE (NO ROBOTIC TEMPLATES)
======================================================================
- TALK LIKE A REAL PERSON: Speak in a natural, professional tone. Keep responses short (3-5 sentences max).

======================================================================
3. PROGRESSIVE LEAD CAPTURE AT HIGH VALUE
======================================================================
- ONLY AFTER discussing their environment, offer a formal deliverable (HLD, BOQ Sizing). Ask for Company Name, Email, and Phone ONLY when requested.
- Accept whatever email the person offers, including personal addresses. Never tell a prospect their email is unacceptable.

======================================================================
4. HONESTY
======================================================================
- Never invent client names, case studies, certifications, or project references. If you do not know something, say so and offer to connect them with the team.`;

        const groqRawFetch = await fetchWithTimeout('https://api.groq.com/openai/v1/chat/completions', {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${apiKey}`, 'Content-Type': 'application/json' },
            body: JSON.stringify({
                model: 'openai/gpt-oss-120b',
                messages: [
                    { role: 'system', content: systemDirectives },
                    { role: 'user', content: message }
                ],
                temperature: 0.3,
                max_tokens: 1024
            })
        }, 10000);

        const rawDataBlock = await groqRawFetch.json();

        if (rawDataBlock.choices && rawDataBlock.choices[0]) {
            return res.status(200).json({ response: rawDataBlock.choices[0].message.content });
        }
        console.error('❌ Groq unexpected response:', JSON.stringify(rawDataBlock).slice(0, 500));
        return res.status(502).json({ error: 'The assistant is unavailable right now. Please try again shortly.' });

    } catch (error) {
        console.error('💥 Chat gateway error:', error.message);
        return res.status(500).json({ error: 'The assistant is unavailable right now. Please try again shortly.' });
    }
});

// ⚡ 6. EXPLICIT NAVIGATION COMPONENTS
app.get('/header.html', (req, res) => {
    const baseDir = process.env.VERCEL ? process.cwd() : path.join(__dirname, '..');
    res.sendFile(path.join(baseDir, 'views/header.html'));
});

app.get('/footer.html', (req, res) => {
    const baseDir = process.env.VERCEL ? process.cwd() : path.join(__dirname, '..');
    res.sendFile(path.join(baseDir, 'views/footer.html'));
});

// ======================================================================
// ⚡ 7. RECURSIVE & CASE-INSENSITIVE CATCH-ALL ROUTER
// Serves the SAME html to every visitor — humans and Googlebot alike.
// No user-agent sniffing anywhere: that is what kept us clear of cloaking.
// ======================================================================
app.get('*', (req, res, next) => {
    if (req.path.startsWith('/api/') || (req.path.includes('.') && !req.path.endsWith('.html'))) {
        return next();
    }

    let requestedPath = req.path.replace(/^\//, '').replace(/\.html$/, '');
    if (!requestedPath || requestedPath === '/') requestedPath = 'index';

    if (requestedPath.startsWith('views/')) {
        requestedPath = requestedPath.replace(/^views\//, '');
    }

    // Reject traversal attempts before touching the filesystem
    if (requestedPath.includes('..') || requestedPath.includes('\0')) {
        return res.status(400).send('Bad Request');
    }

    const rootDir = path.join(__dirname, '..');
    const searchDirs = [
        path.join(rootDir, 'views'),
        path.join(rootDir, 'public')
    ];

    function findFileRecursive(dir, targetPathSegments) {
        if (!fs.existsSync(dir)) return null;

        const currentSegment = targetPathSegments[0].toLowerCase();
        let files;
        try {
            files = fs.readdirSync(dir);
        } catch (e) {
            return null;
        }

        for (const file of files) {
            if (file.toLowerCase() === currentSegment || file.toLowerCase() === currentSegment + '.html') {
                const fullPath = path.join(dir, file);
                const stat = fs.statSync(fullPath);

                if (targetPathSegments.length === 1) {
                    if (stat.isFile()) return fullPath;
                } else if (stat.isDirectory()) {
                    const result = findFileRecursive(fullPath, targetPathSegments.slice(1));
                    if (result) return result;
                }
            }
        }
        return null;
    }

    const pathSegments = requestedPath.split('/').filter(Boolean);
    if (!pathSegments.length) pathSegments.push('index');

    let resolvedFile = null;
    for (const baseDir of searchDirs) {
        resolvedFile = findFileRecursive(baseDir, pathSegments);
        if (resolvedFile) break;
    }

    if (resolvedFile) {
        return res.sendFile(resolvedFile);
    }

    // Serve the real 404 page if there is one, so Google gets a proper 404
    const notFoundPage = path.join(rootDir, 'views', '404.html');
    if (fs.existsSync(notFoundPage)) {
        return res.status(404).sendFile(notFoundPage);
    }
    return res.status(404).send('Page Not Found');
});

// Port Initialization
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`🚀 Operational Pipeline Status: Active On Port: ${PORT}`);
});

module.exports = app;