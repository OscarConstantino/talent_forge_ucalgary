document.addEventListener('DOMContentLoaded', function() {
    const cookieBanner = document.getElementById('cookieConsentBanner');
    const acceptBtn = document.getElementById('acceptCookiesBtn');
    const declineBtn = document.getElementById('declineCookiesBtn'); // Get the new decline button
    const COOKIE_NAME = 'talentforge_cookie_consent';

    // Function to set a cookie
    function setCookie(name, value, days) {
        let expires = "";
        if (days) {
            const date = new Date();
            date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
            expires = "; expires=" + date.toUTCString();
        }
        document.cookie = name + "=" + (value || "") + expires + "; path=/; SameSite=Lax";
    }

    // Function to get a cookie
    function getCookie(name) {
        const nameEQ = name + "=";
        const ca = document.cookie.split(';');
        for(let i=0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) === ' ') c = c.substring(1, c.length);
            if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
        }
        return null;
    }

    // Function to apply consent based on cookie value
    function applyConsent(consentValue) {
        if (consentValue === 'accepted') {
            // User has accepted all cookies
            // Enable any scripts/features that rely on non-essential cookies here
            // For example:
            // loadGoogleAnalytics();
            // loadMarketingPixels();
            console.log("Cookies accepted. Non-essential functionalities are enabled.");
        } else if (consentValue === 'declined') {
            // User has declined non-essential cookies
            // Disable/block any scripts/features that rely on non-essential cookies here
            // Ensure no GA, tracking pixels etc. are loaded or initialized.
            console.log("Cookies declined. Non-essential functionalities are disabled.");
            // You might want to revoke consent for any services that were already loaded
            // if this function is called after an initial page load.
        }
        // Hide the banner regardless of choice
        cookieBanner.style.display = 'none';
    }

    // On page load, check for consent
    const currentConsent = getCookie(COOKIE_NAME);
    if (currentConsent) {
        applyConsent(currentConsent);
    } else {
        cookieBanner.style.display = 'flex'; // Show banner if no consent yet
    }

    // Event listener for the accept button
    if (acceptBtn) {
        acceptBtn.addEventListener('click', function() {
            setCookie(COOKIE_NAME, 'accepted', 365); // Set cookie to 'accepted' for 1 year
            applyConsent('accepted');
        });
    }

    // Event listener for the decline button
    if (declineBtn) {
        declineBtn.addEventListener('click', function() {
            setCookie(COOKIE_NAME, 'declined', 365); // Set cookie to 'declined' for 1 year
            applyConsent('declined');
        });
    }
});