import React, { useState } from 'react';
import '../Apps.css';


function InputPage() {
  const [document, setDocument] = useState('');
  const [summary, setSummary] = useState('');

  async function summarizeText() {
    try {
      const response = await fetch('http://localhost:5005/summarize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ document }),
      });

      if (response.ok) {
        const data = await response.json();
        setSummary(data.summary);
      } else {
        console.error('Server returned an error:', response.statusText);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  }

  return (
    <div className="Apps">
      <header className="Apps-header">
        <h1>Summarize Your Story Here</h1>
        <div className="input-container">
          <textarea
            placeholder="Enter your document"
            value={document}
            onChange={(e) => setDocument(e.target.value)}
          ></textarea>
          <button onClick={summarizeText}>Summarize</button>
        </div>
        {summary && (
          <div className="summary-container">
            <h2>Summary:</h2>
            <p>{summary}</p>
          </div>
        )}
      </header>
    </div>
  );
}

export default InputPage;
