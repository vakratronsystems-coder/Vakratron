const { GoogleGenAI } = require('@google/genai');
const path = require('path');

// Safe Environment Variables hydration for Gemini Engine
if (!process.env.GEMINI_API_KEY) {
    const rootEnvPath = path.resolve(process.cwd(), '.env');
    require('dotenv').config({ path: rootEnvPath });
}

// 🚨 Debug Guardrail
if (!process.env.GEMINI_API_KEY) {
    console.error('❌ Critical Pipeline Aborted: GEMINI_API_KEY is missing from environment Matrix!');
}

// Initialize Google Gemini Infrastructure Engine safely (Zero-Cost Tier)
const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });

/**
 * AI Gateway Function (Gemini Decoupled Adapter)
 * Handles communication with Google's Flash Core LLM
 */
async function getAIResponse(userMessage) {
    try {
        // Using gemini-2.5-flash as it is extremely fast and free
        const response = await ai.models.generateContent({
            model: 'gemini-2.5-flash',
            contents: userMessage,
            config: {
                systemInstruction: "You are the Vakratron Systems AI Infrastructure Expert. Keep answers technical, concise, and professional. If the user asks to connect with the team, support, or a human, politely tell them to fill out the 'Request Consultation' form on the contact.html page or drop an email to connect@vakratronsys.com."
            }
        });

        return response.text;
    } catch (error) {
        console.error("❌ Gemini Core Engine Error:", error.message);
        throw new Error("Unable to compute AI response at this moment.");
    }
}

module.exports = { getAIResponse };