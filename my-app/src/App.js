import React, { useState } from 'react';
import './App.css';

function App() {
  const labels = ["Sad or Happy?", "Fear or Angry?", "Suprise or Boredom?","Anxious or Calm?"];

  const [barValues, setBarValues] = useState([0, 0,0,0]);

  const handleSliderChange = (index, newValue) => {
    setBarValues(prevValues => {
      const newValues = [...prevValues];
      newValues[index] = newValue;
      return newValues;
    });
  };

  // Handle confirm button click
  const handleConfirm = () => {
    console.log('Storing values into the database:', barValues);

    // Example API call (uncomment and adjust as needed):
    /*
    fetch('/api/store-values', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ barValues })
    })
      .then(response => response.json())
      .then(data => console.log('Stored successfully:', data))
      .catch(error => console.error('Error storing values:', error));
    */

    alert('Values confirmed: ' + barValues.join(', '));
  };

  return (
    <div className="App">
      <h2>Which movie you like the most</h2>
      {barValues.map((value, index) => (
        <div key={index} style={{ marginBottom: '10px' }}>
          <label>
          {labels[index]}: {value}
          </label>
          <br />
          <input
            type="range"
            min="-10"
            max="10"
            value={value}
            onChange={(e) => handleSliderChange(index, Number(e.target.value))}
          />
        </div>
      ))}
      <button onClick={handleConfirm}>Confirm</button>
    </div>
  );
}

export default App;
