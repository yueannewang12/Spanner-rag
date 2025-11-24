import React, { useState } from "react";
import { auth, login, logout } from "./firebase";

const API_BASE = "https://spanner-rag-backend-198925083406.us-central1.run.app";

function App() {
  const [user, setUser] = useState(null);
  const [query, setQuery] = useState("");
  const [mode, setMode] = useState("rag"); // or "graph"
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSignIn = async () => {
    try {
      const result = await login();
      setUser(result.user);
    } catch (err) {
      alert("Login failed: " + err.message);
    }
  };

  const handleLogout = async () => {
    await logout();
    setUser(null);
  };

  const askQuestion = async () => {
    if (!query.trim()) return alert("Please enter a question.");
    setLoading(true);
    setAnswer("");

    try {
      const res = await fetch(`${API_BASE}/query/${mode}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });
      const data = await res.json();
      setAnswer(data.answer || data.error || "No response.");
    } catch (err) {
      setAnswer("Error contacting backend: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif", maxWidth: 800, margin: "auto" }}>
      <h1>Spanner RAG Assistant</h1>

      {!user ? (
        <button onClick={handleSignIn}>Sign in with Google</button>
      ) : (
        <>
          <p>👋 Welcome, {user.displayName} <button onClick={handleLogout}>Log out</button></p>

          <div style={{ marginTop: 20 }}>
            <label>
              <b>Mode:</b>{" "}
              <select value={mode} onChange={(e) => setMode(e.target.value)}>
                <option value="rag">RAG (Vector Retrieval)</option>
                <option value="graph">Graph RAG</option>
              </select>
            </label>
          </div>

          <textarea
            rows={3}
            style={{ width: "100%", marginTop: 20, fontSize: "1rem" }}
            placeholder="Ask a question..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />

          <div style={{ marginTop: 10 }}>
            <button onClick={askQuestion} disabled={loading}>
              {loading ? "Thinking..." : "Ask"}
            </button>
          </div>

          {answer && (
            <div
              style={{
                background: "#f7f7f7",
                padding: 15,
                borderRadius: 8,
                marginTop: 20,
                whiteSpace: "pre-wrap",
              }}
            >
              <b>Answer:</b>
              <p>{answer}</p>
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default App;
