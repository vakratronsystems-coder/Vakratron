const express = require('express');
const path = require('path');
const fs = require('fs');
const mongoose = require('mongoose');
const { SitemapStream, streamToPromise } = require('sitemap');

// Environment variables loading configuration mapping one step back to root directory
if (process.env.NODE_ENV !== 'production') {
    require('dotenv').config({ path: path.join(__dirname, '../.env') });
}

const app = express();

// ⚡ 1. GLOBAL PAYLOAD PARSERS (ALWAYS AT THE ABSOLUTE TOP)
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// ⚡ 2. EXPLICIT STATIC DIRECTORIES BYPASS (Fixes styling & script breaks across deep nodes)
app.use(express.static(path.join(__dirname, '../public')));
app.use('/images', express.static(path.join(__dirname, '../public/images')));
// app.use('/views/portfolio', express.static(path.join(__dirname, '../views/portfolio')));
// app.use('/views', express.static(path.join(__dirname, '../views')));

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

// ⚡ 3. SITEMAP EXPLICIT BYPASS
app.get('/sitemap.xml', async (req, res) => {
    try {
        const smStream = new SitemapStream({
            hostname: 'https://vakratronsys.com'
        });

        const pages = new Set();

        function scan(folder) {
            if (!fs.existsSync(folder)) return;
            
            const files = fs.readdirSync(folder);
            files.forEach(file => {
                if (file === 'header.html' || file === 'footer.html' || file === '404.html') {
                    return;
                }
            
                const full = path.join(folder, file);

                if (fs.statSync(full).isDirectory()) {
                    scan(full);
                } else if (file.endsWith('.html')) {
                    let url = full
                    .replace(path.join(__dirname, '../views'), '')
                    .replace(path.join(__dirname, '../public'), '')
                    .replace(/\\/g, '/');
                
                    if (url.endsWith('/index.html')) {
                        url = url.replace('/index.html', '/');
                    }
                    
                    url = url.replace('.html', '');
                    
                    if (url === '/index') {
                        url = '/';
                    }
                    
                    pages.add(url);
                }
            });
        }

        scan(path.join(__dirname, '../views'));
        scan(path.join(__dirname, '../public'));

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
    res.send(`User-agent: *
Allow: /

Sitemap: https://vakratronsys.com/sitemap.xml`);
});

// ⚡ 4. CONTACT FORM SUBMISSION ENDPOINT
app.post('/api/contact', async (req, res) => {
    try {
        const { name, email, phone, reason } = req.body;
        
        if (!name || !email) {
            console.error('⚠️ Empty cluster data block rejected.');
            return res.status(400).json({ success: false, error: "Payload token defect" });
        }

        console.log('📥 Processing Request Matrix for Client:', name);

        const newContact = new Contact({ name, email, phone, reason });
        await newContact.save();
        console.log('✅ Data Cluster Ingestion: Record committed successfully.');

        res.status(200).json({ success: true });

        // Asynchronous background email dispatch via Resend
        setImmediate(async () => {
            if (!process.env.RESEND_API_KEY) {
                console.error('⚠️ Alert Pipeline Aborted: Missing RESEND_API_KEY.');
                return;
            }

            try {
                const response = await fetch('https://api.resend.com/emails', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${process.env.RESEND_API_KEY}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        from: 'Vakratron Core <alert@vakratronsys.com>',
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

                const data = await response.json();
                if (response.ok) {
                    console.log('📬 Resend API Pipeline: Notification dispatched. ID:', data.id);
                } else {
                    console.error('⚠️ Resend API Ingestion Rejection:', data);
                }
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
// ⚡ 5. SOVEREIGN AI INTERACTION GATEWAY (DIAGNOSTIC PIPELINE ACTIVE)
// ======================================================================
// ======================================================================
// ⚡ 5. SOVEREIGN AI INTERACTION GATEWAY (HUMAN CONSULTANT ENGINE)
// ======================================================================
app.post('/api/chat', async (req, res) => {
    try {
        const { message } = req.body;
        console.log('📥 INBOUND LEAD CORE TRACE - Received User Token String:', message);

        if (!message) {
            console.error('⚠️ Input verification failure: Empty query frame.');
            return res.status(400).json({ error: "Missing prompt token matrix." });
        }

        const apiKey = process.env.GROQ_API_KEY;
        if (!apiKey) {
            console.error('❌ CONFIGURATION ERROR: process.env.GROQ_API_KEY undefined or null!');
            return res.status(500).json({ error: "Hardware engine credential layer defect." });
        }

        const systemDirectives = `You are Vakra-Bot, a Principal Cloud & AI Infrastructure Architect at Vakratron Systems. You talk like a real human peer and senior solution architect—NOT an automated template engine or robotic bot.

======================================================================
1. WARM WELCOME & OPTIONAL NAME ONBOARDING
======================================================================
- If a user first greets you (e.g. "hi", "hello"), greet them warmly in 1-2 lines and optionally ask for their name in a frictionless way.
- Example: "Hello 👋 Welcome to Vakratron Systems! I'm Vakra-Bot, Principal Infrastructure Architect. May I know your name before we begin? (Skip if you prefer!) How can I help engineer your infrastructure today?"

======================================================================
2. HUMAN CONVERSATIONAL DIALOGUE (NO ROBOTIC TEMPLATES)
======================================================================
- TALK LIKE A REAL PERSON: Speak in a natural, professional, and friendly tone (English or natural Hinglish matching the user's vibe).
- NO FIXED HEADINGS OR TEMPLATES: NEVER use structured headers like "### Problem Assessment", "### Trade-off Analysis", "### Recommended Blueprint", or "### Business Impact".
- KEEP IT CONCISE & DIALOGUE-BASED: Keep responses short (3 to 5 sentences max per turn). Discuss their requirement, ask 1 or 2 focused questions about their environment (e.g., On-Prem or Cloud? Workload size? Target RPO/RTO?), and build the architecture together step-by-step.

======================================================================
3. PROGRESSIVE LEAD CAPTURE AT HIGH VALUE
======================================================================
- ONLY AFTER discussing their environment and sharing initial architectural insights, offer a formal deliverable (HLD, BOQ Sizing, DR Roadmap).
- Ask for Company Name, Email, and Phone ONLY when they want a formal HLD/BOQ generated.`;

        console.log('📡 Dispatching raw network payload frame to external LPU grid nodes...');
        const groqRawFetch = await fetch('https://api.groq.com/openai/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                model: 'llama-3.3-70b-versatile', 
                messages: [
                    { role: 'system', content: systemDirectives },
                    { role: 'user', content: message }
                ],
                temperature: 0.3,
                max_tokens: 1024
            })
        });

        const rawDataBlock = await groqRawFetch.json();
        console.log('📬 RESPONSE INGESTION DETECTED - Server Status Code:', groqRawFetch.status);

        if (rawDataBlock.choices && rawDataBlock.choices[0]) {
            const compiledOutputText = rawDataBlock.choices[0].message.content;
            console.log('✅ TRANSLATION COMPLETION SECURE: Token layout validated.');
            return res.status(200).json({ response: compiledOutputText });
        } else {
            console.error('❌ RAW DATA BLOCK INGESTION STRUCT DEFECT:', JSON.stringify(rawDataBlock));
            return res.status(500).json({ error: "External matrix format parsing crash." });
        }

    } catch (error) {
        console.error('💥 SYSTEM EXCEPTION CRASH DUMP IN GATEWAY:', error.stack);
        return res.status(500).json({ error: "Architecture engine stack trace runtime fault." });
    }
});

// ⚡ 6. EXPLICIT NAVIGATION COMPONENTS
app.get('/header.html', (req, res) => {
    res.sendFile(path.join(__dirname, '../views/header.html'));
});

app.get('/footer.html', (req, res) => {
    res.sendFile(path.join(__dirname, '../views/footer.html'));
});

// ======================================================================
// ⚡ 7. STRICT ISOLATED CATCH-ALL ROUTER FOR HTML VIEWS & BOT INJECTION (CASE INSENSITIVE FIX)
// ======================================================================
// ======================================================================
// ⚡ 7. STRICT ISOLATED CATCH-ALL ROUTER FOR ALL HTML VIEWS & GLOBAL BOT INJECTION
// ======================================================================
app.get('*', (req, res, next) => {
    if (req.path.startsWith('/api/') || (req.path.includes('.') && !req.path.endsWith('.html'))) {
        return next();
    }

    let requestedPage = req.params[0] ? req.params[0].replace(/^\//, '') : '';

    if (!requestedPage || requestedPage === '/') {
        requestedPage = 'index.html';
    }

    if (requestedPage.startsWith('views/')) {
        requestedPage = requestedPage.replace('views/', '');
    }

    if (requestedPage.endsWith('/')) {
        requestedPage += 'index.html';
    } else if (!requestedPage.includes('.')) {
        requestedPage += '.html';
    }

    const portfolioCheck = path.join(__dirname, '../views/portfolio', requestedPage);
    const viewsPath = path.join(__dirname, '../views', requestedPage);
    const publicPath = path.join(__dirname, '../public', requestedPage);

    let finalResolvedPath = null;
    if (fs.existsSync(portfolioCheck)) {
        finalResolvedPath = portfolioCheck;
    } else if (fs.existsSync(viewsPath)) {
        finalResolvedPath = viewsPath;
    } else if (fs.existsSync(publicPath)) {
        finalResolvedPath = publicPath;
    }

    if (finalResolvedPath && finalResolvedPath.endsWith('.html')) {
        fs.readFile(finalResolvedPath, 'utf8', (err, htmlContent) => {
            if (err) return res.status(404).send('Resource Matrix Fault: Target Not Found');

            const chatScriptPayload = '\n<!-- Dynamic Sovereign Bot Script Injected Globally -->\n<script src="/vakra-chat.js"></script>\n';
            let updatedHtml = htmlContent;

            if (/<\/body>/i.test(htmlContent)) {
                updatedHtml = htmlContent.replace(/(<\/body>)/i, `${chatScriptPayload}$1`);
            } else {
                updatedHtml = htmlContent + chatScriptPayload;
            }

            res.setHeader('Content-Type', 'text/html');
            return res.send(updatedHtml);
        });
    } else {
        next();
    }
});
// ⚡ 8. DEFAULT 404 ROUTE
app.use((req, res) => {
    res.status(404).send('Resource Matrix Fault: Target Not Found');
});

// Port Initialization
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`🚀 Operational Pipeline Status: Active On Port: ${PORT}`);
});

module.exports = app;