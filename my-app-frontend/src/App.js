import React, { useState, useCallback } from 'react';
import { BrowserRouter as Router, Route, Routes, useNavigate, useLocation } from 'react-router-dom';
import './App.css';
import happy from './images/happy.png';
import sad from './images/sad.png';
import anger from './images/anger.png';
import calm from './images/calm.png';
// import disguest from './images/disguest.png';
// import fear from './images/fear.png';
// import surprise from './images/surprise.png';
// import trust from './images/trust.png';
import dinosaur from './images/dinosaur.png'
import smartphone from './images/smartphone.png'

function Home() {

  const labels = ["Happy or Sad?", "Calm or Tense", "Which year you want to watch?"];
  const [barValues, setBarValues] = useState([0, 0, 1975]);
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

      // Pass the movie data to the new page via navigate
      navigate('/new-page', { state: { barValues, rankedMovies: data.rankedMovies } });
  
    } catch (error) {
      console.log("That is an error!");
      console.error('Error storing values:', error.message);
    }
  };

  return (
    <div className="App">
      <h1 style={{ marginTop: "200px" }}>Which movie do you like the most?</h1>
      {barValues.map((value, index) => (
        <div key={index} className="slider-container">
          {index === 0 && <img src={calm} alt="calm" className="my-emoji-left" />}
          {index === 1 && <img src={happy} alt="happy" className="my-emoji-left" />}
          {index === 2 && <img src={dinosaur} alt="old" className="my-emoji-left" />}

          <label style={{ fontSize: "35px" }}>
            {labels[index]}: {value}
          </label>

          {index === 0 && <img src={sad} alt="sad" className="my-emoji-right" />}
          {index === 1 && <img src={anger} alt="anger" className="my-emoji-right" />}
          {index === 2 && <img src={smartphone} alt="smartphone" className="my-emoji-right" />}

          <br />
          <input
            type="range"
            min={index === 2 ? "1920" : "-1"}
            max={index === 2 ? "2025" : "1"}
            step={index === 2 ? "1" : "0.1"}
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
  const location = useLocation();
  const { barValues, rankedMovies } = location.state || { barValues: [], rankedMovies: [] };

  return (
    <div className="App">
      <h1>Welcome to the New Interface!</h1>
      <p>Your values have been stored successfully.</p>

      {/* Display user input values */}
      <h3>User Inputs:</h3>
      <ul>
        {Object.entries(barValues).map(([key, value]) => (
          <li key={key}>
            {key}: {value}
          </li>
        ))}
      </ul>

      {/* Display ranked movies */}
      {rankedMovies.length > 0 && (
        <div className="ranked-movies">
          <h2>Top Movies:</h2>
          <div className="movies-list">
            {rankedMovies.map((movie, index) => (
              <div key={index} className="movie">
                <img src={movie.Poster} alt={movie.Title} className="movie-poster" />
                <h3>{movie.Title}</h3>
              </div>
            ))}
          </div>
        </div>
      )}
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
