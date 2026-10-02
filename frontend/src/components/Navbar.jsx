import { useState } from "react";
import { NavLink, Link, useNavigate } from "react-router-dom";
import { AnimatePresence, motion as Motion } from "framer-motion";
import { BookOpen, LogOut, Menu, X } from "lucide-react";
import { isAuthenticated, removeToken } from "../auth/auth";
import { cn } from "../lib/utils";
import ThemeToggle from "./ThemeToggle";
import Button from "./ui/Button";

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
    setMenuOpen(false);
    navigate("/login");
  }

  function closeMenu() {
    setMenuOpen(false);
  }

  const linkClass = ({ isActive }) =>
    cn(
      "rounded-lg px-3 py-2 text-sm font-medium transition-colors",
      isActive
        ? "bg-accent text-primary"
        : "text-muted-foreground hover:bg-accent hover:text-foreground"
    );

  const links = NAV_LINKS.map(({ to, label, end }) => (
    <NavLink key={to} to={to} end={end} className={linkClass} onClick={closeMenu}>
      {label}
    </NavLink>
  ));

  return (
    <nav className="sticky top-0 z-40 h-14 border-b border-border bg-background/80 backdrop-blur">
      <div className="mx-auto flex h-full max-w-6xl items-center justify-between px-4 sm:px-6">
        <Link to="/" onClick={closeMenu} className="flex items-center gap-2 font-semibold">
          <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-accent text-primary">
            <BookOpen size={18} />
          </span>
          <span className="hidden sm:inline">Research Paper Assistant</span>
        </Link>

        <div className="hidden items-center gap-1 md:flex">
          {links}
          <ThemeToggle />
          <Button variant="ghost" size="sm" onClick={handleLogout}>
            <LogOut size={16} />
            Logout
          </Button>
        </div>

        <div className="flex items-center gap-1 md:hidden">
          <ThemeToggle />
          <Button
            variant="ghost"
            size="icon"
            aria-label="Toggle navigation menu"
            aria-expanded={menuOpen}
            onClick={() => setMenuOpen((open) => !open)}
          >
            {menuOpen ? <X size={18} /> : <Menu size={18} />}
          </Button>
        </div>
      </div>

      <AnimatePresence>
        {menuOpen && (
          <Motion.div
            initial={{ opacity: 0, y: -8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            transition={{ duration: 0.15 }}
            className="absolute inset-x-0 top-full flex flex-col gap-1 border-b border-border bg-background p-3 md:hidden"
          >
            {links}
            <Button
              variant="ghost"
              className="justify-start"
              onClick={handleLogout}
            >
              <LogOut size={16} />
              Logout
            </Button>
          </Motion.div>
        )}
      </AnimatePresence>
    </nav>
  );
}

export default Navbar;