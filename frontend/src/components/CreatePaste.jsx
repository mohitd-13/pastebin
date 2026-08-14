import { useState } from "react";
import { createPaste } from "../api";
import CopyButton from "./CopyButton";
import LinkButton from "./LinkButton";


const CreatePaste = () => {
  const [content, setContent] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [pasteUrl, setPasteUrl] = useState("");
  const [copied, setCopied] = useState(false);

  async function submitHandler(e) {
    e.preventDefault();

    if (!content.trim()) {
      setError("Content cannot be empty");
      return;
    }

    setLoading(true);
    setError("");
    setPasteUrl("");
    setCopied(false);

    try {
      const res = await createPaste(content);
      const url = `${window.location.origin}/${res.id}`;
      setPasteUrl(url);
      setContent("");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function copyToClipboard() {
    try {
      await navigator.clipboard.writeText(pasteUrl);

      setCopied(true);
      setTimeout(() => {
        setCopied(false);
      }, 2000);
    } catch {
      setError("Failed to copy link.");
    }
  }

  return (
    <div className="flex items-center justify-center h-screen bg-gray-100 dark:bg-gray-900">
      <div className="flex flex-col h-3/4 w-1/2 dark:bg-gray-800 rounded-2xl overflow-hidden">
        <div className="h-1/7 px-6 pt-5">

            <h3 className="text-xl font-bold dark:text-gray-100">PasteBin</h3>
            <p className="dark:text-gray-400">Save and share your code snippets with others.</p>
        </div>

        <form
          className="flex flex-col h-6/7 px-6"
          onSubmit={(e) => {
            submitHandler(e);
          }}>
          <textarea
            className="h-4/5 dark:bg-gray-600 px-2 py-2"
            placeholder="Paste code snippets here..."
            value={content}
            onChange={(e) => setContent(e.target.value)}
            disabled={loading}
          />
          {error && (
            <p className="text-red-500 text-center mt-2">{error}</p>
          )}
          {pasteUrl && (
            <div className="flex items-center gap-2 mt-3">
              <input
                className="flex-1 px-3 py-2 rounded"
                type="text"
                value={pasteUrl}
                readOnly
              />

            </div>
          )}
          <div className="flex items-center justify-center h-1/5">
            {pasteUrl ? <CopyButton copyFunction={copyToClipboard} copied={copied} /> : <LinkButton loading={loading} />}
          </div>
        </form>
      </div>
    </div>
  )
}

export default CreatePaste;
