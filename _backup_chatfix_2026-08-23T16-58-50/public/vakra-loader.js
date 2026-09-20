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
            // ⛔ Never hijack controls that belong to the consultation form.
            // This engine matches button[class*="btn"] + text containing
            // "consultation", which is exactly our submit button — it was
            // redirecting to /contact.html instead of letting the form post,
            // so every enquiry from these pages was silently lost.
            if (btn.closest && btn.closest('#vakra-consult-cta')) return;

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
// ⚡ DEEP-TECH CONSULTATION CTA  (replaces the old blur/OTP gate)
// ----------------------------------------------------------------------
// WHY THE GATE WAS REMOVED:
//
// 1. COST — every gate submission fired an OTP email, and every verify
//    fired another. Bots were burning the monthly email quota. With the
//    gate gone, ZERO OTP emails are sent; only a genuine enquiry sends
//    one notification to you.
//
// 2. IT NEVER ACTUALLY BLOCKED ANYONE — the page content sat fully in the
//    DOM behind a CSS blur, and both catch-blocks GRANTED access on any
//    network error (`sessionStorage.setItem("vakra_lead_unlocked","true")`).
//    Anyone could get in by going offline for a second.
//
// 3. IT SNIFFED USER-AGENTS to let Googlebot past the gate while showing
//    humans a wall. That is cloaking, against Google's Search Essentials,
//    and risks the whole domain being removed from search.
//
// What replaces it: content is open to everyone, and a non-blocking
// consultation card is appended at the END of deep-tech pages. Readers who
// found the material useful convert far better than readers forced to pay
// with their phone number before seeing a word.
// ======================================================================
(function () {
    const DEEP_TECH_PATHS = [
        '/gpu_ai_cluster/', '/ai_agent/', '/api_services/', '/cloud_model/',
        '/dc-dr/', '/ent_llm/', '/platform_engineering/', '/tec_blueprint/'
    ];

    const initConsultCta = () => {
        const path = window.location.pathname.toLowerCase();

        // Skip index / hub pages — they already carry their own CTAs
        if (path === '/' || path.endsWith('index.html') ||
            path.includes('master_') ||
            path.endsWith('whitepapers.html') || path.endsWith('blueprints.html')) {
            return;
        }

        if (!DEEP_TECH_PATHS.some(p => path.includes(p))) return;
        if (document.getElementById('vakra-consult-cta')) return;

        injectCtaStyles();

        // NOTE: this is a <div>, deliberately NOT a <section>.
        // The THEME LOCK block above force-overrides the background of every
        // <section> with !important, and the SPACING ENGINE adds 90px padding
        // to `section:first-of-type`. A <div> stays clear of both.
        const card = document.createElement('div');
        card.id = 'vakra-consult-cta';

        card.innerHTML = `
            <div class="vk-cta-card">
                <div class="vk-cta-accent"></div>
                <h3 class="vk-cta-title">Want this mapped to your own environment?</h3>
                <p class="vk-cta-sub">
                    Share a few details and our Principal Solutions Architect will come back with a
                    sizing view, HLD outline or BoQ direction for your specific workload. No obligation.
                </p>

                <div id="vakra-cta-alert" class="vk-cta-alert"></div>

                <form id="vakra-cta-form" novalidate>
                    <!-- 🐝 HONEYPOT: invisible to humans, irresistible to bots -->
                    <input type="text" name="website" id="vakra-cta-website" tabindex="-1"
                           autocomplete="off" aria-hidden="true" class="vk-cta-hp">
                    <!-- ⏱️ TIMING TRAP: humans never submit within 3 seconds of load -->
                    <input type="hidden" id="vakra-cta-loadedat" value="">

                    <div class="vk-cta-grid">
                        <input type="text"  id="vakra-cta-name"    class="vk-cta-input" placeholder="Full Name *" required>
                        <input type="email" id="vakra-cta-email"   class="vk-cta-input" placeholder="Email *" required>
                        <input type="tel"   id="vakra-cta-phone"   class="vk-cta-input" placeholder="Phone with country code *" required>
                        <input type="text"  id="vakra-cta-company" class="vk-cta-input" placeholder="Company / Organization">
                    </div>

                    <button type="submit" id="vakra-cta-btn" class="vk-cta-submit">Request Consultation</button>
                    <p class="vk-cta-note">We usually reply within one business day.</p>
                </form>
            </div>
        `;

        // PLACEMENT: always immediately BEFORE the footer.
        // The earlier build appended to `main || body`; on pages without a
        // <main> tag that dropped the card *below* the footer.
        const footer = document.querySelector('footer');
        const main = document.querySelector('main');

        if (footer && footer.parentNode) {
            footer.parentNode.insertBefore(card, footer);
        } else if (main) {
            main.appendChild(card);
        } else {
            document.body.appendChild(card);
        }

        // Stamp load time for the timing trap
        const loadedAt = document.getElementById('vakra-cta-loadedat');
        if (loadedAt) loadedAt.value = String(Date.now());

        bindCtaForm();
    };

    const injectCtaStyles = () => {
        if (document.getElementById('vakra-cta-styles')) return;
        const style = document.createElement('style');
        style.id = 'vakra-cta-styles';
        style.textContent = `
            #vakra-consult-cta {
                display: block;
                width: 100%;
                padding: 0 20px 64px 20px;
                box-sizing: border-box;
                font-family: 'Inter', system-ui, -apple-system, sans-serif;
            }
            #vakra-consult-cta .vk-cta-card {
                position: relative;
                max-width: 720px;
                margin: 0 auto;
                padding: 34px 32px 28px 32px;
                background: #0b1425;
                border: 1px solid rgba(148, 163, 184, 0.14);
                border-radius: 18px;
                box-shadow: 0 18px 50px rgba(0, 0, 0, 0.45);
                overflow: hidden;
                box-sizing: border-box;
            }
            #vakra-consult-cta .vk-cta-accent {
                position: absolute;
                top: 0; left: 0; right: 0;
                height: 3px;
                background: linear-gradient(90deg, #C2185B, #38bdf8);
            }
            #vakra-consult-cta .vk-cta-title {
                font-family: 'Poppins', 'Inter', sans-serif;
                margin: 0 0 8px 0;
                color: #f8fafc;
                font-size: 1.3rem;
                line-height: 1.35;
                font-weight: 600;
            }
            #vakra-consult-cta .vk-cta-sub {
                color: #94a3b8;
                font-size: 0.9rem;
                line-height: 1.6;
                margin: 0 0 22px 0;
            }
            #vakra-consult-cta .vk-cta-alert {
                display: none;
                padding: 10px 13px;
                margin-bottom: 16px;
                border-radius: 8px;
                font-size: 0.83rem;
                font-weight: 600;
            }
            #vakra-consult-cta .vk-cta-hp {
                position: absolute !important;
                left: -9999px !important;
                opacity: 0 !important;
                height: 0 !important;
                width: 0 !important;
                pointer-events: none !important;
            }
            #vakra-consult-cta .vk-cta-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 12px;
            }
            #vakra-consult-cta .vk-cta-input {
                width: 100%;
                padding: 12px 14px;
                background: #020617;
                border: 1px solid rgba(148, 163, 184, 0.18);
                color: #f1f5f9;
                border-radius: 9px;
                font-size: 0.9rem;
                font-family: inherit;
                box-sizing: border-box;
                transition: border-color .18s ease, box-shadow .18s ease;
                outline: none;
            }
            #vakra-consult-cta .vk-cta-input::placeholder { color: #64748b; }
            #vakra-consult-cta .vk-cta-input:focus {
                border-color: #C2185B;
                box-shadow: 0 0 0 3px rgba(194, 24, 91, 0.16);
            }
            #vakra-consult-cta .vk-cta-submit {
                width: 100%;
                margin-top: 16px;
                padding: 13px;
                background: linear-gradient(135deg, #C2185B, #9d1449);
                border: none;
                color: #fff;
                font-family: inherit;
                font-weight: 700;
                font-size: 0.94rem;
                border-radius: 9px;
                cursor: pointer;
                transition: transform .15s ease, box-shadow .15s ease, opacity .15s ease;
            }
            #vakra-consult-cta .vk-cta-submit:hover:not(:disabled) {
                transform: translateY(-1px);
                box-shadow: 0 10px 26px rgba(194, 24, 91, 0.32);
            }
            #vakra-consult-cta .vk-cta-submit:disabled { opacity: .6; cursor: not-allowed; }
            #vakra-consult-cta .vk-cta-note {
                text-align: center;
                color: #64748b;
                font-size: 0.76rem;
                margin: 12px 0 0 0;
            }
            @media (max-width: 640px) {
                #vakra-consult-cta { padding: 0 16px 48px 16px; }
                #vakra-consult-cta .vk-cta-card { padding: 26px 20px 22px 20px; border-radius: 14px; }
                #vakra-consult-cta .vk-cta-title { font-size: 1.15rem; }
                #vakra-consult-cta .vk-cta-grid { grid-template-columns: 1fr; }
            }
        `;
        document.head.appendChild(style);
    };

    const bindCtaForm = () => {
        const form = document.getElementById('vakra-cta-form');
        const alertBox = document.getElementById('vakra-cta-alert');
        if (!form || !alertBox) return;

        const showAlert = (text, isSuccess = true) => {
            alertBox.style.display = 'block';
            alertBox.style.background = isSuccess ? 'rgba(34, 197, 94, 0.15)' : 'rgba(239, 68, 68, 0.15)';
            alertBox.style.border = isSuccess ? '1px solid #22c55e' : '1px solid #ef4444';
            alertBox.style.color = isSuccess ? '#4ade80' : '#f87171';
            alertBox.innerText = text;
        };

        form.onsubmit = async (e) => {
            e.preventDefault();

            const btn = document.getElementById('vakra-cta-btn');
            const name = document.getElementById('vakra-cta-name').value.trim();
            const email = document.getElementById('vakra-cta-email').value.trim();
            const phone = document.getElementById('vakra-cta-phone').value.trim();
            const company = document.getElementById('vakra-cta-company').value.trim();

            if (!name || !email || !phone) {
                showAlert('Please fill in your name, email and phone.', false);
                return;
            }

            // Digits only, 7–15 — matches the server's global rule.
            // The old form used /^[6-9]\d{9}$/ which silently rejected every
            // non-Indian number, i.e. every international enquiry.
            const digits = phone.replace(/\D/g, '');
            if (digits.length < 7 || digits.length > 15) {
                showAlert('Please enter a valid phone number with country code.', false);
                return;
            }

            btn.disabled = true;
            const originalLabel = btn.innerText;
            btn.innerText = 'Sending…';

            const payload = {
                name,
                email,
                phone,
                company,
                reason: 'Consultation request — ' + window.location.pathname,
                // Bot traps travel with the payload
                website: document.getElementById('vakra-cta-website').value,
                formLoadedAt: document.getElementById('vakra-cta-loadedat').value
            };

            try {
                const res = await fetch('/api/contact', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();

                if (data && data.success) {
                    form.style.display = 'none';
                    showAlert('✅ Thank you — we will get back to you shortly.', true);
                } else {
                    showAlert('❌ ' + ((data && data.error) || 'Could not send. Please try again.'), false);
                    btn.innerText = originalLabel;
                    btn.disabled = false;
                }
            } catch (err) {
                // FAIL HONESTLY. The old code claimed success on network errors,
                // which meant real enquiries vanished while the user walked away happy.
                console.error('Consultation submit failed:', err);
                showAlert('❌ Network error. Please try again, or email vakratronsystems@gmail.com', false);
                btn.innerText = originalLabel;
                btn.disabled = false;
            }
        };
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initConsultCta);
    } else {
        initConsultCta();
    }
})();