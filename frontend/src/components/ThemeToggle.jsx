import { useState } from "react";
import { Moon, Sun } from "lucide-react";
import { applyTheme, getInitialTheme } from "../lib/theme";
import Button from "./ui/Button";

function ThemeToggle() {
  const [theme, setTheme] = useState(getInitialTheme);

  function toggleTheme() {
    const next = theme === "dark" ? "light" : "dark";
    applyTheme(next);
    setTheme(next);
  }

  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={toggleTheme}
      aria-label="Toggle theme"
    >
      {theme === "dark" ? <Sun size={18} /> : <Moon size={18} />}
    </Button>
  );
}

export default ThemeToggle;