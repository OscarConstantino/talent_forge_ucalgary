// static/js/vanta.js
document.addEventListener("DOMContentLoaded", function() {
    if (typeof VANTA !== 'undefined' && VANTA.NET) {
        VANTA.NET({
            el: "#vanta-background", // Ensure this matches HTML
            mouseControls: true,
            touchControls: true,
            gyroControls: false,
            minHeight: 200.00, // <--- Check these values
            minWidth: 200.00,  // <---
            scale: 1.00,
            scaleMobile: 1.00,
            color: 0xaa9432,
            backgroundColor: 0x141d46,
            points: 13.00,
            maxDistance: 22.00,
            spacing: 18.00
        });
    } else {
        console.error("VANTA library not loaded or not ready.");
    }
});