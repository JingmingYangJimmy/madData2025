import React, { useState, useCallback, useEffect, useRef } from 'react';
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
import { motion, useAnimation } from "framer-motion";

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
      const keyMap = ["happy_index", "calm_index", "time_index"];
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

  const movies = (rankedMovies || []).slice(0, 10);

  const [hoveredMovie, setHoveredMovie] = useState(null);
  const [movieHovered, setMovieHovered] = useState(false);
  const movieControls = useAnimation();
  const movieTimeoutRef = useRef(null);

  const startMovieAnimation = () => {
    movieControls.start({
      x: [0, -movies.length * 200],
      transition: {
        repeat: Infinity,
        duration: 20,
        ease: "linear",
      },
    });
  };

  useEffect(() => {
    if (movies.length === 0) return;

    if (!movieHovered) {
      movieTimeoutRef.current = setTimeout(() => {
        startMovieAnimation();
      }, 5000);
    } else {
      movieControls.stop();
      clearTimeout(movieTimeoutRef.current);
    }

    return () => {
      clearTimeout(movieTimeoutRef.current);
    };
  }, [movieHovered, movieControls, startMovieAnimation, movies.length]);

  return (
    <div className="App">
      <h1>Here are your results!</h1>

      {/* Movie Carousel */}
      <div
        className="relative w-full h-80 overflow-hidden bg-black"
        onMouseEnter={() => setMovieHovered(true)}
        onMouseLeave={() => setMovieHovered(false)}
      >
        <motion.div
          className="flex space-x-4 cursor-grab"
          animate={movieControls}
          initial={{ x: 0 }}
          drag="x"
          dragConstraints={{ left: -movies.length * 200, right: 0 }}
          dragMomentum={false}
        >
          {[...movies, ...movies].map((movie, index) => (
            <motion.div
              key={index}
              className="relative w-48 h-72 shrink-0 cursor-pointer"
              onMouseEnter={() => setHoveredMovie(index)}  // Use index instead of movie.id
              onMouseLeave={() => setHoveredMovie(null)}
              animate={hoveredMovie === index ? { scale: 1.1 } : { scale: 1 }} // Compare with index
              transition={{ duration: 0.3 }}
            >
              <img src={movie.Poster} alt={movie.Title} className="w-full h-full object-cover" />
              <h3 className="absolute bottom-4 left-4 text-white">{movie.Title}</h3>

              {/* Display Plot and Year only for the hovered movie */}
              {hoveredMovie === index && (
                <div className="absolute bottom-0 left-0 bg-black bg-opacity-70 text-white p-4 w-full">
                  <p>{movie.Plot}</p>
                  <p>{movie.Year}</p>
                </div>
              )}
            </motion.div>
          ))}
        </motion.div>
      </div>
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
