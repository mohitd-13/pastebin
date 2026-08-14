const LinkButton = (props) => {
  return (
    <button
      className="bg-sky-500 hover:bg-sky-700 action:scale-95 text-white text-xl font-bold py-3 px-5 rounded-lg"
      type="submit"
      disabled={props.loading}
    >
      {props.loading ? "Generating..." : "Generate Link"}
    </button>
  )
}

export default LinkButton;
