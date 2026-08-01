import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./Home";
import ViewPaste from "./ViewPaste";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/:id" element={<ViewPaste />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
