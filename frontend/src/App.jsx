import { BrowserRouter, Routes, Route } from "react-router-dom";
import CreatePaste from "./components/CreatePaste";
import ViewPaste from "./components/ViewPaste";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<CreatePaste />} />
        <Route path="/:id" element={<ViewPaste />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
