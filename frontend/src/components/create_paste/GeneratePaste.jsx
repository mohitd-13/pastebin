import { useState } from "react";
import { createPaste } from "../../api";
import PasteForm from "./PasteForm";
import PasteCreated from "./PasteCreated";

const CreatePaste = () => {
  const [content, setContent] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [copyError, setCopyError] = useState("");
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
    setCopyError("");
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
      setCopyError("Failed to copy link.");
    }
  }

  return (
    <div className="flex items-center justify-center h-screen bg-gray-100 dark:bg-gray-900">
      <div className="flex flex-col h-3/4 w-1/2 bg-sky-200 dark:bg-gray-800 rounded-2xl overflow-hidden">
        <div className="px-6 pt-5">
            <h3 className="text-xl font-bold dark:text-gray-100">PasteBin</h3>
            <p className="dark:text-gray-400 text-gray-600">Save and share your code snippets with others.</p>
        </div>

        {pasteUrl
          ? <PasteCreated pasteUrl={pasteUrl} copied={copied} copyToClipboard={copyToClipboard} error={error} copyError={copyError} />
          : <PasteForm content={content} onContentChange={setContent} loading={loading} submitHandler={submitHandler} error={error} />
        }

      </div>
    </div>
  )
}

export default CreatePaste;
