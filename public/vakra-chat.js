// 🦾 VAKRATRON CYBER AI INFRASTRUCTURE & DESIGN SUITE WIDGET - PRODUCTION ULTIMATE CORE
(() => {
    // ==========================================
    // MODULE 1: AI CORE MATRIX WIDGET
    // ==========================================
    function initVakraWidget() {
        if (window.location.pathname.includes('contact.html')) return; 
        if (document.getElementById('chatTrigger')) return;

        const chatStyles = document.createElement('style');
        chatStyles.innerHTML = `
            #chatTrigger {
                position: fixed !important; bottom: 30px !important; right: 30px !important;
                width: 60px !important; height: 60px !important; min-width: 60px !important; min-height: 60px !important;
                border-radius: 50% !important; background: linear-gradient(135deg, #C2185B 0%, #9d174d 100%) !important;
                box-shadow: 0 4px 25px rgba(194, 24, 91, 0.5) !important; border: 1px solid rgba(255,255,255,0.2) !important;
                cursor: pointer !important; z-index: 99999991 !important; display: flex !important; align-items: center !important; justify-content: center !important;
                padding: 0 !important; margin: 0 !important; transition: all 0.2s ease-in-out !important;
            }
            #chatTrigger:hover { transform: scale(1.08) !important; box-shadow: 0 6px 30px rgba(194, 24, 91, 0.7) !important; }
            
            .vakra-chat-window {
                position: fixed !important; bottom: 95px !important; right: 30px !important;
                width: 380px !important; height: calc(100vh - 140px) !important; 
                max-height: 560px !important; min-height: 380px !important;
                display: none !important; flex-direction: column !important;
                background: rgba(15, 23, 42, 0.96) !important; backdrop-filter: blur(20px) !important; -webkit-backdrop-filter: blur(20px) !important;
                border: 1px solid rgba(194, 24, 91, 0.4) !important; 
                box-shadow: 0 20px 50px rgba(0,0,0,0.8), 0 0 40px rgba(194, 24, 91, 0.15) !important;
                border-radius: 16px !important; z-index: 99999992 !important; overflow: hidden !important; box-sizing: border-box !important;
            }
            
            .vakra-chat-window.active { display: flex !important; }
            .vakra-chat-header { background: rgba(194, 24, 91, 0.2) !important; border-bottom: 1px solid rgba(194, 24, 91, 0.4) !important; padding: 15px 20px !important; display: flex !important; align-items: center !important; justify-content: space-between !important; }
            .vakra-chat-header h3 { margin: 0 !important; font-family: 'Poppins', sans-serif !important; font-size: 1.05rem !important; font-weight: 600 !important; color: #fff !important; display: flex !important; align-items: center !important; gap: 10px !important; }
            .vakra-chat-header h3 span { width: 8px !important; height: 8px !important; background: #10b981 !important; border-radius: 50% !important; display: inline-block !important; box-shadow: 0 0 8px #10b981 !important; }
            .vakra-chat-close { background: transparent !important; border: none !important; color: #94a3b8 !important; cursor: pointer !important; font-size: 1.1rem !important; }
            .vakra-chat-messages { flex: 1 !important; padding: 20px !important; overflow-y: auto !important; display: flex !important; flex-direction: column !important; gap: 15px !important; background: rgba(2, 6, 23, 0.4) !important; }
            .vakra-msg { max-width: 85% !important; padding: 12px 16px !important; border-radius: 14px !important; font-size: 0.92rem !important; line-height: 1.5 !important; word-wrap: break-word !important; }
            .vakra-msg.system { background: rgba(30, 41, 59, 0.7) !important; border: 1px solid rgba(255, 255, 255, 0.08) !important; color: #e2e8f0 !important; align-self: flex-start !important; border-top-left-radius: 2px !important; }
            .vakra-msg.user { background: linear-gradient(135deg, #C2185B 0%, #9d174d 100%) !important; border: 1px solid rgba(194, 24, 91, 0.4) !important; color: #fff !important; align-self: flex-end !important; border-top-right-radius: 2px !important; }
            .vakra-chat-input-area { padding: 15px 20px !important; border-top: 1px solid rgba(255, 255, 255, 0.08) !important; background: #0f172a !important; display: flex !important; gap: 10px !important; align-items: center !important; }
            .vakra-chat-input { flex: 1 !important; background: rgba(2, 6, 23, 0.8) !important; border: 1px solid rgba(255, 255, 255, 0.1) !important; border-radius: 10px !important; padding: 12px !important; color: #fff !important; font-size: 0.9rem !important; outline: none !important; font-family: 'Inter', sans-serif !important; }
            .vakra-chat-send { background: rgba(56, 189, 248, 0.1) !important; border: 1px solid rgba(56, 189, 248, 0.3) !important; color: #38bdf8 !important; width: 44px !important; height: 44px !important; border-radius: 10px !important; display: flex !important; align-items: center !important; justify-content: center !important; cursor: pointer !important; }
            .vakra-chat-send:hover { background: #38bdf8 !important; color: #020617 !important; box-shadow: 0 0 15px rgba(56, 189, 248, 0.4) !important; }
            .vakra-typing { display: flex; gap: 4px; padding: 5px 0; align-items: center; }
            .vakra-typing span { width: 6px; height: 6px; background: #94a3b8; border-radius: 50%; animation: vakraBounce 1.4s infinite ease-in-out both; }
            .vakra-typing span:nth-child(1) { animation-delay: -0.32s; }
            .vakra-typing span:nth-child(2) { animation-delay: -0.16s; }
            @keyframes vakraBounce { 0%, 80%, 100% { transform: scale(0); } 40% { transform: scale(1.0); } }
        `;
        document.head.appendChild(chatStyles);

        const chatContainer = document.createElement('div');
        chatContainer.innerHTML = `
            <div id="chatTrigger" title="Query AI Architecture Matrix">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width: 28px !important; height: 28px !important; color: #fff !important; display: block !important;"><path d="M12 8V4H8"></path><rect width="16" height="12" x="4" y="8" rx="2"></rect><path d="M2 14h2"></path><path d="M20 14h2"></path><path d="M15 13v2"></path><path d="M9 13v2"></path></svg>
            </div>
            <div class="vakra-chat-window" id="chatWindow">
                <div class="vakra-chat-header">
                    <h3><span></span> Vakratron Core AI Matrix</h3>
                    <button class="vakra-chat-close" id="chatClose">✕</button>
                </div>
                <div class="vakra-chat-messages" id="chatMessages">
                    <div class="vakra-msg system">System Online. Greetings from Vakratron Systems Core Infrastructure Pipeline. How can I assist you with accelerated compute matrices, hypervisor failovers, or high-density cloud blueprints today?</div>
                </div>
                <div class="vakra-chat-input-area">
                    <input type="text" class="vakra-chat-input" id="chatInput" placeholder="Input prompt token matrix..." autocomplete="off">
                    <button class="vakra-chat-send" id="chatSend">➤</button>
                </div>
            </div>
        `;
        document.body.appendChild(chatContainer);

        const trigger = document.getElementById('chatTrigger');
        const windowEl = document.getElementById('chatWindow');
        const closeBtn = document.getElementById('chatClose');
        const sendBtn = document.getElementById('chatSend');
        const inputEl = document.getElementById('chatInput');
        const messagesContainer = document.getElementById('chatMessages');

        trigger.onclick = function(e) {
            e.preventDefault();
            e.stopPropagation();
            if (windowEl.style.display === 'flex') {
                windowEl.style.setProperty('display', 'none', 'important');
            } else {
                windowEl.style.setProperty('display', 'flex', 'important');
                inputEl.focus();
            }
        };

        closeBtn.onclick = function(e) {
            e.preventDefault();
            windowEl.style.setProperty('display', 'none', 'important');
        };

        async function dispatchUserPrompt() {
            const promptValue = inputEl.value.trim();
            if (!promptValue) return;

            appendBubble(promptValue, 'user');
            inputEl.value = '';

            const typingIndicator = document.createElement('div');
            typingIndicator.className = 'vakra-msg system';
            typingIndicator.innerHTML = `<div class="vakra-typing"><span></span><span></span><span></span></div>`;
            messagesContainer.appendChild(typingIndicator);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;

            try {
                const apiResponse = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: promptValue })
                });

                const dataset = await apiResponse.json();
                typingIndicator.remove();

                if (apiResponse.ok && dataset.response) {
                    appendBubble(dataset.response, 'system');
                    const lowerMessage = promptValue.toLowerCase();
                    if (lowerMessage.includes('connect') || lowerMessage.includes('talk to human')) {
                        setTimeout(() => {
                            appendBubble("⚡ System Action: Redirecting token matrix to the Sovereign Advisory Desk...", 'system');
                            setTimeout(() => { window.location.href = 'contact.html'; }, 1500);
                        }, 1000);
                    }
                } else {
                    appendBubble("Execution Defect: Unable to pipeline calculated tokens from LLM core.", 'system');
                }
            } catch (networkError) {
                if(typingIndicator) typingIndicator.remove();
                appendBubble("Network Fault: Endpoint connectivity degraded or blocked.", 'system');
            }
        }

        function appendBubble(content, actor) {
            const bubble = document.createElement('div');
            bubble.className = `vakra-msg ${actor}`;
            bubble.innerHTML = content.replace(/\n/g, '<br>');
            messagesContainer.appendChild(bubble);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }

        sendBtn.onclick = dispatchUserPrompt;
        inputEl.onkeydown = function(e) { if (e.key === 'Enter') dispatchUserPrompt(); };
    }

    // ==========================================
    // MODULE 2: VAKRATRON BRANDED ARCHITECTURE SUITE
    // ==========================================
    function initVakraWhiteboard() {
        if (document.getElementById('whiteboardTrigger')) return;

        const boardStyles = document.createElement('style');
        boardStyles.innerHTML = `
            #whiteboardTrigger {
                position: fixed !important; bottom: 30px !important; right: 105px !important; 
                width: 60px !important; height: 60px !important; border-radius: 50% !important; 
                background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
                box-shadow: 0 4px 25px rgba(0, 0, 0, 0.6) !important; border: 1px solid rgba(194, 24, 91, 0.4) !important;
                cursor: pointer !important; z-index: 99999991 !important; display: flex !important; align-items: center !important; justify-content: center !important;
                transition: all 0.2s ease-in-out !important;
            }
            #whiteboardTrigger:hover { 
                transform: scale(1.08) !important; border-color: #C2185B !important;
                box-shadow: 0 6px 30px rgba(194, 24, 91, 0.4) !important; 
            }
            
            .vakra-board-overlay {
                position: fixed !important; top: 0 !important; left: 0 !important;
                width: 100vw !important; height: 100vh !important;
                background: rgba(15, 23, 42, 0.9) !important; backdrop-filter: blur(20px) !important; -webkit-backdrop-filter: blur(20px) !important;
                z-index: 99999999 !important; display: none; flex-direction: column !important; box-sizing: border-box !important;
            }
            
            .vakra-board-header {
                background: #0f172a !important; border-bottom: 1px solid rgba(194, 24, 91, 0.3) !important;
                padding: 14px 30px !important; display: flex !important; align-items: center !important; justify-content: space-between !important;
                color: #fff !important; font-family: 'Poppins', sans-serif !important;
            }
            
            .vakra-board-footer {
                background: #0f172a !important; border-top: 1px solid rgba(255, 255, 255, 0.06) !important;
                padding: 8px 30px !important; display: flex !important; justify-content: space-between;
                color: #64748b !important; font-family: 'Inter', sans-serif !important; font-size: 0.78rem !important; letter-spacing: 0.03em;
            }
            
            .vakra-board-close {
                background: rgba(194, 24, 91, 0.1) !important; border: 1px solid rgba(194, 24, 91, 0.4) !important;
                color: #fff !important; padding: 6px 16px !important; border-radius: 8px !important; cursor: pointer !important;
                font-family: 'Inter', sans-serif !important; font-weight: 500 !important; transition: all 0.2s !important;
            }
            .vakra-board-close:hover { background: #C2185B !important; box-shadow: 0 0 15px rgba(194, 24, 91, 0.5) !important; }
        `;
        document.head.appendChild(boardStyles);

        const boardContainer = document.createElement('div');
        boardContainer.innerHTML = `
            <div id="whiteboardTrigger" title="Launch Vakratron Design Suite">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width: 26px !important; height: 26px !important; color: #C2185B !important; display: block !important;">
                    <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>
                    <polyline points="2 17 12 22 22 17"></polyline>
                    <polyline points="2 12 12 17 22 12"></polyline>
                </svg>
            </div>
            
            <div class="vakra-board-overlay" id="vakraBoardModal">
                <div class="vakra-board-header">
                    <div style="display: flex; align-items: center; gap: 14px;">
                        <h3 style="margin: 0 !important; font-size: 1.2rem !important; font-weight: 600 !important; letter-spacing: -0.01em; color: #ffffff !important;">
                            VAKRATRON DESIGN SUITE <span style="font-size: 0.75rem; color: #C2185B; font-weight: 400; letter-spacing: 0.1em; margin-left: 8px; vertical-align: middle;">[ INFRASTRUCTURE SANDBOX v2.0 ]</span>
                        </h3>
                    </div>
                    <button class="vakra-board-close" id="closeBoardBtn">Close Console ✕</button>
                </div>
                
                <div style="flex: 1 !important; width: 100% !important; background: #1a1a1a !important; position: relative;">
                    <iframe 
                        id="vakraIframeApp"
                        style="width: 100%; height: 100%; border: none; display: block;"
                        src="https://embed.diagrams.net/?embed=1&ui=dark&spin=0&modified=unsaved&proto=json&libraries=1"
                    >
                    </iframe>
                </div>
                
                <div class="vakra-board-footer">
                    <div>© 2026 VAKRATRON SYSTEMS. ALL RIGHTS RESERVED. SECURE INDUSTRIAL KERNEL.</div>
                    <div style="font-weight: 600; color: #475569;">VAKRATRON TOOLS CORE <span style="color: rgba(194, 24, 91, 0.6);">|</span> POWERED BY DRAW.IO</div>
                </div>
            </div>
        `;
        document.body.appendChild(boardContainer);

        const trigger = document.getElementById('whiteboardTrigger');
        const modal = document.getElementById('vakraBoardModal');
        const closeBtn = document.getElementById('closeBoardBtn');

        trigger.onclick = function(e) {
            e.preventDefault();
            modal.style.setProperty('display', 'flex', 'important');
            document.body.style.overflow = 'hidden'; 
        };

        closeBtn.onclick = function(e) {
            e.preventDefault();
            modal.style.setProperty('display', 'none', 'important');
            document.body.style.overflow = 'auto'; 
        };

        // 📡 ACTIVE INTERCEPTOR DATA LINK ENGINE
        window.addEventListener('message', function(evt) {
            if (evt.origin === 'https://embed.diagrams.net') {
                try {
                    const data = JSON.parse(evt.data);
                    
                    if (data.event === 'init') {
                        const iframe = document.getElementById('vakraIframeApp');
                        iframe.contentWindow.postMessage(JSON.stringify({
                            action: 'load',
                            autosave: 1,
                            xml: '<mxGraphModel><root><mxCell id="0"/><mxCell id="1" parent="0"/></root></mxGraphModel>'
                        }), 'https://embed.diagrams.net');
                    }
                    
                    if (data.event === 'save') {
                        const blob = new Blob([data.xml], { type: 'text/xml' });
                        const a = document.createElement('a');
                        a.href = URL.createObjectURL(blob);
                        a.download = 'Vakratron_Topology_Draft.xml';
                        a.click();
                    }
                } catch (e) {
                    // Suppress JSON string parsing error noise
                }
            }
        });
    }

    // ==========================================
    // INITIALIZATION RUNTIME
    // ==========================================
    if (document.body) {
        initVakraWidget();
        initVakraWhiteboard();
    } else {
        window.addEventListener('DOMContentLoaded', () => {
            initVakraWidget();
            initVakraWhiteboard();
        });
    }
})();