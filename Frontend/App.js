import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import InputPage from './pages/InputPage';
import DefaultPage from './pages/DefaultPage';
import TextToSpeechApp from './pages/TextToSpeechApp'; // Assuming it's in the 'pages' folder

function App() {
  return (
    <Router>
      <div>
        {/* Navigation Links */}
        <nav>
          <ul>
            <li><Link to="/input">Input Page</Link></li>
            <li><Link to="/">Default Page</Link></li>
            <li><Link to="/text-to-speech">Text to Speech</Link></li> {/* Added this new link */}
          </ul>
        </nav>

        <Routes>
          <Route path="/input" element={<InputPage />} />
          <Route path="/" element={<DefaultPage />} />
          <Route path="/text-to-speech" element={<TextToSpeechApp />} /> {/* Added this new route */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
