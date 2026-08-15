import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getPaste } from "../../api";

const ViewPaste = () => {
  const { id } = useParams();

  const [content, setContent] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [copyError, setCopyError] = useState("");
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    async function fetchPaste() {
      try {
        setLoading(true);
        setError("");
        setCopyError("");

        const res = await getPaste(id);
        setContent(res);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    fetchPaste();
  }, [id]);

  async function copyToClipboard() {
    try {
      await navigator.clipboard.writeText(content);

      setCopied(true);

      setTimeout(() => {
        setCopied(false);
      }, 2000);
    } catch {
      setCopyError("Failed to copy content.");
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen bg-gray-100 dark:bg-gray-900">
        <p className="text-xl dark:text-gray-100">
          Loading paste...
        </p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-screen bg-gray-100 dark:bg-gray-900">
        <p className="text-red-500 bg-red-400 text-xl">
          {error}
        </p>
      </div>
    );
  }

  return (
    <div className="flex items-center justify-center h-screen bg-gray-100 dark:bg-gray-900">
      <div className="flex flex-col h-3/4 w-1/2 dark:bg-gray-800 rounded-2xl overflow-hidden">
        <div className="px-6 pt-5">

          <h3 className="text-xl font-bold dark:text-gray-100">
            PasteBin
          </h3>
        </div>

        <div className="flex flex-col flex-1 px-6 py-5">
          <pre className="flex-1 overflow-auto bg-gray-700 text-gray-100 p-4 rounded-lg whitespace-pre-wrap">
            {content}
          </pre>

          {copyError && (
            <p className="bg-red-100 text-red-500 text-center font-bold px-4 py-3 rounded-lg whitespace-pre-wrap">
              {copyError}
            </p>
          )}

          <div className="flex justify-center mt-5">
            <button
              onClick={copyToClipboard}
              className="bg-green-500 hover:bg-green-700 text-white text-xl font-bold py-3 px-5 rounded-lg"
            >
              {copied ? "Copied!" : "Copy to Clipboard"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ViewPaste;
