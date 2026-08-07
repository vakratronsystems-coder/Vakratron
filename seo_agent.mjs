import { google } from 'googleapis';
import { GoogleGenAI } from '@google/genai';
import dotenv from 'dotenv';
import fs from 'fs';

dotenv.config();

const SITE_URL = 'https://vakratronsys.com/';

// Credentials Loader (Env variable pehle check karega, fir local file fallback)
function getGscCredentials() {
    if (process.env.GSC_KEY_JSON) {
        try {
            return JSON.parse(process.env.GSC_KEY_JSON);
        } catch (e) {
            console.error('❌ Failed to parse GSC_KEY_JSON env variable:', e.message);
        }
    }
    
    // Fallback: Agar local env mein path / file ho
    const keyFilePath = './gsc-key.json';
    if (fs.existsSync(keyFilePath)) {
        return JSON.parse(fs.readFileSync(keyFilePath, 'utf8'));
    }

    throw new Error('❌ No GSC Credentials found in process.env.GSC_KEY_JSON or gsc-key.json file!');
}

async function fetchSearchConsoleData() {
    const keys = getGscCredentials();

    const auth = new google.auth.JWT({
        email: keys.client_email,
        key: keys.private_key,
        scopes: ['https://www.googleapis.com/auth/webmasters.readonly'],
    });

    const searchconsole = google.searchconsole({ version: 'v1', auth });

    // Date range calculation (last 7 days data)
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

async function runSeoAudit() {
    try {
        console.log('🔍 Search Console se performance data fetch ho raha hai...');
        const rows = await fetchSearchConsoleData();

        console.log('🤖 Gemini API se Daily Audit & Growth Report generate ho rahi hai...\n');
        
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

        console.log('================ 📊 DAILY SEO AGENT REPORT ================');
        console.log(response.text);
        console.log('==========================================================');

    } catch (error) {
        console.error('❌ Error during SEO Audit execution:', error);
    }
}

runSeoAudit();