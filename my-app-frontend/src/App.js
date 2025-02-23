import React, { useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import './App.css';

function Home() {
  const labels = ["Happy or Sad?", "Calm or Tense", "Which year you want to watch?"];
  const [barValues, setBarValues] = useState([0, 0, 1975]);
  const [likedGenres, setLikedGenres] = useState([]);
  const [dislikedGenres, setDislikedGenres] = useState([]);
  const [keepMood, setKeepMood] = useState(false);
  const [yearRange, setYearRange] = useState([1920, 2025]);
  const navigate = useNavigate();

  const genres = [
    "Action", "Comedy", "Drama", "Horror", "Sci-Fi", "Romance", "Thriller", "Adventure", "Fantasy"
  ];

  const handleSliderChange = useCallback((index, newValue) => {
    setBarValues(prevValues => {
      const newValues = [...prevValues];
      newValues[index] = Number(newValue);
      return newValues;
    });
  }, []);

  const handleGenreSelection = (genre, type) => {
    if (type === 'like') {
      if (likedGenres.includes(genre)) {
        setLikedGenres(likedGenres.filter(item => item !== genre));
      } else if (likedGenres.length < 3) {
        setLikedGenres([...likedGenres, genre]);
      }
    } else {
      if (dislikedGenres.includes(genre)) {
        setDislikedGenres(dislikedGenres.filter(item => item !== genre));
      } else {
        setDislikedGenres([...dislikedGenres, genre]);
      }
    }
  };

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
      <h1 style={{ marginTop: "200px" }}>How do you feel?</h1>

      {/* Genre Selection for "Like" */}
      <div>
        <h2>What Genres Do You Like? (Max 3)</h2>
        <div className="genre-slider">
          {genres.map((genre, index) => (
            <div
              key={index}
              className={`genre-box ${likedGenres.includes(genre) ? 'selected' : ''}`}
              onClick={() => handleGenreSelection(genre, 'like')}
            >
              {genre}
            </div>
          ))}
        </div>
      </div>

      {/* Genre Selection for "Dislike" */}
      <div>
        <h2>What Genres Do You Dislike?</h2>
        <div className="genre-slider">
          {genres.map((genre, index) => (
            <div
              key={index}
              className={`genre-box ${dislikedGenres.includes(genre) ? 'selected' : ''} ${likedGenres.includes(genre) ? 'disabled' : ''}`}
              onClick={() => handleGenreSelection(genre, 'dislike')}
            >
              {genre}
            </div>
          ))}
        </div>
      </div>

      {/* Mood Sliders */}
      {barValues.map((value, index) => (
        <div key={index} className="slider-container">
          <label style={{ fontSize: "35px" }}>
            {labels[index]}: {value}
          </label>
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

      {/* Checkbox for Mood */}
      <div>
        <input
          type="checkbox"
          checked={keepMood}
          onChange={() => setKeepMood(!keepMood)}
        />
        <label>Do You Want To Keep Your Mood?</label>
      </div>

      {/* Year Range Slider */}
      <div>
        <h2>{labels[2]}</h2>
        <input
          type="range"
          min={1920}
          max={2025}
          value={yearRange[0]}
          onChange={(e) => setYearRange([e.target.value, yearRange[1]])}
        />
        <input
          type="range"
          min={1920}
          max={2025}
          value={yearRange[1]}
          onChange={(e) => setYearRange([yearRange[0], e.target.value])}
        />
        <p>{`Year Range: ${yearRange[0]} - ${yearRange[1]}`}</p>
      </div>

      <button onClick={handleConfirm}>Confirm</button>
    </div>
  );
}

export default Home;

function NewPage() {
  const location = useLocation();
  const { barValues, rankedMovies } = location.state || { barValues: [], rankedMovies: [] };

  const movies = (rankedMovies && rankedMovies.length > 0
    ? rankedMovies.filter((movie) => movie.Year >= barValues[2]).slice(0, 10)
    : []);

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
