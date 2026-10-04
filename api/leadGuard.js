/* Lead quality guard for /api/contact (Oct 2026).
 *
 * Why: bots were posting straight to /api/contact (never loading the site),
 * using random-letter names and other people's email addresses. Each one
 * landed in the inbox and the sheet, and the enquirer auto-reply went to a
 * stranger's address, which also hurts our sending reputation.
 *
 * Layers:
 *  1. Signed form token: the page asks /api/form-token when it loads and
 *     sends it back with the enquiry. A script that never loads the page has
 *     no token. Stateless HMAC, so it works across serverless instances.
 *  2. Gibberish-name check: letter pairs that do not occur in real names
 *     (tuned to accept Indian compound names such as Rajkumar, Sukhpreet, Iqbal).
 *  3. Phone shape: country code, or a valid Indian number.
 *  4. Email shape: Gmail dot-alias throwaways ("u.fodo.xi.no32"), placeholder
 *     domains (xyz.com, example.com) and domains with no mail servers.
 *  5. Email one-time code: the enquiry is only delivered once the person types
 *     the 6-digit code we emailed them, so a made-up address can never get through.
 */
const crypto = require('crypto');
const dns = require('dns').promises;

const SECRET = process.env.FORM_TOKEN_SECRET ||
    crypto.createHash('sha256').update('vk-form-token|' + (process.env.MONGO_URI || '') + '|' + (process.env.RESEND_API_KEY || '')).digest('hex');
const TOKEN_MIN_AGE_MS = 3000;            // nobody fills the form in under 3 s
const TOKEN_MAX_AGE_MS = 12 * 60 * 60 * 1000;
// Until this date an enquiry WITHOUT a token is still accepted if it passes the
// stricter checks (covers browsers holding the old cached script). After it, or
// when FORM_TOKEN_REQUIRED=true, tokenless enquiries are dropped silently.
const TOKEN_GRACE_UNTIL = Date.parse('2026-10-15T00:00:00Z');

function sign(payload) {
    return crypto.createHmac('sha256', SECRET).update(payload).digest('base64url').slice(0, 32);
}

function issueFormToken() {
    const payload = Date.now().toString(36) + '.' + crypto.randomBytes(6).toString('base64url');
    return payload + '.' + sign(payload);
}

/** 'valid' | 'missing' | 'invalid' | 'too-fast' */
function checkFormToken(token, now = Date.now()) {
    if (!token) return 'missing';
    const parts = String(token).split('.');
    if (parts.length !== 3) return 'invalid';
    const payload = parts[0] + '.' + parts[1];
    const expect = sign(payload);
    const a = Buffer.from(parts[2]); const b = Buffer.from(expect);
    if (a.length !== b.length || !crypto.timingSafeEqual(a, b)) return 'invalid';
    const issued = parseInt(parts[0], 36);
    if (!Number.isFinite(issued)) return 'invalid';
    const age = now - issued;
    if (age < TOKEN_MIN_AGE_MS) return 'too-fast';
    if (age > TOKEN_MAX_AGE_MS) return 'invalid';
    return 'valid';
}

function tokenRequired(now = Date.now()) {
    return process.env.FORM_TOKEN_REQUIRED === 'true' || now > TOKEN_GRACE_UNTIL;
}

// Letter pairs that essentially never occur inside real personal names,
// in English or in romanised Indian names. Kept deliberately short:
// pairs like jg (Rajgopal), hp (Sukhpreet), qb (Iqbal), cg (McGregor) are NOT here.
const BAD_PAIRS = new Set((
    'qc qd qf qg qh qj qk qm qn qp qs qt qv qw qx qz ' +
    'bx cx dx fx gx hx jx kx lx mx px qx sx tx vx wx zx ' +
    'xz xj xq xk xv xg xb xd xf xp ' +
    'cg cj cv cf cb cd cp cq cw ' +
    'jq jx jz jf vq vx vz vf vc vw gq gx gz bq bz kq kz pq pz dq dz ' +
    'fq fv fj hq hz lq mq nq rq tq wq wz zq yq'
).split(' ').filter(Boolean));

function wordLooksRandom(raw) {
    let w = raw.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z]/g, '');
    if (w.length < 3) return false;             // initials and short names are fine
    if (w.startsWith('mc') || w.startsWith('mac')) w = w.replace(/^ma?c/, '');
    if (/^([b-df-hj-np-tv-z])\1/.test(w) && !w.startsWith('ll')) return true;   // "Nnwobg"
    for (let i = 0; i < w.length - 1; i++) {
        if (BAD_PAIRS.has(w[i] + w[i + 1])) return true;                       // "Ulfx"
    }
    return false;
}

function nameLooksRandom(name) {
    const words = String(name || '').trim().split(/\s+/).filter(Boolean);
    const latin = words.filter(w => /[a-z]/i.test(w));
    if (!latin.length) return false;            // non-Latin scripts: leave to other checks
    return latin.some(wordLooksRandom);
}

/** Country code, or a well-formed Indian number. */
function phoneLooksReal(phone) {
    const s = String(phone || '').trim();
    const d = s.replace(/\D/g, '');
    if (s.startsWith('+') || s.startsWith('00')) {
        const intl = s.startsWith('00') ? d.slice(2) : d;
        if (intl.startsWith('91')) return /^91[6-9]\d{9}$/.test(intl);   // India: real mobile only
        return intl.length >= 8 && intl.length <= 15;
    }
    if (d.length === 10) return /^[6-9]/.test(d);                 // Indian mobile
    if (d.length === 11) return /^0[1-9]/.test(d);                // 0 + mobile or STD landline
    if (d.length === 12) return /^91[6-9]/.test(d);               // 91 + mobile
    return false;
}

/** Gmail-style throwaway local parts: 3+ dots, or several 1-2 letter fragments. */
function emailLooksThrowaway(email) {
    const [local = '', domain = ''] = String(email || '').toLowerCase().split('@');
    const parts = local.split('.');
    const tiny = parts.filter(p => p.length <= 2).length;
    if ((domain === 'gmail.com' || domain === 'googlemail.com') && parts.length >= 4) return true;
    return parts.length >= 4 && tiny >= 3;
}

// Domains people type when they do not want to give a real address.
const PLACEHOLDER_DOMAINS = new Set([
    'example.com', 'example.org', 'example.net', 'example.in', 'test.com', 'test.in', 'testing.com',
    'xyz.com', 'abc.com', 'abcd.com', 'abc.in', 'xyz.in', 'domain.com', 'yourdomain.com',
    'company.com', 'yourcompany.com', 'sample.com', 'demo.com', 'fake.com', 'none.com',
    'asdf.com', 'qwerty.com', '123.com', 'aaa.com', 'email.example', 'noemail.com', 'na.com',
    // common misspellings that bounce
    'gmial.com', 'gamil.com', 'gmai.com', 'gmail.co', 'gmail.con', 'gmail.cm', 'yaho.com', 'yahooo.com', 'hotmial.com', 'outlok.com'
]);
function emailDomainLooksFake(email) {
    const domain = String(email || '').toLowerCase().split('@')[1] || '';
    return PLACEHOLDER_DOMAINS.has(domain);
}

/** true if the domain publishes mail servers. Fails OPEN on DNS timeouts so a slow resolver never loses a lead. */
async function emailDomainReceives(email, timeoutMs = 2500) {
    const domain = String(email || '').toLowerCase().split('@')[1] || '';
    if (!domain) return false;
    const lookup = dns.resolveMx(domain).then(mx => Array.isArray(mx) && mx.some(r => r && r.exchange && r.exchange !== '.'))
        .catch(err => (err && (err.code === 'ENOTFOUND' || err.code === 'ENODATA' || err.code === 'NXDOMAIN')) ? false : true);
    const timer = new Promise(r => setTimeout(() => r(true), timeoutMs));
    return Promise.race([lookup, timer]);
}

// Email one-time code, stateless: the server signs (email, code, expiry) and
// hands back only the signature. Works across serverless instances, no store.
const OTP_TTL_MS = 20 * 60 * 1000;
function issueEmailCode(email) {
    const code = String(crypto.randomInt(0, 1000000)).padStart(6, '0');
    const exp = (Date.now() + OTP_TTL_MS).toString(36);
    const token = exp + '.' + sign('otp|' + String(email).toLowerCase().trim() + '|' + code + '|' + exp);
    return { code, token };
}
/** 'valid' | 'missing' | 'expired' | 'wrong' */
function checkEmailCode(email, code, token, now = Date.now()) {
    if (!code || !token) return 'missing';
    const [exp, sig] = String(token).split('.');
    if (!exp || !sig) return 'wrong';
    if (now > parseInt(exp, 36)) return 'expired';
    const expect = sign('otp|' + String(email).toLowerCase().trim() + '|' + String(code).replace(/\D/g, '') + '|' + exp);
    const a = Buffer.from(sig); const b = Buffer.from(expect);
    return (a.length === b.length && crypto.timingSafeEqual(a, b)) ? 'valid' : 'wrong';
}

// Topic strings from the OLD contact form. That form is gone from the site,
// so a submission carrying one of these was not typed into our current pages.
const LEGACY_REASONS = new Set([
    'AI Infrastructure & GPU Clusters Planning',
    'Hybrid/Private Cloud Solutions Architecture',
    'Data Centre & Life Safety Security Design',
    'General Corporate Inquiry',
]);

module.exports = { issueFormToken, checkFormToken, tokenRequired, nameLooksRandom, phoneLooksReal, emailLooksThrowaway, emailDomainLooksFake, emailDomainReceives, issueEmailCode, checkEmailCode, LEGACY_REASONS, wordLooksRandom };
