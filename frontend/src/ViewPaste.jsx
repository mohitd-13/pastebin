import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { getPaste } from "./api";

function ViewPaste() {
  const { id } = useParams(); // reads the "id" from the URL, e.g. /93idmk -> "93idmk"
  const [paste, setPaste] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getPaste(id)
      .then((data) => setPaste(data))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [id]);

  return (
    <div style={{ maxWidth: 600, margin: "60px auto", fontFamily: "sans-serif" }}>
      <h1>Pastebin</h1>

      {loading && <p>Loading...</p>}

      {error && (
        <div
          style={{
            backgroundColor: "#f0f0f0",
            border: "1px solid #ccc",
            borderRadius: 6,
            padding: 12,
            color: "red",
          }}
        >
          {error}
        </div>
      )}

      {paste && (
        <pre
          style={{
            backgroundColor: "#f0f0f0",
            border: "1px solid #ccc",
            borderRadius: 6,
            padding: 12,
            fontSize: 14,
            fontFamily: "monospace",
            whiteSpace: "pre-wrap",
            wordBreak: "break-word",
          }}
        >
          {paste.content}
        </pre>
      )}
    </div>
  );
}

export default ViewPaste;