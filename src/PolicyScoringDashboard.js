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

    const scored = [];

    for (const file of selectedFiles) {
      const formData = new FormData();
      formData.append("file", file);

      try {
        const response = await fetch("https://steflangehennig-policy-scoring-api.hf.space/score", {
          method: "POST",
          body: formData,
        });

        if (!response.ok) {
          throw new Error("Failed to score document");
        }

        const data = await response.json();
        const rawScores = data.scores;

        const scores = {
          EmpiricalResearch: rawScores["Use of Empirical Research"].score,
          FormalEvidenceGathering: rawScores["Formal Evidence-Gathering Process"].score,
          TransparencyAccessibility: rawScores["Transparency and Accessibility"].score,
          ExpertStakeholderInput: rawScores["Expert and Stakeholder Input"].score,
          EvaluationIteration: rawScores["Evaluation and Iteration"].score,
        };

        scored.push({
          fileName: file.name,
          scores,
        });
      } catch (err) {
        console.error("Scoring error:", err);
        setError(`Failed to score document: ${file.name}`);
      }
    }

    setResults(scored);
    setSelectedRadar(scored[0] || null);
    setLoading(false);
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
              This tool uses free and open-source AI models to score uploaded policy documents based on five evidence-based policy dimensions.
              The output shows the scores ranging from 0-3 and a radar chart showing the scores across the dimension. You can export a .csv file
              of your results. 
            </p>
            <p className="text-sm text-emerald-800 mb-4">
              To maintain performance and fairness using the free features of FastAPI and Hugging Face, a limit applies to the number of documents 
              you can upload at one time (5 documents max every 30 minutes, and 1 document at a time). Currently, the scoring model accepts .docx and .txt files.
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
                      <th className="px-4 py-2">Empirical Research</th>
                      <th className="px-4 py-2">Formal Evidence Gathering</th>
                      <th className="px-4 py-2">Transparency & Accessibility</th>
                      <th className="px-4 py-2">Expert & Stakeholder Input</th>
                      <th className="px-4 py-2">Evalutation & Iteration</th>
                      <th className="px-4 py-2">View</th>
                    </tr>
                  </thead>
                  <tbody>
                    {results.map(({ fileName, scores }) => (
                      <tr key={fileName} className="border-t border-emerald-200">
                        <td className="px-4 py-2 font-medium text-emerald-900">{fileName}</td>
                        <td className="px-4 py-2">{scores.EmpiricalResearch}</td>
                        <td className="px-4 py-2">{scores.FormalEvidenceGathering}</td>
                        <td className="px-4 py-2">{scores.TransparencyAccessibility}</td>
                        <td className="px-4 py-2">{scores.ExpertStakeholderInput}</td>
                        <td className="px-4 py-2">{scores.EvaluationIteration}</td>
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
                        <PolarRadiusAxis domain={[0, 3]} tickCount={6} />
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
