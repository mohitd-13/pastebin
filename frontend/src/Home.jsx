import { useState } from "react";
import { createPaste } from "./api";

function Home() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null); // will hold the created link
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  async function handleCreateLink() {
    setLoading(true);
    setError(null);
    setResult(null);
    setCopied(false);

    try {
      const data = await createPaste(text);
      const link = `${window.location.origin}/${data.id}`;
      setResult(link);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function handleCopy() {
    navigator.clipboard.writeText(result);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  }

  return (
    <div style={{ maxWidth: 600, margin: "60px auto", fontFamily: "sans-serif" }}>
      <h1>Pastebin</h1>

      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Paste your logs/text here..."
        rows={10}
        style={{
          width: "100%",
          backgroundColor: "#f0f0f0",
          border: "1px solid #ccc",
          borderRadius: 6,
          padding: 12,
          fontSize: 14,
          fontFamily: "monospace",
          resize: "vertical",
          boxSizing: "border-box",
        }}
      />

      <button
        onClick={handleCreateLink}
        disabled={loading || !text.trim()}
        style={{ marginTop: 12, padding: "8px 16px", cursor: "pointer" }}
      >
        {loading ? "Creating..." : "Create Link"}
      </button>

      {(result || error) && (
        <div
          style={{
            marginTop: 20,
            backgroundColor: "#f0f0f0",
            border: "1px solid #ccc",
            borderRadius: 6,
            padding: 12,
          }}
        >
          {error ? (
            <span style={{ color: "red" }}>{error}</span>
          ) : (
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <span style={{ fontFamily: "monospace" }}>{result}</span>
              <button onClick={handleCopy} style={{ cursor: "pointer" }}>
                {copied ? "Copied!" : "Copy URL"}
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default Home;