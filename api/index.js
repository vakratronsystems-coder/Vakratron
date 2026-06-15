const express = require('express');
const path = require('path');
const fs = require('fs');
const mongoose = require('mongoose');

if (process.env.NODE_ENV !== 'production') {
    require('dotenv').config({ path: path.join(__dirname, '../.env') });
}

const app = express();

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve static assets out of the public folder mapping
app.use(express.static(path.join(__dirname, '../public')));
app.use('/images', express.static(path.join(__dirname, '../public/images')));

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

// FORM SUBMISSION PIPELINE (Resend HTTP API Architecture)
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

    if (requestedPage.endsWith('/')) {
        requestedPage += 'index.html';
    } else if (!requestedPage.includes('.')) {
        requestedPage += '.html';
    }

    const filePath = path.join(__dirname, '../views', requestedPage);
    serveFileWithGapFix(filePath, res);
});

// ====== Render Persistent Server Port Initialization ======
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`🚀 Operational Pipeline Status: Active`);
    console.log(`📡 Cluster Engine Syncing On Port: ${PORT}`);
});

module.exports = app;