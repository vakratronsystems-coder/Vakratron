const express = require('express');
const path = require('path');
const fs = require('fs');
const mongoose = require('mongoose');
const { getAIResponse } = require('../services/aiService');

if (process.env.NODE_ENV !== 'production') {
    require('dotenv').config({ path: path.join(__dirname, '../.env') });
}

const app = express();

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// ⚡ 1. DIRECT XML SITEMAP PIPELINE BYPASS ROUTE (Strict Production Fix)
app.use('/sitemap.xml', (req, res) => {
    const sitemapPath = path.join(__dirname, '../public/sitemap.xml');
    if (fs.existsSync(sitemapPath)) {
        res.header('Content-Type', 'application/xml');
        return res.sendFile(sitemapPath);
    }
    res.status(404).send('Sitemap not found');
});

// ⚡ 2. UNIVERSAL CROSS-DIRECTORY FILE INTERCEPTOR (INDEX RENDERING FIX)
// ⚡ 2. UNIVERSAL CROSS-DIRECTORY FILE INTERCEPTOR (FIXED FOR PORTFOLIO AND ALIGNMENT)
app.use((req, res, next) => {
    // Static assets ko directly skip karo (except HTML)
    if (req.path.includes('.') && !req.path.endsWith('.html')) {
        return next();
    }

    // Strict block guardrail for contact page AND sitemap pipeline
    if (req.path.toLowerCase().includes('contact') || req.path.toLowerCase().includes('sitemap')) {
        return next();
    }

    let cleanPath = decodeURIComponent(req.path);
    let targetFile = cleanPath;
    
    if (targetFile === '/' || targetFile.toLowerCase() === '/index' || targetFile.toLowerCase() === '/index.html') {
        targetFile = 'index.html';
    }
    
    if (targetFile.startsWith('/')) targetFile = targetFile.substring(1);
    if (targetFile.startsWith('views/')) targetFile = targetFile.replace('views/', '');
    if (!targetFile.endsWith('.html') && targetFile.length > 0) targetFile += '.html';

    // 🚀 CRITICAL FIX: Portfolio pages ko fs.readFile se bacha kar direct native sendFile par bhejo
    const portfolioPath = path.join(__dirname, '../views/portfolio', targetFile);
    if (fs.existsSync(portfolioPath)) {
        res.setHeader('Content-Type', 'text/html');
        return res.sendFile(portfolioPath);
    }

    // Baaki normal pages ke liye aapka original fs.readFile logic intact rakha hai
    const publicPath = path.join(__dirname, '../public', targetFile);
    const viewsPath = path.join(__dirname, '../views', targetFile);

    let finalResolvedPath = null;
    if (fs.existsSync(viewsPath)) {
        finalResolvedPath = viewsPath;
    } else if (fs.existsSync(publicPath)) {
        finalResolvedPath = publicPath;
    }

    if (finalResolvedPath) {
        fs.readFile(finalResolvedPath, 'utf8', (err, htmlContent) => {
            if (err) return next();

            if (htmlContent.includes('</body>')) {
                const updatedHtml = htmlContent.replace(
                    '</body>', 
                    '<script src="/vakra-chat.js"></script></body>'
                );
                return res.send(updatedHtml);
            }
            res.send(htmlContent);
        });
    } else {
        next();
    }
});
// Serve static assets out of the public folder mapping
app.use(express.static(path.join(__dirname, '../public')));
app.use('/images', express.static(path.join(__dirname, '../public/images')));

// 👑 EXPLICIT STATIC CONTENT SYNC (Locks alignment mapping)
app.use('/views/portfolio', express.static(path.join(__dirname, '../views/portfolio')));
app.use('/views', express.static(path.join(__dirname, '../views')));

// DATABASE SCHEMA & MODEL SETUP
const contactSchema = new mongoose.Schema({
    name: { type: String, required: true },
    email: { type: String, required: true },
    phone: { type: String, required: true },
    reason: { type: String, required: true }
}, { bufferCommands: true }); // Keep true so queries wait smoothly if DB is connecting during a cold start

const Contact = mongoose.models.Contact || mongoose.model('Contact', contactSchema);

// GLOBAL CONNECTION POOL
if (process.env.MONGO_URI) {
    mongoose.connect(process.env.MONGO_URI, {
        serverSelectionTimeoutMS: 8000 // 8 seconds guardrail for cloud cold-starts
    })
    .then(() => console.log('🚀 Operational Pipeline: MongoDB Atlas Handshake Secured.'))
    .catch(err => console.error('❌ Pipeline Fault: Connection Refused.', err));
}

// FORM SUBMISSION PIPELINE (Resend HTTP API Architecture - Certified Domain)
app.post('/api/contact', async (req, res) => {
    try {
        const { name, email, phone, reason } = req.body;
        console.log('📥 Processing Request Matrix for Client:', name);

        // 1. Ingest into MongoDB Cluster smoothly
        const newContact = new Contact({ name, email, phone, reason });
        await newContact.save();
        console.log('✅ Data Cluster Ingestion: Record committed successfully.');

        // 2. IMMEDIATE HTTP RELEASE: Respond to frontend instantly!
        res.status(200).json({ success: true });

        // 3. ASYNCHRONOUS BACKGROUND API EMAIL DISPATCH (No SMTP Port Blocks)
        setImmediate(async () => {
            if (!process.env.RESEND_API_KEY) {
                console.error('⚠️ Alert Pipeline Aborted: Missing RESEND_API_KEY environment variable.');
                return;
            }

            try {
                // Utilizing standard HTTPS Port 443 over API instead of legacy mail ports
                const response = await fetch('https://api.resend.com/emails', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${process.env.RESEND_API_KEY}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        from: 'Vakratron Core <alert@vakratronsys.com>', // 🔥 UPDATE SECURED HERE (LANDS IN INBOX)
                        to: 'vakratronsystems@gmail.com', // Aapka official dynamic destination inbox
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
                    console.log('📬 Resend API Pipeline: Notification dispatched successfully. ID:', data.id);
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

// 🔥 NEW SECURE AI INTERACTION ENDPOINT (Decoupled execution gateway)
app.post('/api/chat', async (req, res) => {
    try {
        const { message } = req.body;
        if (!message) {
            return res.status(400).json({ error: "Payload execution defect: Missing prompt token." });
        }
        
        console.log('📡 Routing Matrix: Forwarding instruction to Gemini Core Engine...');
        const aiResponse = await getAIResponse(message);
        
        res.status(200).json({ response: aiResponse });
    } catch (error) {
        console.error('❌ Core Compute Fault on /api/chat:', error.message);
        res.status(500).json({ error: "Architecture failure: Unable to compute AI response stack." });
    }
});

// EXPLICIT STATIC COMPONENT ISOLATION (No Overlaps, Clean Content Streams)
app.get('/header.html', (req, res) => {
    const headerPath = path.join(__dirname, '../views/header.html');
    if (fs.existsSync(headerPath)) {
        res.setHeader('Content-Type', 'text/html');
        return res.sendFile(headerPath);
    }
    res.status(404).send('Header blueprint missing');
});

app.get('/footer.html', (req, res) => {
    const footerPath = path.join(__dirname, '../views/footer.html');
    if (fs.existsSync(footerPath)) {
        res.setHeader('Content-Type', 'text/html');
        return res.sendFile(footerPath);
    }
    res.status(404).send('Footer blueprint missing');
});

// Safe File Injection Engine
function serveFileWithGapFix(filePath, res) {
    if (fs.existsSync(filePath)) {
        res.setHeader('Content-Type', 'text/html');
        return res.sendFile(filePath);
    }
    const indexFallback = path.join(__dirname, '../views/index.html');
    res.setHeader('Content-Type', 'text/html');
    res.sendFile(indexFallback);
}

// CATCH-ALL ROUTER FOR STRUCTURAL VALIDATION (Opens exact requested pages)
app.get(/(.*)/, (req, res) => {
    let requestedPage = req.params[0] ? req.params[0].replace(/^\//, '') : '';

    if (!requestedPage) {
        return serveFileWithGapFix(path.join(__dirname, '../views/index.html'), res);
    }

    if (requestedPage === 'header.html' || requestedPage === 'footer.html') {
        return;
    }

    if (requestedPage.startsWith('views/')) {
        requestedPage = requestedPage.replace('views/', '');
    }

    if (requestedPage.endsWith('/')) {
        requestedPage += 'index.html';
    } else if (!requestedPage.includes('.')) {
        requestedPage += '.html';
    }

    // 🚀 PORFTOLIO GRACEFUL DIRECTORY ROUTER RESOLUTION
    let filePath = path.join(__dirname, '../views', requestedPage);
    let portfolioCheck = path.join(__dirname, '../views/portfolio', requestedPage);

    if (fs.existsSync(portfolioCheck)) {
        res.setHeader('Content-Type', 'text/html');
        return res.sendFile(portfolioCheck);
    }

    serveFileWithGapFix(filePath, res);
});

// ====== Render Persistent Server Port Initialization ======
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`🚀 Operational Pipeline Status: Active`);
    console.log(`📡 Cluster Engine Syncing On Port: ${PORT}`);
});

module.exports = app;