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
// ✅ 1. Standardize Static Middleware Layers (Sabhi component maps ko top standard par rakhein)
app.use(express.static(path.join(__dirname, '../public')));
app.use('/images', express.static(path.join(__dirname, '../public/images')));

// ✅ 2. EXPLICIT STATIC COMPONENT BYPASS (Vercel runtime crash protection)
// Agar header ya footer manga jaye, toh use direct clean view response bhejein
app.get('/header.html', (req, res) => {
    const headerPath = path.join(__dirname, '../views/header.html');
    if (fs.existsSync(headerPath)) {
        res.setHeader('Content-Type', 'text/html');
        return res.sendFile(headerPath);
    }
    res.status(404).send('Header not found');
});

app.get('/footer.html', (req, res) => {
    const footerPath = path.join(__dirname, '../views/footer.html');
    if (fs.existsSync(footerPath)) {
        res.setHeader('Content-Type', 'text/html');
        return res.sendFile(footerPath);
    }
    res.status(404).send('Footer not found');
});

// Dynamic Clean HTML File Server Utility
function serveFileWithGapFix(filePath, res) {
    if (fs.existsSync(filePath)) {
        const html = fs.readFileSync(filePath, 'utf8');
        res.setHeader('Content-Type', 'text/html');
        return res.send(html);
    }
    // Deep fallback sequence
    const indexFallback = path.join(__dirname, '../views/index.html');
    const html = fs.readFileSync(indexFallback, 'utf8');
    res.setHeader('Content-Type', 'text/html');
    res.send(html);
}

// ✅ 3. Isolated Dynamic Catch-All Router (Bypasses component files seamlessly)
app.get(/(.*)/, (req, res) => {
    let requestedPage = req.params[0] ? req.params[0].replace(/^\//, '') : '';

    if (!requestedPage) {
        return serveFileWithGapFix(path.join(__dirname, '../views/index.html'), res);
    }

    // Static asset leak safeguard
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

module.exports = app;