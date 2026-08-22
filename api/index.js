const express = require('express');
const path = require('path');
const fs = require('fs');
const mongoose = require('mongoose');
const { SitemapStream, streamToPromise } = require('sitemap');
const rateLimit = require('express-rate-limit');

// ======================================================================
// 🛡️ SECURITY & PRE-VALIDATION UTILITIES
// ======================================================================

// 1. IP Rate Limiter (Max 3 OTP requests per 15 minutes per IP)
const otpLimiter = rateLimit({
    windowMs: 15 * 60 * 1000, 
    max: 3, 
    message: { success: false, error: "Too many requests from this IP. Please try again after 15 minutes." },
    standardHeaders: true,
    legacyHeaders: false,
});

// FLEXIBLE GLOBAL PHONE VALIDATOR (NO LEADS BLOCKED)
function isValidGlobalMobile(phone) {
    if (!phone) return false;
    const cleanPhone = phone.replace(/\D/g, ''); // Extract numbers only

    // Global E.164 standard: Minimum 7 digits (small countries) to 15 digits (int'l with country code)
    if (cleanPhone.length < 7 || cleanPhone.length > 15) return false;

    // Reject ONLY obvious dummy spam (e.g. 0000000000 or 1111111111)
    if (/^(\d)\1+$/.test(cleanPhone)) return false;

    return true;
}

// 3. Human Name Check (Blocks Keyboard Smash like "Uoiowwd Mhlaurvgl")
function isValidHumanName(name) {
    if (!name || name.trim().length < 3) return false;
    const cleanName = name.trim();
    if (!/^[a-zA-Z\s]+$/.test(cleanName)) return false;
    const gibberishRegex = /[bcdfghjklmnpqrstvwxyz]{5,}/i;
    if (gibberishRegex.test(cleanName)) return false;
    return true;
}

// 4. Strict Business / Corporate Email Validator (Blocks Gmail, Yahoo, Hotmail, etc.)
function isValidEmailStrict(email) {
    if (!email || !email.includes('@')) return false;
    const [localPart, domain] = email.toLowerCase().split('@');

    // Block Free Public Email Domains Completely
    const publicDomains = [
        'gmail.com', 'yahoo.com', 'yahoo.co.in', 'hotmail.com', 
        'outlook.com', 'icloud.com', 'aol.com', 'zoho.com', 'rediffmail.com'
    ];
    if (publicDomains.includes(domain)) return false;

    // Block Disposable / Temp Domains
    const disposableDomains = [
        'tempmail.com', '10minutemail.com', 'guerrillamail.com', 
        'mailinator.com', 'yopmail.com', 'trashmail.com'
    ];
    if (disposableDomains.includes(domain)) return false;

    // Block Dot-Spam in local address
    const dotCount = (localPart.match(/\./g) || []).length;
    if (dotCount > 3) return false;

    return true;
}

// Environment variables loading configuration mapping one step back to root directory
if (process.env.NODE_ENV !== 'production') {
    require('dotenv').config({ path: path.join(__dirname, '../.env') });
}

const app = express();

// ⚡ 1. GLOBAL PAYLOAD PARSERS
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// ⚡ 2. EXPLICIT STATIC DIRECTORIES BYPASS
app.use(express.static(path.join(__dirname, '../public')));
app.use('/images', express.static(path.join(__dirname, '../public/images')));

// DATABASE SCHEMA & MODEL SETUP
const contactSchema = new mongoose.Schema({
    name: { type: String, required: true },
    email: { type: String, required: true },
    phone: { type: String, required: true },
    reason: { type: String, required: true }
}, { bufferCommands: true });

const Contact = mongoose.models.Contact || mongoose.model('Contact', contactSchema);

if (process.env.MONGO_URI) {
    mongoose.connect(process.env.MONGO_URI, { serverSelectionTimeoutMS: 8000 })
    .then(() => console.log('🚀 Operational Pipeline: MongoDB Atlas Handshake Secured.'))
    .catch(err => console.error('❌ Pipeline Fault:', err));
}

// ⚡ IN-MEMORY OTP STORE (Expires in 10 Mins)
const otpStore = {};

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

// ⚡ 3. SITEMAP EXPLICIT BYPASS
app.get('/sitemap.xml', async (req, res) => {
    try {
        const smStream = new SitemapStream({ hostname: 'https://vakratronsys.com' });
        const pages = new Set();
        const baseDir = process.env.VERCEL ? process.cwd() : path.join(__dirname, '..');

        function scan(folder) {
            if (!fs.existsSync(folder)) return;
            const files = fs.readdirSync(folder);
            files.forEach(file => {
                if (file === 'header.html' || file === 'footer.html' || file === '404.html') return;
                const full = path.join(folder, file);
                if (fs.statSync(full).isDirectory()) {
                    scan(full);
                } else if (file.endsWith('.html')) {
                    let url = full.replace(path.join(baseDir, 'views'), '').replace(path.join(baseDir, 'public'), '').replace(/\\/g, '/');
                    if (url.endsWith('/index.html')) url = url.replace('/index.html', '/');
                    url = url.replace('.html', '');
                    if (url === '/index') url = '/';
                    pages.add(url);
                }
            });
        }

        scan(path.join(baseDir, 'views'));
        scan(path.join(baseDir, 'public'));

        pages.forEach(p => {
            smStream.write({
                url: p,
                lastmod: new Date(),
                changefreq: p === "/" ? "daily" : "weekly",
                priority: p === "/" ? 1.0 : 0.8
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

// ⚡ 4. CONTACT FORM SUBMISSION ENDPOINT (WITH GLOBAL VALIDATION & SHEET SYNC)
app.post('/api/contact', async (req, res) => {
    try {
        const { name, email, phone, reason } = req.body;
        
        if (!isValidHumanName(name)) {
            return res.status(400).json({ success: false, error: "Please enter a valid full name." });
        }
        if (!isValidGlobalMobile(phone)) {
            return res.status(400).json({ success: false, error: "Please enter a valid phone number with country code." });
        }
        if (!isValidEmailStrict(email)) {
            return res.status(400).json({ success: false, error: "Personal emails are not allowed. Please enter your Corporate Email." });
        }

        console.log('📥 Processing Request Matrix for Client:', name);

        const newContact = new Contact({ name, email, phone, reason });
        await newContact.save();

        // 📊 SILENT BACKGROUND PUSH TO GOOGLE SHEET
        const sheetWebhook = process.env.GOOGLE_SHEET_WEBHOOK_URL;
        if (sheetWebhook) {
            fetchWithTimeout(sheetWebhook, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    name: name, 
                    email: email, 
                    phone: phone, 
                    company: 'Direct Contact Form', 
                    pageRequested: reason || 'Contact Us Page' 
                })
            }).catch(err => console.error("⚠️ [Contact Sheet Error]:", err.message));
        }

        res.status(200).json({ success: true });

        // Email Dispatch
        setImmediate(async () => {
            const apiKey = process.env.RESEND_OTP_API_KEY || process.env.RESEND_API_KEY;
            if (!apiKey) return;

            try {
                await fetchWithTimeout('https://api.resend.com/emails', {
                    method: 'POST',
                    headers: { 'Authorization': `Bearer ${apiKey}`, 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        from: 'Vakratron Core <onboarding@resend.dev>',
                        to: 'vakratronsystems@gmail.com', 
                        subject: '🚨 New Enterprise Architectural Blueprint Request Ingested',
                        html: `
                            <div style="font-family: Arial, sans-serif; padding: 20px; background: #0f172a; color: #fff; border-radius: 8px;">
                                <h2 style="color: #38bdf8;">⚡ Core Cluster Inbound Lead Detected</h2>
                                <hr style="border-color: rgba(255,255,255,0.1);" />
                                <p><strong>Client Name:</strong> ${name}</p>
                                <p><strong>Communication Link:</strong> ${email}</p>
                                <p><strong>Secure Phone Vector:</strong> ${phone}</p>
                                <p><strong>Architectural Track:</strong> <span style="color: #f43f5e; font-weight: bold;">${reason}</span></p>
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
            return res.status(500).json({ success: false, error: error.message });
        }
    }
});

// ======================================================================
// ⚡ 4.1. DEEP-TECH OTP GATING API ENDPOINTS (WITH TIMEOUT & SPAM PROTECTION)
// ======================================================================

// ⚡ OPTION 2: SINGLE EMAIL WITH BCC (STRICT ALL-FIELD VALIDATION)
app.post('/api/send-otp', otpLimiter, async (req, res) => {
    try {
        const { name, email, phone, company, pageRequested } = req.body;

        // 🛡️ A. STRICT PRE-VALIDATION (हर एक फील्ड अनिवार्य है)
        if (!isValidHumanName(name)) {
            return res.status(400).json({ success: false, error: "Please enter a valid full name." });
        }

        if (!isValidEmailStrict(email)) {
            return res.status(400).json({ 
                success: false, 
                error: "Personal emails (Gmail, Yahoo, etc.) are not allowed. Please enter your official Corporate / Business Email." 
            });
        }

        if (!isValidGlobalMobile(phone)) {
            return res.status(400).json({ 
                success: false, 
                error: "Please enter a valid phone number with country code (e.g. +91 9876543210)." 
            });
        }

        const generatedOtp = Math.floor(1000 + Math.random() * 9000).toString();
        
        otpStore[email] = {
            otp: generatedOtp,
            name: name,
            phone: phone,
            company: company,
            pageRequested: pageRequested,
            expiresAt: Date.now() + 10 * 60 * 1000
        };

        // 📊 B. SILENT BACKGROUND PUSH TO GOOGLE SHEET
        const sheetWebhook = process.env.GOOGLE_SHEET_WEBHOOK_URL;
        if (sheetWebhook) {
            console.log("📊 [Google Sheet Push]: Dispatching lead data...");
            fetchWithTimeout(sheetWebhook, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, email, phone, company, pageRequested })
            })
            .then(() => console.log("✅ [Google Sheet Success]: Lead Row Inserted!"))
            .catch(err => console.error("⚠️ [Google Sheet Error]:", err.message));
        }

        const apiKey = process.env.RESEND_OTP_API_KEY || process.env.RESEND_API_KEY;
        if (!apiKey) {
            return res.status(500).json({ success: false, error: "Server email key missing." });
        }

        // ⚡ C. SINGLE RESEND API CALL WITH BCC
        await fetchWithTimeout('https://api.resend.com/emails', {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${apiKey}`, 'Content-Type': 'application/json' },
            body: JSON.stringify({
                from: 'Vakratron Systems <auth@vakratronsys.com>',
                to: [email],
                bcc: ['vakratronsystems@gmail.com'],
                subject: `🔑 Access Code: ${generatedOtp} - Vakratron Systems`,
                html: `
                    <div style="font-family: Arial, sans-serif; background: #0f172a; color: #ffffff; padding: 24px; border-radius: 12px; max-width: 500px; margin: 0 auto;">
                        <h2 style="color: #38bdf8; margin-top: 0;">Vakratron Systems</h2>
                        <p>Hello <b>${name}</b>,</p>
                        <p>Use the following 4-digit code to verify your access for the requested Deep-Tech Architecture Specification:</p>
                        <div style="text-align: center; margin: 24px 0;">
                            <span style="background: #020617; border: 1px solid #C2185B; padding: 12px 24px; font-size: 2rem; font-weight: bold; letter-spacing: 8px; color: #C2185B; border-radius: 8px; display: inline-block;">${generatedOtp}</span>
                        </div>
                        <p style="color: #94a3b8; font-size: 0.8rem;">This code is valid for 10 minutes.</p>
                        <div style="margin-top: 30px; padding-top: 15px; border-top: 1px dashed rgba(255,255,255,0.2); font-size: 0.78rem; color: #64748b;">
                            <span>Client: ${name} | Phone: ${phone} | Company: ${company || 'N/A'} | Page: ${pageRequested}</span>
                        </div>
                    </div>
                `
            })
        });

        res.status(200).json({ success: true, message: "OTP sent successfully." });

    } catch (err) {
        console.error("❌ Send OTP Error:", err);
        res.status(500).json({ success: false, error: "Email delivery failed or timed out." });
    }
});

// ⚡ OTP VERIFY + CONFIRMATION EMAIL
app.post('/api/verify-otp', async (req, res) => {
    try {
        const { email, otpCode } = req.body;
        const record = otpStore[email];

        if (!record) return res.json({ success: false, error: "No OTP request found." });
        if (Date.now() > record.expiresAt) {
            delete otpStore[email];
            return res.json({ success: false, error: "OTP expired." });
        }

        if (record.otp === otpCode.toString().trim()) {
            const leadData = { ...record };
            delete otpStore[email];

            const apiKey = process.env.RESEND_OTP_API_KEY || process.env.RESEND_API_KEY;
            if (apiKey) {
                fetchWithTimeout('https://api.resend.com/emails', {
                    method: 'POST',
                    headers: { 'Authorization': `Bearer ${apiKey}`, 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        from: 'Vakratron Systems <auth@vakratronsys.com>',
                        to: [email],
                        subject: `📄 Access Unlocked: ${leadData.pageRequested || 'Architecture Blueprint'} - Vakratron Systems`,
                        html: `
                            <div style="font-family: Arial, sans-serif; background: #0f172a; color: #ffffff; padding: 28px; border-radius: 12px; max-width: 550px; margin: 0 auto;">
                                <h2 style="color: #38bdf8; margin-top: 0;">Vakratron Systems</h2>
                                <p style="font-size: 1.05rem;">Dear <b>${leadData.name || 'Valued Client'}</b>,</p>
                                <p>Thank you for verifying your credentials. You now have full unlocked access to our Enterprise Architecture Specification Blueprint:</p>
                                <div style="background: #1e293b; border-left: 4px solid #38bdf8; padding: 16px; margin: 20px 0; border-radius: 4px;">
                                    <h4 style="margin: 0 0 6px 0; color: #f8fafc;">${leadData.pageRequested || 'Deep-Tech Solution Blueprint'}</h4>
                                    <p style="margin: 0; color: #94a3b8; font-size: 0.85rem;">Status: <b>Unlocked & Verified Access</b></p>
                                </div>
                                <p>If you wish to discuss custom enterprise deployments or workload sizing with our Principal Solutions Architect, feel free to reply directly to this email or visit us at <a href="https://vakratronsys.com" style="color: #38bdf8; text-decoration: none;">vakratronsys.com</a>.</p>
                                <hr style="border: 0; border-top: 1px solid rgba(255,255,255,0.1); margin: 24px 0;" />
                                <p style="color: #64748b; font-size: 0.8rem; margin: 0;">Best Regards,<br><strong style="color: #cbd5e1;">Enterprise Architecture Team</strong><br>Vakratron Systems</p>
                            </div>
                        `
                    })
                }).catch(err => console.error("⚠️ Confirmation Email Error:", err.message));
            }

            return res.json({ success: true, message: "Verification successful!" });
        }

        res.json({ success: false, error: "Invalid OTP code." });

    } catch (err) {
        console.error("❌ Verify OTP Error:", err);
        res.status(500).json({ success: false, error: "Verification server error." });
    }
});

// ⚡ 5. SOVEREIGN AI INTERACTION GATEWAY
app.post('/api/chat', async (req, res) => {
    try {
        const { message } = req.body;
        if (!message) return res.status(400).json({ error: "Missing prompt token matrix." });

        const apiKey = process.env.GROQ_API_KEY;
        if (!apiKey) return res.status(500).json({ error: "Hardware engine credential layer defect." });

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
- ONLY AFTER discussing their environment, offer a formal deliverable (HLD, BOQ Sizing). Ask for Company Name, Email, and Phone ONLY when requested.`;

        const groqRawFetch = await fetchWithTimeout('https://api.groq.com/openai/v1/chat/completions', {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${apiKey}`, 'Content-Type': 'application/json' },
            body: JSON.stringify({
                model: 'llama-3.3-70b-versatile', 
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
        } else {
            return res.status(500).json({ error: "External matrix format parsing crash." });
        }

    } catch (error) {
        console.error('💥 SYSTEM EXCEPTION CRASH DUMP IN GATEWAY:', error.stack);
        return res.status(500).json({ error: "Architecture engine stack trace runtime fault." });
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

// ⚡ 7. CATCH-ALL ROUTER FOR RENDER HOSTING
// =========================================================
// ⚡ RECURSIVE & CASE-INSENSITIVE ROUTER FOR PRODUCTION
// =========================================================
const fs = require('fs');

app.get('*', (req, res, next) => {
    // API calls, static assets (images, css, js) ko express.static handle karne de
    if (req.path.startsWith('/api/') || (req.path.includes('.') && !req.path.endsWith('.html'))) {
        return next();
    }

    let requestedPath = req.path.replace(/^\//, '').replace(/\.html$/, '');
    if (!requestedPath || requestedPath === '/') requestedPath = 'index';

    // Stripping extra '/views/' if present in the URL
    if (requestedPath.startsWith('views/')) {
        requestedPath = requestedPath.replace(/^views\//, '');
    }

    const rootDir = path.join(__dirname, '..');
    const searchDirs = [
        path.join(rootDir, 'views'),
        path.join(rootDir, 'public')
    ];

    // Helper function for recursive, case-insensitive search (Linux production fix)
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

    const pathSegments = requestedPath.split('/');
    let resolvedFile = null;

    for (const baseDir of searchDirs) {
        resolvedFile = findFileRecursive(baseDir, pathSegments);
        if (resolvedFile) break;
    }

    if (resolvedFile) {
        return res.sendFile(resolvedFile);
    } else {
        return res.status(404).send('Page Not Found');
    }
});

// Server Listen (agar niche app.listen hai to uske upar ise rakhein)

// Port Initialization
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`🚀 Operational Pipeline Status: Active On Port: ${PORT}`);
});

module.exports = app;