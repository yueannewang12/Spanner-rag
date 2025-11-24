import React, { useState } from "react";

const API_BASE = "https://spanner-rag-backend-oa24ximoaa-uc.a.run.app";

function App() {
  const DEFAULT_QUESTION =
    "I am looking for a beginner drone. Please give me some recommendations.";
  const [query, setQuery] = useState(DEFAULT_QUESTION);
  const [ragAnswer, setRagAnswer] = useState("");
  const [graphAnswer, setGraphAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const askQuestion = async () => {
    setLoading(true);
    setError(null);
    setRagAnswer("");
    setGraphAnswer("");

    try {
      // Fetch both RAG and Graph RAG answers in parallel
      const [ragRes, graphRes] = await Promise.all([
        fetch(`${API_BASE}/query/rag`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ query }),
        }),
        fetch(`${API_BASE}/query/graph`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ query }),
        }),
      ]);

      const ragData = await ragRes.json();
      const graphData = await graphRes.json();

      if (!ragRes.ok || !graphRes.ok) {
        throw new Error("Backend returned an error");
      }

      setRagAnswer(ragData.answer || ragData.error || "No RAG response.");
      setGraphAnswer(
        graphData.answer || graphData.error || "No Graph RAG response."
      );
    } catch (err) {
      console.error("Fetch error:", err);
      setError("⚠️ Could not contact backend. Please try again later.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        fontFamily: "sans-serif",
        maxWidth: 1200,
        margin: "auto",
        padding: "2rem",
      }}
    >
      <h1 style={{ textAlign: "center" }}>Graph-RAG Comparison</h1>

      <textarea
        rows={3}
        style={{
          width: "100%",
          fontSize: "1rem",
          borderRadius: 6,
          border: "1px solid #ccc",
          padding: 10,
        }}
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />

      <div style={{ textAlign: "center", marginTop: 10 }}>
        <button
          onClick={askQuestion}
          disabled={loading}
          style={{
            background: "#4CAF50",
            color: "white",
            border: "none",
            padding: "10px 20px",
            borderRadius: 5,
            cursor: "pointer",
          }}
        >
          {loading ? "Thinking..." : "Ask"}
        </button>
      </div>

      {error && (
        <div
          style={{
            color: "#b00020",
            background: "#ffe6e6",
            padding: 10,
            borderRadius: 5,
            marginTop: 20,
          }}
        >
          {error}
        </div>
      )}

      {/* Two-column layout for RAG and Graph RAG */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          marginTop: 30,
          gap: "20px",
        }}
      >
        {/* RAG Panel */}
        <div
          style={{
            flex: 1,
            background: "#f9f9f9",
            padding: 20,
            borderRadius: 8,
            boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
          }}
        >
          <h2>RAG (Vector Retrieval)</h2>
          <div style={{ whiteSpace: "pre-wrap" }}>
            {ragAnswer || (loading && "Loading RAG answer...")}
          </div>
        </div>

        {/* Graph RAG Panel */}
        <div
          style={{
            flex: 1,
            background: "#f9f9f9",
            padding: 20,
            borderRadius: 8,
            boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
          }}
        >
          <h2>Graph RAG</h2>
          <div style={{ whiteSpace: "pre-wrap" }}>
            {graphAnswer || (loading && "Loading Graph RAG answer...")}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
