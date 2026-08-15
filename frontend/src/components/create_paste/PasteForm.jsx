const PasteFrom = ({ content, onContentChange, loading, submitHandler, error }) => {
  return (
    <form
      className="flex flex-col flex-1 px-6 py-5"
      onSubmit={(e) => {
        submitHandler(e);
      }}
    >
      <textarea
        className="flex-1 overflow-auto dark:bg-gray-700 dark:text-gray-100 p-4 rounded-lg whitespace-pre-wrap"
        placeholder="Paste code snippets here..."
        value={content}
        onChange={(e) => onContentChange(e.target.value)}
        disabled={loading}
      />

      {error && (
        <p className="bg-red-100 text-red-500 text-center font-bold px-4 py-3 rounded-lg whitespace-pre-wrap">
        {error}
        </p>
      )}

      <div className="flex justify-center mt-5">
        <button
          className="bg-sky-500 hover:bg-sky-700 action:scale-95 text-white text-xl font-bold py-3 px-5 rounded-lg"
          type="submit"
          disabled={loading}
        >
          {loading ? "Generating..." : "Generate Link"}
        </button>
      </div>
    </form>
  )
}

export default PasteFrom;
