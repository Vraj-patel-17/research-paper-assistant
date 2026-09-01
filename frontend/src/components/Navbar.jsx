import { useState } from "react";
import { NavLink, Link, useNavigate } from "react-router-dom";
import { isAuthenticated, removeToken } from "../auth/auth";
import "./Navbar.css";

const NAV_LINKS = [
  { to: "/", label: "Papers", end: true },
  { to: "/bookmarks", label: "Bookmarks", end: false },
];

function Navbar() {
  const navigate = useNavigate();
  const [menuOpen, setMenuOpen] = useState(false);

  if (!isAuthenticated()) {
    return null;
  }

  function handleLogout() {
    removeToken();
    navigate("/login");
  }

  function closeMenu() {
    setMenuOpen(false);
  }

  return (
    <nav className="navbar">
      <div className="navbar-inner">
        <Link to="/" className="navbar-brand" onClick={closeMenu}>
          Research Paper Assistant
        </Link>

        <button
          type="button"
          className="navbar-toggle"
          aria-label="Toggle navigation menu"
          aria-expanded={menuOpen}
          onClick={() => setMenuOpen((open) => !open)}
        >
          <span className="navbar-toggle-bar" />
          <span className="navbar-toggle-bar" />
          <span className="navbar-toggle-bar" />
        </button>

        <div className={`navbar-links ${menuOpen ? "open" : ""}`}>
          {NAV_LINKS.map(({ to, label, end }) => (
            <NavLink
              key={to}
              to={to}
              end={end}
              className={({ isActive }) =>
                `navbar-link ${isActive ? "active" : ""}`
              }
              onClick={closeMenu}
            >
              {label}
            </NavLink>
          ))}

          <button type="button" className="navbar-logout" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;