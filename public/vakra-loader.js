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
// 🌌 VAKRATRON ADVISORY PLATFORM - ULTIMATE THEME MATRIX SYNC
document.addEventListener("DOMContentLoaded", () => {
    const TARGET_THEME_COLOR = "#030d1a"; // Aapka signature slate blue-black tone

    const enforceUniformTheme = () => {
        // 1. Force override global window elements
        document.documentElement.style.setProperty('background', TARGET_THEME_COLOR, 'important');
        document.documentElement.style.setProperty('background-color', TARGET_THEME_COLOR, 'important');
        document.body.style.setProperty('background', TARGET_THEME_COLOR, 'important');
        document.body.style.setProperty('background-color', TARGET_THEME_COLOR, 'important');

        // 2. Select every structural node capable of breaking the background flow
        const layoutSelectors = 'section, div, main, footer, header, .hero, .solutions, .roadmap-section, .why-card, .pain-section';
        const elements = document.querySelectorAll(layoutSelectors);

        elements.forEach(el => {
            // Unke purane background elements aur configurations ko completely force delete kijiye
            el.style.setProperty('background', TARGET_THEME_COLOR, 'important');
            el.style.setProperty('background-color', TARGET_THEME_COLOR, 'important');
            el.style.setProperty('background-image', 'none', 'important');
            el.style.setProperty('border-color', 'rgba(255, 255, 255, 0.03)', 'important');
        });
        
        console.log("[VAKRA-OS]: Global uniform slate theme successfully loaded.");
    };

    // Run execution loops immediately during lifecycle phases
    enforceUniformTheme();
    setTimeout(enforceUniformTheme, 50);
    setTimeout(enforceUniformTheme, 200); // Dynamic grids loader buffer protection
});