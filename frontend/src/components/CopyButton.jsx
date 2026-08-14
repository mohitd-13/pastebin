const CopyButton = (props) => {

  return (
    <button
      className="bg-green-500 hover:bg-green-700 action:scale-95 text-white text-xl font-bold py-3 px-5 rounded-lg"
      type="button"
      onClick={props.copyFunction}
    >
      {props.copied ? "Copied!" : "Copy to Clipboard"}
    </button>
  )
}

export default CopyButton;
