import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import SearchContent from "./SearchContent";
import UFO_Sighting_Details from "./UFO_Sighting_Details";
import HomePage from "./HomePage";

const App = () => {
  return (
    <Router>
      <Routes>
        {/* <Route path="/" element={<HomePage />} /> */}
        {/* <Route path="/searchcontent" element={<SearchContent />} /> */}
        <Route path="/" element={<SearchContent />} />
        <Route path="/searchcontent/:id" element={<UFO_Sighting_Details />} />
      </Routes>
    </Router>
  );
};

export default App;
