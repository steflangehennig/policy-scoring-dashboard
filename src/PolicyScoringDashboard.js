import React, { useState, useRef } from "react";
import { UploadCloud, Loader2, Download, AlertTriangle } from "lucide-react";
import html2canvas from "html2canvas";
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer } from "recharts";

const Card = ({ children, className = "" }) => (
  <div className={`bg-white shadow rounded-lg ${className}`}>{children}</div>
);

const CardContent = ({ children, className = "" }) => (
  <div className={`p-4 ${className}`}>{children}</div>
);

const Button = ({ children, className = "", ...props }) => (
  <button
    className={`px-4 py-2 rounded font-medium transition-colors ${className}`}
    {...props}
  >
    {children}
  </button>
);

export default function PolicyScoringDashboard() {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedRadar, setSelectedRadar] = useState(null);
  const chartRef = useRef(null);

  const validTypes = ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/plain"];

  const handleFileChange = (event) => {
    const files = Array.from(event.target.files);
    const invalidFile = files.find((file) => !validTypes.includes(file.type));
    if (invalidFile) {
      setError("One or more files have invalid types. Please upload only PDF, DOCX, or TXT files.");
      setSelectedFiles([]);
      return;
    }
    setSelectedFiles(files);
    setResults([]);
    setError(null);
  };

  const handleSubmit = async () => {
    if (!selectedFiles.length) return;
    setLoading(true);
    setError(null);

    try {
      const scored = selectedFiles.map((file, i) => ({
        fileName: file.name,
        scores: {
          Clarity: (i % 5) + 1,
          Rationale: ((i + 1) % 5) + 1,
          Evidence: ((i + 2) % 5) + 1,
          Alternatives: ((i + 3) % 5) + 1,
          Implementation: ((i + 4) % 5) + 1,
        },
      }));
      setTimeout(() => {
        setResults(scored);
        setSelectedRadar(scored[0]);
        setLoading(false);
      }, 1000);
    } catch (err) {
      setLoading(false);
      setError("An error occurred while scoring the documents. Please try again.");
    }
  };

  const handleExportCSV = () => {
    const header = ["File", "Clarity", "Rationale", "Evidence", "Alternatives", "Implementation"];
    const rows = results.map((r) => [
      r.fileName,
      r.scores.Clarity,
      r.scores.Rationale,
      r.scores.Evidence,
      r.scores.Alternatives,
      r.scores.Implementation,
    ]);
    const csvContent = [header, ...rows].map((e) => e.join(",")).join("\n");
    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.setAttribute("download", "scoring_results.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const chartData = selectedRadar
    ? Object.entries(selectedRadar.scores).map(([dimension, score]) => ({ dimension, score }))
    : [];

  return (
    <div className="min-h-screen p-8 bg-gray-100 text-emerald-900">
      <div className="max-w-4xl mx-auto space-y-8">
        <Card className="shadow-2xl rounded-2xl">
          <CardContent className="p-6">
            <h1 className="text-2xl font-bold text-emerald-900 mb-2">Upload Policy Documents</h1>
            <p className="text-sm text-emerald-800 mb-4">
              This tool uses free and open-source AI models to score uploaded policy documents based on evidence-based policy dimensions.
              To maintain performance and fairness, a limit may apply to the number of documents you can upload at one time. 
              <strong> Note:</strong> The current app only renders the front end and not the back end (e.g., actual scoring model. This is coming soon.)
            </p>
            <input
              type="file"
              multiple
              accept=".pdf,.docx,.txt"
              onChange={handleFileChange}
              className="block w-full text-sm text-emerald-900 bg-white border border-emerald-200 rounded-lg cursor-pointer focus:outline-none mb-4 p-2"
            />
            {error && (
              <div className="flex items-center text-red-600 mb-4">
                <AlertTriangle className="mr-2 w-5 h-5" /> {error}
              </div>
            )}
            <Button
              onClick={handleSubmit}
              disabled={!selectedFiles.length || loading}
              className="bg-emerald-700 hover:bg-emerald-800 text-white"
            >
              {loading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <UploadCloud className="mr-2 h-4 w-4" />}
              {loading ? "Scoring..." : "Submit for Scoring"}
            </Button>
          </CardContent>
        </Card>

        {results.length > 0 && (
          <Card className="shadow-2xl rounded-2xl">
            <CardContent className="p-6">
              <h2 className="text-xl font-semibold text-emerald-900 mb-4">Evidence-Based Policy Scores</h2>
              <div className="overflow-x-auto mb-6">
                <table className="min-w-full table-auto text-left border border-emerald-200 bg-white">
                  <thead>
                    <tr className="bg-emerald-100">
                      <th className="px-4 py-2">File</th>
                      <th className="px-4 py-2">Clarity</th>
                      <th className="px-4 py-2">Rationale</th>
                      <th className="px-4 py-2">Evidence</th>
                      <th className="px-4 py-2">Alternatives</th>
                      <th className="px-4 py-2">Implementation</th>
                      <th className="px-4 py-2">View</th>
                    </tr>
                  </thead>
                  <tbody>
                    {results.map(({ fileName, scores }) => (
                      <tr key={fileName} className="border-t border-emerald-200">
                        <td className="px-4 py-2 font-medium text-emerald-900">{fileName}</td>
                        <td className="px-4 py-2">{scores.Clarity}</td>
                        <td className="px-4 py-2">{scores.Rationale}</td>
                        <td className="px-4 py-2">{scores.Evidence}</td>
                        <td className="px-4 py-2">{scores.Alternatives}</td>
                        <td className="px-4 py-2">{scores.Implementation}</td>
                        <td className="px-4 py-2">
                          <Button onClick={() => setSelectedRadar({ fileName, scores })} className="text-xs bg-emerald-600 text-white hover:bg-emerald-700">
                            Radar
                          </Button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              {selectedRadar && (
                <div>
                  <h3 className="text-lg font-semibold text-emerald-900 mb-2">Radar Chart: {selectedRadar.fileName}</h3>
                  <div ref={chartRef} className="h-80 bg-white rounded-xl p-4">
                    <ResponsiveContainer width="100%" height="100%">
                      <RadarChart cx="50%" cy="50%" outerRadius="70%" data={chartData}>
                        <PolarGrid />
                        <PolarAngleAxis dataKey="dimension" />
                        <PolarRadiusAxis domain={[0, 5]} tickCount={6} />
                        <Radar name="Score" dataKey="score" stroke="#047857" fill="#047857" fillOpacity={0.6} />
                      </RadarChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              )}
              <Button onClick={handleExportCSV} className="mt-4 bg-emerald-700 hover:bg-emerald-800 text-white">
                <Download className="mr-2 h-4 w-4" /> Download Results as CSV
              </Button>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
