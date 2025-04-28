import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./components/Home";
import UploadResume from "./components/UploadResume";
import Admin from "./components/Admin";
// import Dashboard from "./components/Dashboard";

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/upload" element={<UploadResume />} />
        <Route path="/admin" element={<Admin />} />
        {/* <Route path="/dashboard" element={<Dashboard/>} /> */}
      </Routes>
      {/* <Dashboard/> */}
    </Router>
  );
}

export default App;
