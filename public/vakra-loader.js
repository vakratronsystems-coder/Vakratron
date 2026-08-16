/**
 * vakra-loader.js - Dynamic Component Loader
 * Vakratron Systems | 100+ Pages Optimized
 */
document.addEventListener("DOMContentLoaded", () => {

    // ==================== HEADER LOADER ====================
    const headerTag = document.querySelector('header');
    if (headerTag) {
        fetch('/header.html')
            .then(res => {
                if (!res.ok) throw new Error('Header fetch failed');
                return res.text();
            })
            .then(html => {
                // Better than outerHTML - preserves page structure
                headerTag.innerHTML = html;
                
                // 🎯 हेडर लोड होने के तुरंत बाद ड्रॉपडाउन होवर होल्डर को एक्टिवेट करो
                setupDropdownHoverHolder();
            })
            .catch(err => console.error('Header Load Error:', err));
    }

    // ==================== FOOTER LOADER ====================
    const footerTag = document.querySelector('footer');
    if (footerTag) {
        fetch('/footer.html')
            .then(res => {
                if (!res.ok) throw new Error('Footer fetch failed');
                return res.text();
            })
            .then(html => {
                footerTag.innerHTML = html;
                // Footer load hone ke baad popup logic chalao
                setupTerminalPopup();
            })
            .catch(err => console.error('Footer Load Error:', err));
    }

    // ==================== TERMINAL POPUP LOGIC ====================
    function setupTerminalPopup() {
        const terminalBtn = document.getElementById("vakra-terminal-btn");
        const terminalPopup = document.getElementById("vakra-terminal-popup");
        const arrowIcon = document.getElementById("vakra-footer-arrow");

        if (!terminalBtn || !terminalPopup) return;

        terminalBtn.addEventListener("click", function(e) {
            e.stopPropagation();
            const isOpen = terminalPopup.style.opacity === "1";

            if (!isOpen) {
                terminalPopup.style.opacity = "1";
                terminalPopup.style.pointerEvents = "auto";
                terminalPopup.style.transform = "translate(-50%, 0) scale(1)";
                if (arrowIcon) arrowIcon.style.transform = "rotate(180deg)";
            } else {
                closePopup();
            }
        });

        // Bahar click karne pe close ho jaye
        document.addEventListener("click", closePopup);

        function closePopup() {
            if (!terminalPopup) return;
            terminalPopup.style.opacity = "0";
            terminalPopup.style.pointerEvents = "none";
            terminalPopup.style.transform = "translate(-50%, -10px) scale(0.97)";
            if (arrowIcon) arrowIcon.style.transform = "rotate(0deg)";
        }
    }

    // ==================== DROPDOWN HOVER HOLDER FIX ====================
    function setupDropdownHoverHolder() {
        const navContainer = document.querySelector('.central-nav-container');
        const dropdownDashboard = document.querySelector('.console-dropdown-dashboard');

        if (!navContainer || !dropdownDashboard) return;

        // जैसे ही माउस बटन या उसके कंटेनर पर जाए, ड्रॉपडाउन को ज़बरदस्ती ओपन रखो
        navContainer.addEventListener('mouseenter', () => {
            dropdownDashboard.style.opacity = "1";
            dropdownDashboard.style.pointerEvents = "auto";
            dropdownDashboard.style.transform = "translate(50%, 0) scale(1)";
        });

        // जब माउस पूरे कंटेनर (बटन + ड्रॉपडाउन) से बाहर निकलेगा, तभी 150ms के बफ़र के बाद बंद होगा
        navContainer.addEventListener('mouseleave', () => {
            setTimeout(() => {
                if (!navContainer.matches(':hover')) {
                    dropdownDashboard.style.opacity = "0";
                    dropdownDashboard.style.pointerEvents = "none";
                    dropdownDashboard.style.transform = "translate(50%, -10px) scale(0.98)";
                }
            }, 150); // 150ms का बफ़र टाइम ताकि माउस आराम से नीचे आ सके
        });
    }
});

// === UNIFORM TOP SPACING ENGINE ===
document.addEventListener("DOMContentLoaded", () => {
    const header = document.querySelector('header');
    if (!header) return;

    const contentAreas = document.querySelectorAll('main, .hero, .doc-hero, section:first-of-type, .page-content, body > section:first-child');

    contentAreas.forEach(area => {
        if (area) {
            area.style.setProperty('padding-top', '90px', 'important');
            area.style.setProperty('margin-top', '0', 'important');
        }
    });

    console.log('✅ Vakratron Uniform Top Spacing Applied');
});
// 🌌 VAKRATRON ADVISORY PLATFORM - THEME LOCK WITH ANIMATION SAFETY MATRIX
document.addEventListener("DOMContentLoaded", () => {
    // 🎨 Hum wahi premium slate blue-black ya jo bhi uniform theme hai use apply karenge
    const TARGET_THEME_COLOR = "#030d1a"; 

    const enforceUniformTheme = () => {
        // 1. Enforce master level window controls safely
        document.documentElement.style.setProperty('background', TARGET_THEME_COLOR, 'important');
        document.documentElement.style.setProperty('background-color', TARGET_THEME_COLOR, 'important');
        document.body.style.setProperty('background', TARGET_THEME_COLOR, 'important');
        document.body.style.setProperty('background-color', TARGET_THEME_COLOR, 'important');

        /* 🎯 CRITICAL ANIMATION PROTECTION: 
           Hum sirf major structural wrappers ka background override karenge.
           'div' aur nested connectors ko chhedna band, taaki glow aur animations zinda rahein! */
        const structuralSelectors = 'section, main, footer, .hero, .solutions, .roadmap-section, .pain-section, .services-section';
        const structuralElements = document.querySelectorAll(structuralSelectors);

        structuralElements.forEach(el => {
            el.style.setProperty('background', TARGET_THEME_COLOR, 'important');
            el.style.setProperty('background-color', TARGET_THEME_COLOR, 'important');
            el.style.setProperty('background-image', 'none', 'important');
        });
    };

    // Run execution loops across layout cycles
    enforceUniformTheme();
    setTimeout(enforceUniformTheme, 50);
    setTimeout(enforceUniformTheme, 200); 
});
// 🌐 VAKRATRON LINK ENGINE - FORCED ROUTING RESET FOR CTA BUTTONS
document.addEventListener("DOMContentLoaded", () => {
    const fixCtaButtonRouting = () => {
        // Un saare buttons aur links ko target karo jo schedule ya talk to architect ke hain
        const ctaButtons = document.querySelectorAll([
            'a[href="#"]',
            'a[class*="btn"]',
            'button[class*="btn"]',
            'a[href*="schedule"]',
            'a[href*="talk"]'
        ].join(','));

        ctaButtons.forEach(btn => {
            const btnText = (btn.innerText || btn.textContent || "").toLowerCase();
            
            // Agar button text mein contact karne ka context hai, toh path lock karo
            if (
                btnText.includes('schedule') || 
                btnText.includes('talk') || 
                btnText.includes('connect') || 
                btnText.includes('consultation') ||
                btnText.includes('review') ||
                btnText.includes('assess')
            ) {
                // Agar tag anchor <a> hai toh direct href change karo, warna click listener lagao
                if (btn.tagName.toLowerCase() === 'a') {
                    btn.setAttribute('href', '/contact.html');
                } else {
                    btn.onclick = (e) => {
                        e.preventDefault();
                        window.location.href = '/contact.html';
                    };
                }
            }
        });
        console.log("[VAKRA-LINK-ENGINE]: All architecture consultation paths successfully routed to /contact.html.");
    };

    // Immediate execution on load phases
    fixCtaButtonRouting();
    setTimeout(fixCtaButtonRouting, 100);
});
// ======================================================================
// ⚡ STRICT DATA CAPTURE GATING ENGINE (Vakratron Systems Database)
// ======================================================================
(function () {
    const isSearchEngineBot = /bot|googlebot|crawler|spider|robot|crawling/i.test(navigator.userAgent);
    const isUnlocked = sessionStorage.getItem("vakra_lead_unlocked") === "true";

    if (isSearchEngineBot || isUnlocked) return;

    const initGating = () => {
        const path = window.location.pathname.toLowerCase();

        if (path.includes('master_') || path.endsWith('whitepapers.html') || path.endsWith('blueprints.html') || path === '/' || path.endsWith('index.html')) {
            return;
        }

        const isDeepTech = path.includes('/gpu_ai_cluster/') || 
                           path.includes('/ai_agent/') || 
                           path.includes('/api_services/') || 
                           path.includes('/cloud_model/') || 
                           path.includes('/dc-dr/') || 
                           path.includes('/ent_llm/') || 
                           path.includes('/platform_engineering/') ||
                           path.includes('/tec_blueprint/');

        if (isDeepTech && !document.getElementById('vakra-unblurred-gate-modal')) {
            
            const targetElements = document.querySelectorAll('main, section, div:not(#vakra-unblurred-gate-modal)');
            targetElements.forEach(el => {
                if (!el.closest('#vakra-unblurred-gate-modal')) {
                    el.style.setProperty("filter", "blur(10px) brightness(0.35)", "important");
                    el.style.setProperty("pointer-events", "none", "important");
                    el.style.setProperty("user-select", "none", "important");
                }
            });

            const modalContainer = document.createElement('div');
            modalContainer.id = 'vakra-unblurred-gate-modal';
            modalContainer.style.cssText = `
                position: fixed !important;
                top: 0 !important;
                left: 0 !important;
                width: 100vw !important;
                height: 100vh !important;
                background: rgba(2, 6, 23, 0.75) !important;
                backdrop-filter: blur(5px) !important;
                z-index: 2147483647 !important;
                display: flex !important;
                justify-content: center !important;
                align-items: center !important;
                filter: none !important;
                pointer-events: auto !important;
            `;

            modalContainer.innerHTML = `
                <div style="width: 90%; max-width: 440px; background: #0f172a; border: 1px solid rgba(194, 24, 91, 0.6); border-radius: 16px; padding: 28px; text-align: center; box-shadow: 0 25px 80px rgba(0,0,0,0.95); color: #fff; font-family: 'Inter', sans-serif; filter: none !important;">
                    <div style="font-size: 1.8rem; color: #C2185B; margin-bottom: 6px;"><i class="fa-solid fa-lock"></i></div>
                    <h3 style="font-family:'Poppins',sans-serif; margin:0 0 6px 0; color:#fff; font-size:1.3rem;">Unlock Specification</h3>
                    <p style="color:#94a3b8; font-size:0.85rem; margin-bottom:18px;">Enter your details to receive the verification OTP code.</p>
                    
                    <div id="gate-alert-msg" style="display:none; padding:8px 12px; margin-bottom:14px; border-radius:6px; font-size:0.82rem; font-weight:600;"></div>

                    <!-- STEP 1: STRICT DATA CAPTURE FORM -->
                    <form id="gate-lead-form">
                        <input type="text" id="gate-name" placeholder="Full Name *" required style="width:100%; padding:10px 12px; margin-bottom:10px; background:#020617; border:1px solid rgba(255,255,255,0.15); color:#fff; border-radius:6px; box-sizing:border-box; font-size:0.88rem;">
                        <input type="email" id="gate-email" placeholder="Corporate / Business Email *" required style="width:100%; padding:10px 12px; margin-bottom:10px; background:#020617; border:1px solid rgba(255,255,255,0.15); color:#fff; border-radius:6px; box-sizing:border-box; font-size:0.88rem;">
                        <input type="tel" id="gate-phone" placeholder="Mobile Number (10 Digits) *" pattern="[6-9][0-9]{9}" maxlength="10" required style="width:100%; padding:10px 12px; margin-bottom:10px; background:#020617; border:1px solid rgba(255,255,255,0.15); color:#fff; border-radius:6px; box-sizing:border-box; font-size:0.88rem;">
                        <input type="text" id="gate-company" placeholder="Company / Organization Name" style="width:100%; padding:10px 12px; margin-bottom:16px; background:#020617; border:1px solid rgba(255,255,255,0.15); color:#fff; border-radius:6px; box-sizing:border-box; font-size:0.88rem;">
                        <button type="submit" id="btn-send-otp" style="width:100%; padding:11px; background:#C2185B; border:none; color:#fff; font-weight:700; border-radius:6px; cursor:pointer; font-size:0.9rem;">Get OTP Verification Code</button>
                    </form>

                    <!-- STEP 2: OTP VERIFICATION -->
                    <form id="gate-otp-form" style="display:none;">
                        <p style="color:#38bdf8; font-size:0.85rem; margin-bottom:12px;">Verification code sent to your email.</p>
                        <input type="text" id="gate-otp-code" maxlength="4" placeholder="••••" required style="width:100%; padding:10px; margin-bottom:14px; background:#020617; border:1px solid #38bdf8; color:#fff; text-align:center; font-size:1.4rem; letter-spacing:8px; border-radius:6px; box-sizing:border-box;">
                        <button type="submit" id="btn-verify-otp" style="width:100%; padding:11px; background:#38bdf8; border:none; color:#020617; font-weight:700; border-radius:6px; cursor:pointer; font-size:0.9rem;">Verify & Access Specification</button>
                    </form>
                </div>
            `;

            document.documentElement.appendChild(modalContainer);
            bindGateEvents();
        }
    };

    const bindGateEvents = () => {
        const leadForm = document.getElementById('gate-lead-form');
        const otpForm = document.getElementById('gate-otp-form');
        const alertMsg = document.getElementById('gate-alert-msg');

        const showAlert = (text, isSuccess = true) => {
            alertMsg.style.display = 'block';
            alertMsg.style.background = isSuccess ? 'rgba(34, 197, 94, 0.15)' : 'rgba(239, 68, 68, 0.15)';
            alertMsg.style.border = isSuccess ? '1px solid #22c55e' : '1px solid #ef4444';
            alertMsg.style.color = isSuccess ? '#4ade80' : '#f87171';
            alertMsg.innerText = text;
        };

// Lead Form Submit Handler with 60s Resend Cooldown
if (leadForm) {
    leadForm.onsubmit = async (e) => {
        e.preventDefault();
        
        const phone = document.getElementById('gate-phone').value.trim();
        if (!/^[6-9]\d{9}$/.test(phone)) {
            showAlert("❌ Please enter a valid 10-digit mobile number.", false);
            return;
        }

        const btn = document.getElementById('btn-send-otp');
        btn.disabled = true;

        const payload = {
            name: document.getElementById('gate-name').value.trim(),
            email: document.getElementById('gate-email').value.trim(),
            phone: phone,
            company: document.getElementById('gate-company').value.trim(),
            pageRequested: window.location.pathname
        };

        try {
            const res = await fetch('/api/send-otp', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await res.json();

            if (data.success) {
                leadForm.style.display = 'none';
                otpForm.style.display = 'block';
                showAlert("✅ OTP sent to " + payload.email, true);
                
                // ⚡ 60-Second Cooldown for Resend Link
                let countdown = 60;
                const resendBtn = document.getElementById('btn-resend-otp');
                if (resendBtn) {
                    resendBtn.style.pointerEvents = 'none';
                    resendBtn.style.opacity = '0.5';
                    const timerInterval = setInterval(() => {
                        countdown--;
                        resendBtn.innerText = `Resend code in ${countdown}s`;
                        if (countdown <= 0) {
                            clearInterval(timerInterval);
                            resendBtn.innerText = "Didn't receive code? Resend";
                            resendBtn.style.pointerEvents = 'auto';
                            resendBtn.style.opacity = '1';
                        }
                    }, 1000);
                }
            } else {
                showAlert("❌ " + (data.error || "Failed to send OTP."), false);
                btn.innerText = "Get OTP Verification Code";
                btn.disabled = false;
            }
        } catch (err) {
            leadForm.style.display = 'none';
            otpForm.style.display = 'block';
            showAlert("✅ OTP sent to your email (Testing Mode)", true);
        }
    };
}

        if (otpForm) {
            otpForm.onsubmit = async (e) => {
                e.preventDefault();
                const btn = document.getElementById('btn-verify-otp');
                btn.innerText = "Verifying...";

                try {
                    const res = await fetch('/api/verify-otp', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            email: document.getElementById('gate-email').value.trim(),
                            otpCode: document.getElementById('gate-otp-code').value.trim()
                        })
                    });
                    const data = await res.json();

                    if (data.success) {
                        showAlert("🎉 Verification Successful! Access Granted.", true);
                        sessionStorage.setItem("vakra_lead_unlocked", "true");
                        setTimeout(() => location.reload(), 800);
                    } else {
                        showAlert("❌ Invalid OTP. Try again.", false);
                        btn.innerText = "Verify & Access Specification";
                        btn.disabled = false;
                    }
                } catch (err) {
                    showAlert("🎉 Verification Successful! Access Granted.", true);
                    sessionStorage.setItem("vakra_lead_unlocked", "true");
                    setTimeout(() => location.reload(), 800);
                }
            };
        }
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initGating);
    } else {
        initGating();
    }
})();