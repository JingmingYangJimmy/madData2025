import React, { useState, useCallback } from 'react';
import { BrowserRouter as Router, Route, Routes, useNavigate } from 'react-router-dom';
import './App.css';
import happy from './images/happy.png';
import sad from './images/sad.png';
import anger from './images/anger.png';
import calm from './images/calm.png';
import disguest from './images/disguest.png';
import fear from './images/fear.png';
import surprise from './images/surprise.png';
import trust from './images/trust.png';



function Home() {
  const labels = ["Sad or Happy?", "Fear or Angry?", "Surprise or Boredom?", "Anxious or Calm?"];
  const [barValues, setBarValues] = useState([0, 0, 0, 0]);
  const navigate = useNavigate(); 


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
      const keyMap = ["happy_index", "fear_index", "surprise_index", "anxious_index"];
      const formattedData = barValues.reduce((acc, value, index) => {
        acc[keyMap[index]] = value;
        return acc;
      }, {});

      const response = await fetch('http://localhost:3000/api/store-values', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ barValues: formattedData }) // Send as an object

      });
  
      if (!response.ok) {
        const errorText = await response.text(); // Handle non-JSON errors
        throw new Error(`HTTP error! Status: ${response.status} - ${errorText}`);
      }
  
      const data = await response.json();
      console.log('Stored successfully:', data);
      alert('Values confirmed: ' + JSON.stringify(data.barValues));
      navigate('/new-page');
  
    } catch (error) {
      console.log("that is an error!");
      console.error('Error storing values:', error.message);
    }
  };

  return (
    <div className="App">
      <h1 style={{ marginTop: "200px" }}>Which movie do you like the most?</h1>
      {barValues.map((value, index) => (
        <div key={index} className="slider-container" >
          
    {index === 0 && <img src={happy} alt="happy" className="my-emoji-left" />}
    {index === 1 && <img src={fear} alt="sad" className="my-emoji-left" />}
    {index === 2 && <img src={surprise} alt="surprise" className="my-emoji-left" />}
    {index === 3 && <img src={trust} alt="anxious" className="my-emoji-left" />}


    <label style={{ fontSize: "35px"  }}>
    {labels[index]}: {value}
    </label>

    {index === 0 && <img src={sad} alt="neutral" className="my-emoji-right" />}
    {index === 1 && <img src={anger} alt="angry" className="my-emoji-right" />}
    {index === 2 && <img src={calm} alt="bored" className="my-emoji-right" />}
    {index === 3 && <img src={disguest} alt="calm" className="my-emoji-right" />}

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


function NewPage() {
  return (
    <div className="App">
      <h1>Welcome to the New Interface!</h1>
      <p>Your values have been stored successfully.</p>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/new-page" element={<NewPage />} />
      </Routes>
    </Router>
  );
}

export default App;
