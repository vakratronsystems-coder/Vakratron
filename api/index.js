const express = require('express');
const path = require('path');
const fs = require('fs');
const mongoose = require('mongoose');
const nodemailer = require('nodemailer');

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

// FORM SUBMISSION PIPELINE (Zero-Lag Asynchronous Threading)
app.post('/api/contact', async (req, res) => {
    try {
        const { name, email, phone, reason } = req.body;
        console.log('📥 Processing Request Matrix for Client:', name);

        // 1. Ingest into MongoDB Cluster smoothly
        const newContact = new Contact({ name, email, phone, reason });
        await newContact.save();
        console.log('✅ Data Cluster Ingestion: Record committed successfully.');

        // 2. IMMEDIATE HTTP RELEASE: Respond to frontend instantly!
        // Iske chalte user ka button ghumna turant band ho jayega
        res.status(200).json({ success: true });

        // 3. MAIL ENGINE EXECUTION ISOLATION (No Await, Background Thread)
        setImmediate(async () => {
            if (!process.env.GMAIL_USER || !process.env.GMAIL_APP_PASS) {
                console.error('⚠️ Alert Pipeline Aborted: Missing environment credentials.');
                return;
            }

            try {
                const transporter = nodemailer.createTransport({
                    host: 'smtp.gmail.com',
                    port: 465,
                    secure: true, // Upgraded SSL protocol standard
                    auth: {
                        user: process.env.GMAIL_USER,
                        pass: process.env.GMAIL_APP_PASS
                    },
                    tls: {
                        rejectUnauthorized: false // Bypasses explicit proxy/cloud node blocks
                    }
                });

                const mailOptions = {
                    from: `"Vakratron Core Alert Engine" <${process.env.GMAIL_USER}>`,
                    to: process.env.GMAIL_USER,
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
                };

                await transporter.sendMail(mailOptions);
                console.log('📬 Background Alert Pipeline: Notification dispatched.');
            } catch (mailError) {
                console.error('⚠️ Background Notification Network Blocked:', mailError.message);
            }
        });

    } catch (error) {
        console.error('❌ Runtime Ingestion Defect:', error);
        // Only return server fault if response wasn't already dispatched above
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