import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link
} from "react-router-dom";
import PolicyScoringDashboard from "./PolicyScoringDashboard";

const AboutPage = () => (
  <div className="min-h-screen p-8 bg-gradient-to-br from-blue-50 to-purple-100">
    <div className="max-w-3xl mx-auto space-y-4">
      <h1 className="text-2xl font-bold text-gray-800">About This Tool</h1>
      <p className="text-gray-700">
        This dashboard scores policy documents using a rubric grounded in evidence-based policy research.
        Documents are evaluated across five dimensions: Clarity, Rationale, Evidence, Alternatives, and Implementation.
        Scores are generated using free open-source AI models and visualized to help users assess policy quality.
      </p>
    </div>
  </div>
);

const ContactPage = () => (
  <div className="min-h-screen p-8 bg-gradient-to-br from-blue-50 to-purple-100">
    <div className="max-w-3xl mx-auto space-y-4">
      <h1 className="text-2xl font-bold text-gray-800">Contact</h1>
      <p className="text-gray-700">
        This project is maintained by Dr. Stefani Langehennig. You can view the code on GitHub or fork it for your own research use:
      </p>
      <a
        href="https://github.com/YOUR_USERNAME/YOUR_REPO"
        className="text-indigo-600 underline hover:text-indigo-800"
        target="_blank"
        rel="noopener noreferrer"
      >
        Visit GitHub Repository
      </a>
    </div>
  </div>
);

const Navigation = () => (
  <nav className="bg-white shadow py-4 px-8 mb-6">
    <ul className="flex space-x-6 text-gray-700 font-medium">
      <li><Link to="/">Upload</Link></li>
      <li><Link to="/about">About</Link></li>
      <li><Link to="/contact">Contact</Link></li>
    </ul>
  </nav>
);

export default function App() {
  return (
    <Router>
      <Navigation />
      <Routes>
        <Route path="/" element={<PolicyScoringDashboard />} />
        <Route path="/about" element={<AboutPage />} />
        <Route path="/contact" element={<ContactPage />} />
      </Routes>
    </Router>
  );
}
