import { NavLink, Link, useNavigate } from "react-router-dom";
import { isAuthenticated, removeToken } from "../auth/auth";
import "./Navbar.css";

function Navbar() {
  const navigate = useNavigate();
    if (!isAuthenticated()) {
    return null;
}
  function handleLogout() {
    removeToken();
    navigate("/login");
  }

  return (
    <nav className="navbar">
  <div className="navbar-inner">
    <Link to="/" className="navbar-brand">
      Research Paper Assistant
    </Link>

    <div className="navbar-links">
      <NavLink
  to="/"
  className={({ isActive }) =>
    `navbar-link ${isActive ? "active" : ""}`
  }
>
  Papers
</NavLink>

<NavLink
  to="/bookmarks"
  className={({ isActive }) =>
    `navbar-link ${isActive ? "active" : ""}`
  }
>
  Bookmarks
</NavLink>

      <button className="navbar-logout" onClick={handleLogout}>
        Logout
      </button>
    </div>
  </div>
</nav>
  );
}

export default Navbar;