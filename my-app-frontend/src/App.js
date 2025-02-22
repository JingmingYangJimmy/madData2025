import React, { useState, useCallback } from 'react';
import './App.css';
import happy from './images/happy.png';

function App() {
  const labels = ["Sad or Happy?", "Fear or Angry?", "Surprise or Boredom?", "Anxious or Calm?"];
  const [barValues, setBarValues] = useState([0, 0, 0, 0]);

  const handleSliderChange = (index, newValue) => {
    setBarValues(prevValues => {
      const newValues = [...prevValues];
      newValues[index] = Number(newValue);
      return newValues;
    });
  };

  const handleConfirm = async () => {
    const currentValues = [...barValues]; // Ensure latest state values
    console.log('Storing values into the database:', currentValues);

    try {
      const response = await fetch('/api/store-values', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ barValues })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      console.log('Stored successfully:', data);
      alert('Values confirmed: ' + currentValues.join(', '));

    } catch (error) {
      console.error('Error storing values:', error);
    }
  };

  return (
    <div className="App">
      <h2>Which movie do you like the most?</h2>
      <img src={happy} alt="Sample" className="my-image" />
      {barValues.map((value, index) => (
        <div key={index} style={{ marginBottom: '10px' }}>
          <label>{labels[index]}: {value}</label>
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
