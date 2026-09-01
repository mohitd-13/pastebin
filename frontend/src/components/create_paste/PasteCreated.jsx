const PasteCreated = ({ pasteUrl, copied, copyToClipboard, error, copyError }) => {
  return (
    <div className="flex flex-col flex-1 px-6 py-5">
      <div className="flex-1 overflow-auto bg-sky-100 dark:bg-gray-700 text-green-700 dark:text-gray-100 p-4 rounded-lg flex items-center justify-center">
        <div className="border-2 border-dashed border-gray-400 rounded-lg p-6 w-full h-full flex flex-col items-center justify-center text-center">
          <h2 className="text-2xl font-bold mb-1">Success!</h2>
          <p className="dark:text-gray-300 text-green-700 mb-4">Your pasted URL:</p>
          <pre className="bg-green-200 dark:bg-gray-500 text-green-700 dark:text-gray-100 px-4 py-3 rounded-lg whitespace-pre-wrap inline-block">
            {pasteUrl}
          </pre>
        </div>
      </div>

      {error && (
        <p className="bg-red-100 text-red-500 text-center font-bold px-4 py-3 rounded-lg whitespace-pre-wrap">
          {error}
        </p>
      )}

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
  )
}

export default PasteCreated;
