import React from "react";
import { Routes, Route, Link } from "react-router-dom";
import PolicyScoringDashboard from "./PolicyScoringDashboard";
import { FaGithub } from 'react-icons/fa';

const AboutPage = () => (
  <div className="min-h-screen p-8 bg-gray-100 text-emerald-900">
    <div className="max-w-3xl mx-auto space-y-4">
      <h1 className="text-2xl font-bold">About This Tool</h1>
      <p>
        This dashboard scores policy documents using a rubric grounded in evidence-based policy research.
        Documents are evaluated across five dimensions: Use of Empirical Research, Formal Evidence Gathering, Transparency & Accessibility, Expert & Stakeholder Input, and Evaluation & Iteration.
        Scores are generated using free open-source AI models and visualized to help users assess policy quality.
      </p>
    </div>
  </div>
);

const ContactPage = () => (
  <div className="min-h-screen p-8 bg-gray-100 text-emerald-900">
    <div className="max-w-3xl mx-auto space-y-4">
      <h1 className="text-2xl font-bold">Contact</h1>
      <p>
        This project is maintained by Dr. Stefani Langehennig. You can view the code on GitHub:
      </p>
      <a
        href="https://github.com/steflangehennig/policy-scoring-dashboard"
        className="text-emerald-700 underline hover:text-emerald-900 flex items-center space-x-2"
        target="_blank"
        rel="noopener noreferrer"
      >
        <FaGithub size={24} />
        <span>Visit GitHub Repository</span>
      </a>
    </div>
  </div>
);

const Navigation = () => (
  <nav className="bg-gray-50 text-emerald-900 shadow py-4 px-8 mb-6 border-b border-emerald-200">
    <ul className="flex space-x-6 font-medium">
      <li><Link to="/" className="hover:text-emerald-700">Upload</Link></li>
      <li><Link to="/About" className="hover:text-emerald-700">About</Link></li>
      <li><Link to="/Contact" className="hover:text-emerald-700">Contact</Link></li>
    </ul>
  </nav>
);

export default function App() {
  return (
    <div className="min-h-screen bg-gray-100 text-emerald-900">
      <Navigation />
      <Routes>
        <Route
          path="/"
          element={
            <div className="max-w-4xl mx-auto p-6">
              <PolicyScoringDashboard />
            </div>
          }
        />
        <Route path="/about" element={<AboutPage />} />
        <Route path="/contact" element={<ContactPage />} />
        <Route
          path="*"
          element={
            <div className="max-w-4xl mx-auto p-6">
              <PolicyScoringDashboard />
            </div>
          }
        />
      </Routes>
    </div>
  );
}
