import { Link } from "react-router-dom";
import "../styles/Navbar.css";

const Navbar = () => {
  return (
    <nav className="navbar">
      <h1>AI Resume Screener</h1>
      <ul>
        <li><Link to="/">Home</Link></li>
        <li><Link to="/upload">Upload Resume</Link></li>
        <li><Link to="/admin">Admin</Link></li>
      </ul>
    </nav>
  );
};

export default Navbar;