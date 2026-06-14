const express = require('express');
const path = require('path');
const fs = require('fs');
const mongoose = require('mongoose');
const nodemailer = require('nodemailer');

// Dynamic path mapping for .env file from root directory
require('dotenv').config({ path: path.join(__dirname, '../.env') });

const app = express();

// --- MIDDLEWARES FOR FORM HANDLING ---
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// 1. Saari static assets ko public folder se serve karein
// ✅ Static assets pipeline bypass rule (Images, CSS, JS sabke liye explicit route match)
app.use(express.static(path.join(__dirname, '../public')));
app.use('/images', express.static(path.join(__dirname, '../public/images')));

// ==========================================
// 2. DATABASE SCHEMA & MODEL SETUP
// ==========================================
const contactSchema = new mongoose.Schema({
    name: { type: String, required: true },
    email: { type: String, required: true },
    phone: { type: String, required: true },
    reason: { type: String, required: true },
    submittedAt: { type: Date, default: Date.now }
});

const Contact = mongoose.model('Contact', contactSchema);

// ==========================================
// 3. HELPER FUNCTION: LIVE GMAIL DIRECT SELF-ALERT PIPELINE
// ==========================================
async function sendEmailNotification(data) {
    const transporter = nodemailer.createTransport({
        service: 'gmail',
        auth: {
            user: process.env.GMAIL_USER,
            pass: process.env.GMAIL_APP_PASS
        }
    });

    // Cleaned standard HTML content structure without syntax risk
    const htmlContent = `
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden;">
        <div style="background: linear-gradient(135deg, #C2185B 0%, #9d174d 100%); padding: 25px; text-align: center; color: white;">
            <h2 style="margin: 0; font-size: 1.5rem; letter-spacing: 1px;">🚀 New Operational Vector Locked</h2>
            <p style="margin: 5px 0 0 0; opacity: 0.9; font-size: 0.9rem;">Vakratron Systems - Cloud Infrastructure Portal</p>
        </div>
        <div style="padding: 30px; background-color: #f8fafc; color: #334155;">
            <p style="font-size: 1rem; margin-top: 0;">Bhai, a new enterprise consultation request has hit the backend pipeline. Details are logged below:</p>
            <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
                <tr>
                    <td style="padding: 10px 0; border-bottom: 1px solid #e2e8f0; font-weight: bold; width: 35%;">Full Name:</td>
                    <td style="padding: 10px 0; border-bottom: 1px solid #e2e8f0;">${data.name}</td>
                </tr>
                <tr>
                    <td style="padding: 10px 0; border-bottom: 1px solid #e2e8f0; font-weight: bold;">Email ID:</td>
                    <td style="padding: 10px 0; border-bottom: 1px solid #e2e8f0;">${data.email}</td>
                </tr>
                <tr>
                    <td style="padding: 10px 0; border-bottom: 1px solid #e2e8f0; font-weight: bold;">Phone Number:</td>
                    <td style="padding: 10px 0; border-bottom: 1px solid #e2e8f0;">${data.phone}</td>
                </tr>
                <tr>
                    <td style="padding: 10px 0; border-bottom: 1px solid #e2e8f0; font-weight: bold;">Inquiry Vector:</td>
                    <td style="padding: 10px 0; border-bottom: 1px solid #e2e8f0; font-weight: 500;">${data.reason}</td>
                </tr>
            </table>
            <div style="margin-top: 30px; padding: 15px; background-color: #f1f5f9; border-radius: 8px; font-size: 0.85rem; color: #64748b; text-align: center;">
                This packet was automatically routed via Vakratron Secure Server Cluster to vakratronsystems@gmail.com.
            </div>
        </div>
    </div>
    `;

    const mailOptions = {
        from: `"Vakratron Systems Ingestion" <${process.env.GMAIL_USER}>`,
        to: process.env.GMAIL_USER, // Self-sending mechanism
        subject: `🚨 New Lead: ${data.reason} - ${data.name}`,
        html: htmlContent
    };

    await transporter.sendMail(mailOptions);
    console.log('📬 Notification email successfully dispatched to vakratronsystems@gmail.com!');
}

// ==========================================
// 4. POST ENDPOINT FOR CONTACT FORM SUBMISSION
// ==========================================
app.post('/api/contact', async (req, res) => {
    try {
        console.log('--- NEW INCOMING REQUEST LOG ---');
        console.log('📥 Raw req.body received:', req.body); 
        
        const { name, email, phone, reason } = req.body;

        if (!name || !email || !phone || !reason) {
            console.log('❌ Validation Failed! Missing data matrix.');
            return res.status(400).json({ success: false, error: 'All fields are required!' });
        }

        const newContact = new Contact({ name, email, phone, reason });
        await newContact.save();
        console.log('✅ Lead securely locked in MongoDB Atlas cluster!');

        try {
            await sendEmailNotification({ name, email, phone, reason });
        } catch (emailErr) {
            console.error('⚠️ Gmail SMTP Dispatch Failed, but data is saved in DB:', emailErr.message);
        }

        return res.status(200).json({ success: true, message: 'Data packet recorded safely.' });

    } catch (error) {
        console.error('❌ Mongoose operational crash details:', error.message);
        return res.status(500).json({ success: false, error: 'Internal Server Error' });
    }
});

// ==========================================
// 5. FRONT-END ROUTING (HTML PAGES)
// ==========================================
app.get('/', (req, res) => {
    serveFileWithGapFix(path.join(__dirname, '../views/index.html'), res);
});

// Dynamic Catch-All Router (Regex Based - Supports Multilevel Deep Subdirectories)
app.get(/(.*)/, (req, res) => {
    let requestedPage = req.params[0] ? req.params[0].replace(/^\//, '') : '';

    if (!requestedPage) {
        return serveFileWithGapFix(path.join(__dirname, '../views/index.html'), res);
    }

    // Agar end me slash hai toh index page ki taraf route karein
    if (requestedPage.endsWith('/')) {
        requestedPage += 'index.html';
    } else if (!requestedPage.includes('.')) {
        // Agar extension missing hai toh automatically .html Append karein
        requestedPage += '.html';
    }

    // Absolute filepath configuration from root views directory
    const filePath = path.join(__dirname, '../views', requestedPage);

    if (fs.existsSync(filePath)) {
        serveFileWithGapFix(filePath, res);
    } else {
        // 404 Fallback
        console.log(`⚠️ Route Mismatch, falling back to index: ${requestedPage}`);
        serveFileWithGapFix(path.join(__dirname, '../views/index.html'), res);
    }
});

function serveFileWithGapFix(filePath, res) {
    fs.readFile(filePath, 'utf8', (err, data) => {
        if (err) return res.status(500).send('Server Error');

        const gapFixStyle = `
<style>
  header, .header, .navbar { padding-bottom: 0px !important; margin-bottom: 0px !important; }
  .hero, main, section:first-of-type, [class*="section"] { margin-top: -80px !important; position: relative; z-index: 99; }
  main:has(.architectural-badge), section:has([class*="badge"]), .portfolio-section, .grid-section, section:first-of-type:has(span) { margin-top: -30px !important; }
</style>
        `;

        let updatedHtml = data;
        if (data.includes('</header>')) {
            updatedHtml = data.replace('</header>', `</header>${gapFixStyle}`);
        } else if (data.includes('</body>')) {
            updatedHtml = data.replace('</body>', `${gapFixStyle}</body>`);
        } else {
            updatedHtml = data + gapFixStyle;
        }
        res.send(updatedHtml);
    });
}

module.exports = app;

// ==========================================
// 6. SECURE CLOUD SYNCHRONIZATION RUNNER
// ==========================================
const mongoURI = process.env.MONGO_URI;

if (process.env.NODE_ENV !== 'production') {
    if (!mongoURI) {
        console.error('⚠️ MONGO_URI missing in environmental variables (.env file)!');
        process.exit(1);
    }

    mongoose.connect(mongoURI)
        .then(() => {
            console.log('🍃 MongoDB Atlas Cloud Connected Successfully!');
            const PORT = process.env.PORT || 3000;
            app.listen(PORT, () => {
                console.log(`🚀 Secure R&D Server running locally on: http://localhost:${PORT}`);
            });
        })
        .catch(err => {
            console.error('❌ MongoDB Initialization Cluster Error:', err.message);
        });
}