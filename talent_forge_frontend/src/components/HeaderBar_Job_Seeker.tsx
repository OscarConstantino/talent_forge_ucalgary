import { User, LogOut } from "lucide-react";

// Helper function to get CSRF token from cookies
function getCookie(name: string) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const Header = () => {
  const handleSignOut = async () => {
    const csrftoken = getCookie('csrftoken'); // Get it once here

    if (!csrftoken) {
      console.error("CSRF token not found. Cannot sign out.");
      // Potentially alert the user or redirect them
      return; // Stop the function if no token
    }

    try {
      const response = await fetch("/logout", {
        method: "POST",
        headers: {
          'X-CSRFToken': csrftoken, // Use the retrieved token
          // Remove or change Content-Type if not sending JSON
          // 'Content-Type': 'application/json',
        },
        // For logout, you typically don't send a body.
        // If Django expects an empty JSON object, uncomment:
        // body: JSON.stringify({}),
      });

      if (response.ok) {
        console.log("User signed out successfully from Django.");
        window.location.href = '/login'; // Or your desired redirect
      } else {
        const errorData = await response.text(); // Get more details on error
        console.error(`Logout failed: ${response.status} - ${errorData}`);
        // Handle specific Django errors if needed (e.g., if CSRF token was invalid)
      }
    } catch (error) {
      console.error("Error during sign out:", error);
    }
  };

  return (
    <header className="main-header">
      <div className="logo-section">

        <img src="/static/images/LogoBlack.png" alt="TF Logo" className="logo-img"/>
        <span className="brand-text"></span>
      </div>
      <nav className="nav-links">
        <a href="/job_seeker_dashboard/" className="active">Home</a>
        <a href="#">Profile</a>
        <a href="/my_applications/">Jobs applied</a>
        <a href="/job_search_page/">Search Job</a>
      </nav>
      <div className="user-controls"> {/* Changed div name for better semantics */}
        <User size={24} strokeWidth={2.5} />
        {/* Sign-out button */}
        <button onClick={handleSignOut} className="sign-out-button">
          <LogOut size={24} strokeWidth={2.5} />
          <span className="sign-out-text">Sign Out</span> {/* Optional text label */}
        </button>
      </div>
    </header>
  );
};

export default Header;
