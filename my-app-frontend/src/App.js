import React, { useState, useCallback } from 'react';
import './App.css';
import happy from './images/happy.png';

function App() {
  const labels = ["Sad or Happy?", "Fear or Angry?", "Surprise or Boredom?", "Anxious or Calm?"];
  const [barValues, setBarValues] = useState([0, 0, 0, 0]);

  const handleSliderChange = useCallback((index, newValue) => {
    setBarValues(prevValues => {
      const newValues = [...prevValues];
      newValues[index] = Number(newValue);
      return newValues;
    });
  }, []);

  const handleConfirm = async () => {
    console.log('Storing values into the database:', barValues);
  
    try {
      const response = await fetch('/api/store-values', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          barValues: barValues.reduce((acc, value, index) => {
            const keyMap = ["happy_index", "fear_index", "surprise_index", "anxious_index"];
            acc[keyMap[index]] = value;
            return acc;
          }, {})
        })
      });
  
      if (!response.ok) {
        const errorText = await response.text(); // Handle non-JSON errors
        throw new Error(`HTTP error! Status: ${response.status} - ${errorText}`);
      }
  
      const data = await response.json();
      console.log('Stored successfully:', data);
      alert('Values confirmed: ' + JSON.stringify(data.barValues));
  
    } catch (error) {
      console.error('Error storing values:', error);
      alert(`Error: ${error.message}`);
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
            onChange={(e) => handleSliderChange(index, e.target.value)}
            />
        </div>
      ))}
      <button onClick={handleConfirm}>Confirm</button>
    </div>
  );
}

export default App;
