import { google } from 'googleapis';
import { GoogleGenAI } from '@google/genai';
import nodemailer from 'nodemailer';
import dotenv from 'dotenv';
import fs from 'fs';

dotenv.config();

const SITE_URL = 'https://vakratronsys.com/';

// Credentials Loader (Env variable check, then local file fallback)
function getGscCredentials() {
    if (process.env.GSC_KEY_JSON) {
        try {
            return JSON.parse(process.env.GSC_KEY_JSON);
        } catch (e) {
            console.error('❌ Failed to parse GSC_KEY_JSON env variable:', e.message);
        }
    }
    
    const keyFilePath = './gsc-key.json';
    if (fs.existsSync(keyFilePath)) {
        return JSON.parse(fs.readFileSync(keyFilePath, 'utf8'));
    }

    throw new Error('❌ No GSC Credentials found!');
}

async function fetchSearchConsoleData() {
    const keys = getGscCredentials();

    const auth = new google.auth.JWT({
        email: keys.client_email,
        key: keys.private_key,
        scopes: ['https://www.googleapis.com/auth/webmasters.readonly'],
    });

    const searchconsole = google.searchconsole({ version: 'v1', auth });

    const endDate = new Date();
    endDate.setDate(endDate.getDate() - 2);
    const startDate = new Date();
    startDate.setDate(startDate.getDate() - 9);

    const res = await searchconsole.searchanalytics.query({
        siteUrl: SITE_URL,
        requestBody: {
            startDate: startDate.toISOString().split('T')[0],
            endDate: endDate.toISOString().split('T')[0],
            dimensions: ['query', 'page'],
            rowLimit: 25,
        },
    });

    return res.data.rows || [];
}

async function sendSeoReportEmail(reportText) {
    console.log('🔍 Checking Email Credentials...');
    console.log('GMAIL_USER present:', !!process.env.GMAIL_USER);
    console.log('GMAIL_APP_PASS present:', !!process.env.GMAIL_APP_PASS);

    if (!process.env.GMAIL_USER || !process.env.GMAIL_APP_PASS) {
        console.log('❌ Error: GMAIL_USER ya GMAIL_APP_PASS secrets missing hain!');
        return;
    }

    console.log('📧 Sending email via Nodemailer...');

    try {
        const transporter = nodemailer.createTransport({
            service: 'gmail',
            auth: {
                user: process.env.GMAIL_USER,
                pass: process.env.GMAIL_APP_PASS,
            },
        });

        const formattedHtml = reportText
            .replace(/\n/g, '<br>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

        const mailOptions = {
            from: `"Vakratron SEO Agent" <${process.env.GMAIL_USER}>`,
            to: process.env.GMAIL_USER,
            subject: `📊 Daily SEO Audit Report - Vakratron Systems (${new Date().toLocaleDateString('en-IN')})`,
            html: `
                <div style="font-family: Arial, sans-serif; padding: 20px; color: #333; line-height: 1.6;">
                    <h2 style="color: #0d6efd; border-bottom: 2px solid #0d6efd; padding-bottom: 8px;">
                        🚀 Vakratron Systems - Daily SEO & Growth Report
                    </h2>
                    <div>${formattedHtml}</div>
                    <hr style="margin-top: 30px; border: 0; border-top: 1px solid #ccc;">
                    <p style="font-size: 12px; color: #777;">Automated Daily Audit by Vakratron AI Agent</p>
                </div>
            `,
        };

        const info = await transporter.sendMail(mailOptions);
        console.log('✅ Email Successfully Sent! Response:', info.response);
    } catch (err) {
        console.error('❌ Nodemailer Error:', err.message);
    }
}

async function runSeoAudit() {
    try {
        console.log('🔍 Search Console se performance data fetch ho raha hai...');
        const rows = await fetchSearchConsoleData();

        console.log('🤖 Gemini API se Audit Report generate ho rahi hai...\n');
        
        const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });

        const prompt = `
        You are an expert Enterprise SEO & Growth Strategist for Vakratron Systems (vakratronsys.com).
        
        Here is the recent Google Search Console performance data:
        ${JSON.stringify(rows, null, 2)}
        
        Provide a structured, actionable SEO Audit & Growth Report in simple Hindi/English mixing:
        1. 🚨 **Health & Technical Audit**: Mention any suspicious/leaked prompt queries, broken flows, or indexation issues.
        2. 📈 **CTR & Ranking Booster**: Identify queries with high impressions but 0 clicks. Provide EXACT optimized Meta Titles & Meta Descriptions to fix them.
        3. 🚀 **Content Strategy**: Suggest 1 high-intent technical blog title + short outline that will help rank for these queries.
        `;

        const response = await ai.models.generateContent({
            model: 'gemini-2.5-flash',
            contents: prompt,
        });

        const reportContent = response.text;

        console.log('================ 📊 DAILY SEO AGENT REPORT ================');
        console.log(reportContent);
        console.log('==========================================================\n');

        // Explicitly Await Email Function with Logs
        console.log('🚀 Triggering Email Step...');
        await sendSeoReportEmail(reportContent);

    } catch (error) {
        console.error('❌ Critical Error during SEO Audit execution:', error);
    }
}
runSeoAudit();