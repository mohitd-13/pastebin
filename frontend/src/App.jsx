import { BrowserRouter, Routes, Route } from "react-router-dom";
import GeneratePaste from "./components/create_paste/GeneratePaste";
import ViewPaste from "./components/view_paste/ViewPaste";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<GeneratePaste />} />
        <Route path="/:id" element={<ViewPaste />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
