import React, { useState } from "react";

// const API_BASE = "https://spanner-rag-backend-oa24ximoaa-uc.a.run.app";

const API_BASE = "https://spanner-rag-backend-198925083406.us-central1.run.app";
// UPDATED QUESTION GROUPS BASED ON YOUR LATEST UPDATE
const questionCategories = {
  "Graph RAG": [
    "what is the recommendations will be a cost effective SSD ?",
    "I want to buy some advanced cameras for high end resolutions, what is the recommendations?",
    "I am looking for a beginner drone. Please give me some recommendations."
  ],
  "Traditional RAG": [
    "What accessories are compatible with the SkyHawk Zephyr Drone?",
    "What upgrades exist from the Aura X5 to the Aura X5 Pro?"
  ]
};

function App() {
  const [query, setQuery] = useState("");
  const [ragAnswer, setRagAnswer] = useState("");
  const [graphAnswer, setGraphAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSelectQuestion = (e) => {
    const value = e.target.value;
    if (value) {
      setQuery(value);
    }
  };

  const askQuestion = async () => {
    setLoading(true);
    setError(null);
    setRagAnswer("");
    setGraphAnswer("");

    try {
      const [ragRes, graphRes] = await Promise.all([
        fetch(`${API_BASE}/query/rag`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ query })
        }),
        fetch(`${API_BASE}/query/graph`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ query })
        })
      ]);

      const ragData = await ragRes.json();
      const graphData = await graphRes.json();

      if (!ragRes.ok || !graphRes.ok) {
        throw new Error("Backend returned an error");
      }

      setRagAnswer(ragData.answer || ragData.error || "No Traditional RAG response.");
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
        padding: "2rem"
      }}
    >

      {/* LOGOS */}
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          gap: "40px",
          marginBottom: "20px",
          alignItems: "center"
        }}
      >
        <img
          src="/images/spanner.png"
          alt="Spanner Logo"
          style={{ height: 60 }}
        />
        <img
          src="/images/googlecloud.png"
          alt="Google Cloud Logo"
          style={{ height: 60 }}
        />
      </div>

      <h1 style={{ textAlign: "center" }}>Graph-RAG Comparison</h1>

      {/* CATEGORY DROPDOWN */}
      <select
        onChange={handleSelectQuestion}
        style={{
          width: "100%",
          padding: 10,
          marginBottom: 15,
          borderRadius: 6,
          border: "1px solid #ccc",
          fontSize: "1rem"
        }}
      >
        <option value="">Choose a suggested question…</option>

        {Object.entries(questionCategories).map(([category, questions]) => (
          <optgroup key={category} label={category}>
            {questions.map((q, idx) => (
              <option key={idx} value={q}>
                {q}
              </option>
            ))}
          </optgroup>
        ))}
      </select>

      {/* TEXT INPUT */}
      <textarea
        rows={3}
        style={{
          width: "100%",
          fontSize: "1rem",
          borderRadius: 6,
          border: "1px solid #ccc",
          padding: 10
        }}
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Ask a question..."
      />

      <div style={{ textAlign: "center", marginTop: 10 }}>
        <button
          onClick={askQuestion}
          disabled={loading || !query}
          style={{
            background: query ? "#4CAF50" : "#9E9E9E",
            color: "white",
            border: "none",
            padding: "10px 20px",
            borderRadius: 5,
            cursor: query ? "pointer" : "not-allowed"
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
            marginTop: 20
          }}
        >
          {error}
        </div>
      )}

      {/* RESULTS SECTION */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          marginTop: 30,
          gap: "20px"
        }}
      >
        {/* TRADITIONAL RAG PANEL */}
        <div
          style={{
            flex: 1,
            background: "#f9f9f9",
            padding: 20,
            borderRadius: 8,
            boxShadow: "0 2px 4px rgba(0,0,0,0.1)"
          }}
        >
          <h2>Traditional RAG</h2>
          <div style={{ whiteSpace: "pre-wrap" }}>
            {ragAnswer || (loading && "Loading Traditional RAG answer...")}
          </div>
        </div>

        {/* GRAPH RAG PANEL */}
        <div
          style={{
            flex: 1,
            background: "#f9f9f9",
            padding: 20,
            borderRadius: 8,
            boxShadow: "0 2px 4px rgba(0,0,0,0.1)"
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
