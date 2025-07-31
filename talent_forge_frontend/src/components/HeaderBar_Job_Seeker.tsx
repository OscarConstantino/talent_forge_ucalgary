// !!! REMOVE THIS FUNCTION if CSRF_COOKIE_HTTPONLY is TRUE !!!
// It will always return null and cause confusion.
// function getCookie(name: string) { /* ... */ }

const Header = () => {
  // Helper function to get CSRF token from the meta tag
  const getCsrfTokenFromMeta = () => {
    const metaTag = document.querySelector('meta[name="csrf-token"]');
    return metaTag ? metaTag.getAttribute('content') : null;
  };

  const handleSignOut = async () => {
    // Get the CSRF token directly from the meta tag
    const csrftoken = getCsrfTokenFromMeta(); 

    if (!csrftoken) {
      console.error("CSRF token not found in meta tag. Cannot sign out.");
      alert("Logout failed: CSRF token missing from page. Please refresh.");
      return;
    }

    try {
      const response = await fetch("/logout", {
        method: "POST",
        headers: {
          'X-CSRFToken': csrftoken, // Use the token from the meta tag
          'Content-Type': 'application/json', // Assuming your Django view expects JSON
        },
        // VERY IMPORTANT: This ensures the browser sends HttpOnly cookies (like csrftoken and sessionid)
        credentials: 'include', 
        body: JSON.stringify({}), // Send an empty JSON body if your logout view doesn't expect data
      });

      if (response.ok) { // response.ok checks for 2xx status codes
        console.log("User signed out successfully from Django.");
        window.location.href = '/login'; // Redirect to login page
      } else {
        const errorData = await response.text(); // Get specific error message from Django
        console.error(`Logout failed: ${response.status} - ${errorData}`);
        alert(`Logout failed: ${errorData || 'Unknown error'}`);
      }
    } catch (error) {
      console.error("Error during sign out:", error);
      alert("An unexpected error occurred during logout.");
    }
  };

  return (
    <header className="main-header">
      <div className="logo-section">
        {/* Use Django's static tag if this HTML is rendered by Django, otherwise use direct path */}
        <img src="/static/images/LogoBlack.png" alt="TF Logo" className="logo-img"/>
        <span className="brand-text"></span>
      </div>
      <nav className="nav-links">
        {/* Use Django's {% url %} tags if this component's parent is rendered by Django, or absolute paths/React Router for SPA */}
        <a href="/job_seeker_dashboard/" className="active">Home</a>
        <a href="/job_seeker/profile/">Profile</a>
        <a href="/my_applications/">Jobs applied</a>
        <a href="/job_search_page/">Search Job</a>
      </nav>
      <div className="user-controls">
        {/* Your logout button */}
        <button onClick={handleSignOut} className="btn btn-primary btn-sm d-flex align-items-center ">
          <svg xmlns="http://www.w3.org/2000/svg" className="me-1" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
              <polyline points="16 17 21 12 16 7" />
              <line x1="21" y1="12" x2="9" y2="12" />
          </svg>
          <span className="sign-out-text">Sign Out</span>
        </button>
      </div>
    </header>
  );
};

export default Header;