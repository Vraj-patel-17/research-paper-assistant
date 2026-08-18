import { Link, useNavigate } from "react-router-dom";
import { isAuthenticated, removeToken } from "../auth/auth";

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
    <nav>
      <Link to="/">Papers</Link>{" "}
      <Link to="/bookmarks">Bookmarks</Link>{" "}
      <button onClick={handleLogout}>Logout</button>
    </nav>
  );
}

export default Navbar;