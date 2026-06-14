const express = require('express');
const path = require('path');
const fs = require('fs');
const mongoose = require('mongoose');
const nodemailer = require('nodemailer');

// Local execution environments ke liye safe wrap
if (process.env.NODE_ENV !== 'production') {
    require('dotenv').config({ path: path.join(__dirname, '../.env') });
}

const app = express();

// --- MIDDLEWARES FOR FORM HANDLING ---
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Saari static assets pipeline bypass layout maps
app.use(express.static(path.join(__dirname, '../public')));
app.use('/images', express.static(path.join(__dirname, '../public/images')));

// DATABASE SCHEMA & MODEL SETUP
const contactSchema = new mongoose.Schema({
    name: { type: String, required: true },
    email: { type: String, required: true },
    phone: { type: String, required: true },
    reason: { type: String, required: true }
});
const Contact = mongoose.models.Contact || mongoose.model('Contact', contactSchema);

// MONGODB ATLAS CLOUD HANDSHAKE
if (process.env.MONGO_URI) {
    mongoose.connect(process.env.MONGO_URI)
        .then(() => console.log('🚀 Operational Pipeline: MongoDB Atlas Handshake Secured.'))
        .catch(err => console.error('❌ Pipeline Fault: Connection Refused.', err));
}

// SECURE FORM INGESTION ENDPOINT
app.post('/api/contact', async (req, res) => {
    try {
        const { name, email, phone, reason } = req.body;
        
        const newContact = new Contact({ name, email, phone, reason });
        await newContact.save();

        const transporter = nodemailer.createTransport({
            service: 'gmail',
            auth: {
                user: process.env.GMAIL_USER,
                pass: process.env.GMAIL_APP_PASS
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
        res.status(200).json({ success: true });

    } catch (error) {
        console.error('Runtime Ingestion Defect:', error);
        res.status(500).json({ success: false, error: error.message });
    }
});

// Dynamic Clean HTML File Server
function serveFileWithGapFix(filePath, res) {
    if (fs.existsSync(filePath)) {
        const html = fs.readFileSync(filePath, 'utf8');
        res.setHeader('Content-Type', 'text/html');
        return res.send(html);
    }
    // Fallback code agar sub-directory file mismatch ho
    const indexFallback = path.join(__dirname, '../views/index.html');
    const html = fs.readFileSync(indexFallback, 'utf8');
    res.setHeader('Content-Type', 'text/html');
    res.send(html);
}

// Dynamic Catch-All Router 
app.get(/(.*)/, (req, res) => {
    let requestedPage = req.params[0] ? req.params[0].replace(/^\//, '') : '';

    if (!requestedPage) {
        return serveFileWithGapFix(path.join(__dirname, '../views/index.html'), res);
    }

    if (requestedPage.endsWith('/')) {
        requestedPage += 'index.html';
    } else if (!requestedPage.includes('.')) {
        requestedPage += '.html';
    }

    const filePath = path.join(__dirname, '../views', requestedPage);
    serveFileWithGapFix(filePath, res);
});

module.exports = app;