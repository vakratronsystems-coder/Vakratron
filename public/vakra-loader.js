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