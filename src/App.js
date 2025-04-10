import { useState, useEffect } from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import * as pdfjsLib from "pdfjs-dist";
import mammoth from "mammoth";

// Fallback UI components
const Card = ({ children }) => <div className="border rounded-xl p-4 shadow bg-white">{children}</div>;
const CardContent = ({ children }) => <div>{children}</div>;
const Button = ({ children, ...props }) => <button {...props} className="bg-blue-600 text-white px-4 py-2 rounded mt-2">{children}</button>;
const Input = (props) => <input {...props} className="border px-2 py-1 rounded w-full" />;
const Slider = ({ value, min, max, step, onValueChange }) => (
  <input
    type="range"
    value={value[0]}
    min={min}
    max={max}
    step={step}
    onChange={(e) => onValueChange([parseInt(e.target.value, 10)])}
    className="w-full"
  />
);

const initialScores = [
  { dimension: "Empirical Research", score: 0 },
  { dimension: "Evidence-Gathering", score: 0 },
  { dimension: "Transparency", score: 0 },
  { dimension: "Expert Input", score: 0 },
  { dimension: "Evaluation", score: 0 },
];

const keywordHints = {
  "Empirical Research": ["peer-reviewed", "statistically significant", "data", "systematic review"],
  "Evidence-Gathering": ["impact assessment", "survey", "pilot study", "RCT"],
  "Transparency": ["methodology", "data available", "public", "open access"],
  "Expert Input": ["advisory board", "consultation", "stakeholder", "expert"],
  "Evaluation": ["evaluate", "monitoring", "feedback", "revision"],
};

export default function EvidenceDashboard() {
  const [scores, setScores] = useState(initialScores);
  const [documentText, setDocumentText] = useState("");
  const [autoHints, setAutoHints] = useState({});

  const updateScore = (index, value) => {
    const newScores = [...scores];
    newScores[index].score = value;
    setScores(newScores);
  };

  const extractTextFromPDF = async (file) => {
    const typedArray = new Uint8Array(await file.arrayBuffer());
    const pdf = await pdfjsLib.getDocument({ data: typedArray }).promise;
    let text = "";
    for (let i = 1; i <= pdf.numPages; i++) {
      const page = await pdf.getPage(i);
      const content = await page.getTextContent();
      text += content.items.map((item) => item.str).join(" ") + "\n";
    }
    return text;
  };

  const extractTextFromDOCX = async (file) => {
    const arrayBuffer = await file.arrayBuffer();
    const result = await mammoth.extractRawText({ arrayBuffer });
    return result.value;
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    let text = "";
    if (file.type === "application/pdf") {
      text = await extractTextFromPDF(file);
    } else if (
      file.name.endsWith(".docx") ||
      file.type === "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ) {
      text = await extractTextFromDOCX(file);
    } else {
      const reader = new FileReader();
      reader.onload = (event) => {
        setDocumentText(event.target.result);
      };
      reader.readAsText(file);
      return;
    }

    setDocumentText(text);
  };

  useEffect(() => {
    const hints = {};
    for (const [dimension, keywords] of Object.entries(keywordHints)) {
      const found = keywords.filter((kw) =>
        documentText.toLowerCase().includes(kw.toLowerCase())
      );
      if (found.length > 0) hints[dimension] = found;
    }
    setAutoHints(hints);
  }, [documentText]);

  const totalScore = scores.reduce((sum, s) => sum + s.score, 0);
  const classification =
    totalScore <= 4
      ? "Weak"
      : totalScore <= 9
      ? "Moderate"
      : totalScore <= 12
      ? "Strong"
      : "Robust";

  const handleExportCSV = () => {
    const header = ["Dimension", "Score"];
    const rows = scores.map(({ dimension, score }) => [dimension, score]);
    rows.push(["Total", totalScore]);
    rows.push(["Classification", classification]);

    const csvContent =
      [header, ...rows].map((e) => e.join(",")).join("\n");

    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.setAttribute("href", url);
    link.setAttribute("download", "policy_scoring_results.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="p-6 grid gap-6">
      <h1 className="text-3xl font-bold">Evidence-Based Policy Dashboard</h1>

      <Card>
        <CardContent>
          <h2 className="text-xl font-semibold mb-2">Upload Policy Document</h2>
          <Input type="file" accept=".txt,.doc,.docx,.pdf" onChange={handleFileUpload} />
        </CardContent>
      </Card>

      {documentText && (
        <Card>
          <CardContent className="max-h-64 overflow-y-auto">
            <h2 className="text-xl font-semibold mb-2">Document Preview</h2>
            <pre className="whitespace-pre-wrap text-sm text-gray-700">{documentText}</pre>
          </CardContent>
        </Card>
      )}

      <div className="grid md:grid-cols-2 gap-4">
        {scores.map((item, index) => (
          <Card key={item.dimension}>
            <CardContent>
              <h2 className="text-xl font-semibold mb-2">{item.dimension}</h2>
              {autoHints[item.dimension] && (
                <p className="text-sm text-green-600 mb-2">
                  Suggested Keywords Found: {autoHints[item.dimension].join(", ")}
                </p>
              )}
              <Slider
                min={0}
                max={3}
                step={1}
                value={[item.score]}
                onChange={(e) => updateScore(index, parseInt(e.target.value))}
              />
              <p className="mt-2">Score: {item.score}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      <Card>
        <CardContent>
          <h2 className="text-xl font-semibold mb-2">Overall Summary</h2>
          <p>Total Score: {totalScore}</p>
          <p>Classification: <strong>{classification}</strong></p>
          <Button onClick={handleExportCSV}>Export to CSV</Button>
        </CardContent>
      </Card>

      <Card>
        <CardContent className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={scores}>
              <XAxis dataKey="dimension" />
              <YAxis domain={[0, 3]} />
              <Tooltip />
              <Bar dataKey="score" fill="#8884d8" />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  );
}
