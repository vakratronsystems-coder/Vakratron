// 🦾 VAKRATRON CYBER AI INFRASTRUCTURE WIDGET - GLOBAL COMPONENT
(() => {
    function initVakraWidget() {
        // 🔒 EXCLUDE DESK: Agar current page contact.html hai, toh execution block kar do
        if (window.location.pathname.includes('contact.html')) {
            return; 
        }

        // Guardrail: Double injection block check
        if (document.getElementById('chatTrigger')) return;

        // 1. Inject Styles Matrix into Head
        const chatStyles = document.createElement('style');
        chatStyles.innerHTML = `
            #chatTrigger {
                position: fixed !important; bottom: 30px !important; right: 30px !important;
                width: 60px !important; height: 60px !important; min-width: 60px !important; min-height: 60px !important; max-width: 60px !important; max-height: 60px !important;
                border-radius: 50% !important; background: linear-gradient(135deg, #C2185B 0%, #9d174d 100%) !important;
                box-shadow: 0 4px 25px rgba(194, 24, 91, 0.5) !important; border: 1px solid rgba(255,255,255,0.2) !important;
                cursor: pointer !important; z-index: 99999991 !important; display: flex !important; align-items: center !important; justify-content: center !important;
                padding: 0 !important; margin: 0 !important; transform: none !important; transition: all 0.2s ease-in-out !important;
            }
            #chatTrigger:hover { transform: scale(1.08) !important; box-shadow: 0 6px 30px rgba(194, 24, 91, 0.7) !important; }
            .vakra-chat-window {
                position: fixed !important; bottom: 105px !important; right: 30px !important;
                width: 360px !important; height: 500px !important; min-width: 360px !important; min-height: 500px !important; max-width: 360px !important; max-height: 500px !important;
                flex-basis: 360px !important; flex-grow: 0 !important; flex-shrink: 0 !important; display: none !important; flex-direction: column !important;
                background: rgba(15, 23, 42, 0.98) !important; backdrop-filter: blur(20px) !important; -webkit-backdrop-filter: blur(20px) !important;
                border: 1px solid rgba(194, 24, 91, 0.5) !important; box-shadow: 0 20px 50px rgba(0,0,0,0.9), 0 0 40px rgba(194, 24, 91, 0.2) !important;
                border-radius: 20px !important; z-index: 99999992 !important; overflow: hidden !important; box-sizing: border-box !important;
                margin: 0 !important; padding: 0 !important; left: auto !important; top: auto !important; transform: none !important;
            }
            .vakra-chat-window.active { display: flex !important; opacity: 1 !important; pointer-events: auto !important; }
            .vakra-chat-header { background: rgba(194, 24, 91, 0.2) !important; border-bottom: 1px solid rgba(194, 24, 91, 0.4) !important; padding: 15px 20px !important; display: flex !important; align-items: center !important; justify-content: space-between !important; flex-shrink: 0 !important; }
            .vakra-chat-header h3 { margin: 0 !important; font-family: 'Poppins', sans-serif !important; font-size: 1.05rem !important; font-weight: 600 !important; color: #fff !important; display: flex !important; align-items: center !important; gap: 10px !important; }
            .vakra-chat-header h3 span { width: 8px !important; height: 8px !important; background: #10b981 !important; border-radius: 50% !important; display: inline-block !important; box-shadow: 0 0 8px #10b981 !important; }
            .vakra-chat-close { background: transparent !important; border: none !important; color: #94a3b8 !important; cursor: pointer !important; font-size: 1.1rem !important; }
            .vakra-chat-messages { flex: 1 !important; padding: 20px !important; overflow-y: auto !important; display: flex !important; flex-direction: column !important; gap: 15px !important; background: rgba(2, 6, 23, 0.4) !important; }
            .vakra-msg { max-width: 85% !important; padding: 12px 16px !important; border-radius: 14px !important; font-size: 0.92rem !important; line-height: 1.5 !important; word-wrap: break-word !important; box-sizing: border-box !important; }
            .vakra-msg.system { background: rgba(30, 41, 59, 0.7) !important; border: 1px solid rgba(255, 255, 255, 0.08) !important; color: #e2e8f0 !important; align-self: flex-start !important; border-top-left-radius: 2px !important; }
            .vakra-msg.user { background: linear-gradient(135deg, #C2185B 0%, #9d174d 100%) !important; border: 1px solid rgba(194, 24, 91, 0.4) !important; color: #fff !important; align-self: flex-end !important; border-top-right-radius: 2px !important; }
            .vakra-chat-input-area { padding: 15px 20px !important; border-top: 1px solid rgba(255, 255, 255, 0.08) !important; background: #0f172a !important; display: flex !important; gap: 10px !important; align-items: center !important; flex-shrink: 0 !important; }
            .vakra-chat-input { flex: 1 !important; background: rgba(2, 6, 23, 0.8) !important; border: 1px solid rgba(255, 255, 255, 0.1) !important; border-radius: 10px !important; padding: 12px !important; color: #fff !important; font-size: 0.9rem !important; outline: none !important; font-family: 'Inter', sans-serif !important; box-sizing: border-box !important; }
            .vakra-chat-input:focus { border-color: #38bdf8 !important; }
            .vakra-chat-send { background: rgba(56, 189, 248, 0.1) !important; border: 1px solid rgba(56, 189, 248, 0.3) !important; color: #38bdf8 !important; width: 44px !important; height: 44px !important; border-radius: 10px !important; display: flex !important; align-items: center !important; justify-content: center !important; cursor: pointer !important; flex-shrink: 0 !important; }
            .vakra-chat-send:hover { background: #38bdf8 !important; color: #020617 !important; box-shadow: 0 0 15px rgba(56, 189, 248, 0.4) !important; }
            .vakra-typing { display: flex; gap: 4px; padding: 5px 0; align-items: center; }
            .vakra-typing span { width: 6px; height: 6px; background: #94a3b8; border-radius: 50%; animation: vakraBounce 1.4s infinite ease-in-out both; }
            .vakra-typing span:nth-child(1) { animation-delay: -0.32s; }
            .vakra-typing span:nth-child(2) { animation-delay: -0.16s; }
            @keyframes vakraBounce { 0%, 80%, 100% { transform: scale(0); } 40% { transform: scale(1.0); } }
        `;
        document.head.appendChild(chatStyles);

        // 2. Inject HTML Elements Dynamic Structure into Body
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

        // 3. Bind Active Control Scripts Engine Logic
        const trigger = document.getElementById('chatTrigger');
        const windowEl = document.getElementById('chatWindow');
        const closeBtn = document.getElementById('chatClose');
        const sendBtn = document.getElementById('chatSend');
        const inputEl = document.getElementById('chatInput');
        const messagesContainer = document.getElementById('chatMessages');

        // BIND EVENT DIRECTLY FOR MAX PERFORMANCE (No framework event hijacking)
        trigger.onclick = function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            if (windowEl.style.display === 'flex') {
                windowEl.classList.remove('active');
                windowEl.style.setProperty('display', 'none', 'important');
            } else {
                windowEl.classList.add('active');
                windowEl.style.setProperty('display', 'flex', 'important');
                windowEl.style.setProperty('width', '360px', 'important');
                inputEl.focus();
            }
        };

        closeBtn.onclick = function(e) {
            e.preventDefault();
            e.stopPropagation();
            windowEl.classList.remove('active');
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
                    if (lowerMessage.includes('connect') || lowerMessage.includes('talk to human') || lowerMessage.includes('contact team') || lowerMessage.includes('representative') || lowerMessage.includes('connect someone') || lowerMessage.includes('team se connect')) {
                        setTimeout(() => {
                            appendBubble("⚡ System Action: Redirecting token matrix to the Sovereign Advisory Desk...", 'system');
                            setTimeout(() => {
                                window.location.href = 'contact.html';
                            }, 1500);
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

    // 🚀 ULTRA TRIGGER STATE: Execute instantly or wait if body is building
    if (document.body) {
        initVakraWidget();
    } else {
        window.addEventListener('DOMContentLoaded', initVakraWidget);
    }
})();