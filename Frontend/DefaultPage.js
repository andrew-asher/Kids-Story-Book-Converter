import React, { useState } from 'react';

function DefaultPage() {
  const [defaultStory, setDefaultStory] = useState("In a small, quiet village, there lived a poor artist named Maya. She longed for a magical paintbrush that could bring her paintings to life. One day, as she sat by the river, a talking frog appeared. The frog granted her wish, giving her a paintbrush that could make her dreams a reality. Maya’s first creation was a magnificent tree, and as soon as she painted it, it sprouted in her garden. Excitement filled her heart as she realized the power of the brush. She painted a river that flowed with crystal-clear water and a sky filled with brilliant stars. But soon, greed took over her heart. She painted a grand palace and began to live a life of luxury. Her friends and family, concerned by her change, tried to remind her of the happiness she once had. One day, Maya painted a beautiful bird and wished for it to sing. Instead, it let out a mournful cry. She realized that her magical brush had lost its power because she had used it for selfish desires. Filled with regret, Maya painted a simple, humble cottage and wished for her old life back. The cottage appeared, and her heart felt light once more. She returned to her village, where she shared her story and the lessons she had learned about the true meaning of happiness and contentment. The magical paintbrush remained in her hands, but she vowed to use it only for good, creating art that would inspire and bring joy to others. These short stories offer a glimpse into different worlds and lessons about kindness, curiosity, and the consequences of our choices.");
  const [summary, setSummary] = useState('');

  async function summarizeDefaultStory() {
    try {
      const response = await fetch('http://localhost:5005/summarize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ document: defaultStory }),
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
        <h1>Default Story</h1>
        <div className="input-container">
          <textarea
            placeholder="Enter your default story"
            value={defaultStory}
            onChange={(e) => setDefaultStory(e.target.value)}
          ></textarea>
          <button onClick={summarizeDefaultStory}>Summarize</button>
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

export default DefaultPage;
