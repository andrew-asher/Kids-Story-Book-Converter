import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [text, setText] = useState('');
  const [audioURL, setAudioURL] = useState('');

  const handleConvert = async () => {
    try {
      const response = await axios.post('http://localhost:5009/text-to-speech', { text: text }, { responseType: 'blob' });

      if (response.status === 200) {
        const audioBlob = response.data;
        const audioUrl = URL.createObjectURL(audioBlob);
        setAudioURL(audioUrl);
      } else {
        console.error('Server returned an error:', response.statusText);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="Apps">
      <h1>Text to Speech</h1>
      <div className="input-container">
        <textarea
          placeholder="Enter your text"
          value={text}
          onChange={(e) => setText(e.target.value)}
        ></textarea>
        <button onClick={handleConvert}>Convert to Speech</button>
      </div>
      {audioURL && (
        <div className="audio-container">
          <audio controls src={audioURL}>Your browser does not support the audio tag.</audio>
        </div>
      )}
    </div>
  );
}

export default App;
