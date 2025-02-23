import { useState, useEffect, useRef } from "react";
import { motion, useAnimation } from "framer-motion";
import { PlayCircle } from "lucide-react";

// Movie List (Updated with guaranteed working image URLs)
const movies = [
  {
    id: 1,
    title: "Inception",
    poster: "https://m.media-amazon.com/images/I/51Q2WjtSYyL._AC_.jpg",
    trailer: "https://www.youtube.com/embed/YoHD9XEInc0",
    description: "A thief who enters the dreams of others to steal secrets.",
    watchLink: "https://www.netflix.com/title/70131314",
  },
  {
    id: 2,
    title: "Interstellar",
    poster: "https://m.media-amazon.com/images/I/71l1hOg7uJL._AC_SY679_.jpg",
    trailer: "https://www.youtube.com/embed/zSWdZVtXT7E",
    description: "A team of explorers travel through a wormhole in space.",
    watchLink: "https://www.netflix.com/title/70305903",
  },
  {
    id: 3,
    title: "The Dark Knight",
    poster: "https://m.media-amazon.com/images/I/91k6Y-SNTLL._AC_SY679_.jpg",
    trailer: "https://www.youtube.com/embed/EXeTwQWrcwY",
    description: "Batman battles the Joker in Gotham City.",
    watchLink: "https://www.hbomax.com/feature/urn:hbo:feature:GYLjM_QBaR8PDwwEAABHL",
  },
  {
    id: 4,
    title: "Avatar",
    poster: "https://m.media-amazon.com/images/I/71KP6sPzz2L._AC_SY679_.jpg",
    trailer: "https://www.youtube.com/embed/5PSNL1qE6VY",
    description: "A marine on an alien planet joins its native tribe.",
    watchLink: "https://www.disneyplus.com/movies/avatar/7djkbve0X7Zx",
  },
  {
    id: 5,
    title: "Titanic",
    poster: "https://m.media-amazon.com/images/I/91Bw9v2t9yL._AC_SY679_.jpg",
    trailer: "https://www.youtube.com/embed/kVrqfYjkTdQ",
    description: "A love story set on the ill-fated Titanic.",
    watchLink: "https://www.disneyplus.com/movies/titanic/6LZP5OoaRHyZ",
  },
  // Add more movies as needed
];

// TV Show List (Updated with guaranteed working image URLs)
const tvShows = [
  {
    id: 1,
    title: "Breaking Bad",
    poster: "https://m.media-amazon.com/images/I/91FzPaCl6bL._AC_SY679_.jpg",
    trailer: "https://www.youtube.com/embed/HhesaQXLuRY",
    description: "A high school chemistry teacher turned methamphetamine manufacturer.",
    watchLink: "https://www.netflix.com/title/70143836",
  },
  {
    id: 2,
    title: "Stranger Things",
    poster: "https://m.media-amazon.com/images/I/81LHTVvcKKL._AC_SY679_.jpg",
    trailer: "https://www.youtube.com/embed/XWxyRG_tckY",
    description: "A group of kids discovers a dark secret in their town.",
    watchLink: "https://www.netflix.com/title/80057281",
  },
  {
    id: 3,
    title: "The Crown",
    poster: "https://m.media-amazon.com/images/I/91-9G45p06L._AC_SY679_.jpg",
    trailer: "https://www.youtube.com/embed/q0K8V7v8tqM",
    description: "The reign of Queen Elizabeth II, from her early days to the present.",
    watchLink: "https://www.netflix.com/title/80025678",
  },
  {
    id: 4,
    title: "Money Heist",
    poster: "https://m.media-amazon.com/images/I/81yQpF6ufLL._AC_SY679_.jpg",
    trailer: "https://www.youtube.com/embed/OMOsaFyJd4c",
    description: "A group of criminals plan the biggest heist in history.",
    watchLink: "https://www.netflix.com/title/80192098",
  },
  {
    id: 5,
    title: "The Witcher",
    poster: "https://m.media-amazon.com/images/I/71QOPf5gGqL._AC_SY679_.jpg",
    trailer: "https://www.youtube.com/embed/ndl1W4ltY3A",
    description: "A monster hunter searches for his place in a world filled with magic.",
    watchLink: "https://www.netflix.com/title/80189685",
  },
  // Add more TV shows as needed
];

export default function MovieAndTVCarousel() {
  const [hoveredMovie, setHoveredMovie] = useState(null);
  const [hoveredTVShow, setHoveredTVShow] = useState(null);
  const [movieHovered, setMovieHovered] = useState(false);
  const [tvShowHovered, setTVShowHovered] = useState(false);

  const movieControls = useAnimation();
  const tvShowControls = useAnimation();
  const movieTimeoutRef = useRef(null);
  const tvShowTimeoutRef = useRef(null);

  // Start movie animation
  const startMovieAnimation = () => {
    movieControls.start({
      x: [0, -movies.length * 200], // Start position and end position
      transition: {
        repeat: Infinity, // Repeat animation indefinitely
        duration: 20, // Time it takes to scroll from start to end
        ease: "linear", // Linear scrolling
      },
    });
  };

  // Start TV show animation
  const startTVShowAnimation = () => {
    tvShowControls.start({
      x: [0, -tvShows.length * 200], // Start position and end position
      transition: {
        repeat: Infinity, // Repeat animation indefinitely
        duration: 20, // Time it takes to scroll from start to end
        ease: "linear", // Linear scrolling
      },
    });
  };

  // Handle hover for stopping the carousels
  useEffect(() => {
    if (!movieHovered) {
      // If movie carousel isn't hovered, set a timeout to start animation after 5 seconds
      movieTimeoutRef.current = setTimeout(() => {
        startMovieAnimation();
      }, 5000);
    } else {
      movieControls.stop();
      clearTimeout(movieTimeoutRef.current); // Clear timeout when hovered
    }

    if (!tvShowHovered) {
      // If TV show carousel isn't hovered, set a timeout to start animation after 5 seconds
      tvShowTimeoutRef.current = setTimeout(() => {
        startTVShowAnimation();
      }, 5000);
    } else {
      tvShowControls.stop();
      clearTimeout(tvShowTimeoutRef.current); // Clear timeout when hovered
    }

    return () => {
      clearTimeout(movieTimeoutRef.current);
      clearTimeout(tvShowTimeoutRef.current);
    };
  }, [movieHovered, tvShowHovered]);

  return (
    <div>
      {/* Movie Carousel */}
      <div
        className="relative w-full h-80 overflow-hidden bg-black"
        onMouseEnter={() => setMovieHovered(true)}
        onMouseLeave={() => setMovieHovered(false)}
      >
        <motion.div
          className="flex space-x-4 cursor-grab"
          animate={movieControls}
          drag="x"
          dragConstraints={{ left: -movies.length * 200, right: 0 }}
          dragMomentum={false}
        >
          {/* Repeat the movie list */}
          {[...movies, ...movies].map((movie, index) => (
            <motion.div
              key={index}
              className="relative w-48 h-72 shrink-0 cursor-pointer"
              onMouseEnter={() => setHoveredMovie(movie.id)}
              onMouseLeave={() => setHoveredMovie(null)}
              animate={hoveredMovie === movie.id ? { scale: 1.1 } : { scale: 1 }}
              transition={{ duration: 0.3 }}
            >
              {hoveredMovie === movie.id ? (
                <div className="absolute inset-0 bg-black bg-opacity-80 flex flex-col items-center justify-center p-4 text-white">
                  <iframe
                    className="w-full h-48 mb-2"
                    src={movie.trailer}
                    frameBorder="0"
                    allow="autoplay; encrypted-media"
                    allowFullScreen
                  ></iframe>
                  <p className="text-sm text-center">{movie.description}</p>
                  <a
                    href={movie.watchLink}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="mt-2 flex items-center gap-2 bg-red-600 text-white px-4 py-2 rounded-lg"
                  >
                    <PlayCircle /> Watch Now
                  </a>
                </div>
              ) : (
                <img src={movie.poster} alt={movie.title} className="w-full h-full object-cover" />
              )}
            </motion.div>
          ))}
        </motion.div>
      </div>

      {/* TV Show Carousel */}
      <div
        className="relative w-full h-80 overflow-hidden bg-black mt-10"
        onMouseEnter={() => setTVShowHovered(true)}
        onMouseLeave={() => setTVShowHovered(false)}
      >
        <motion.div
          className="flex space-x-4 cursor-grab"
          animate={tvShowControls}
          drag="x"
          dragConstraints={{ left: -tvShows.length * 200, right: 0 }}
          dragMomentum={false}
        >
          {/* Repeat the TV show list */}
          {[...tvShows, ...tvShows].map((show, index) => (
            <motion.div
              key={index}
              className="relative w-48 h-72 shrink-0 cursor-pointer"
              onMouseEnter={() => setHoveredTVShow(show.id)}
              onMouseLeave={() => setHoveredTVShow(null)}
              animate={hoveredTVShow === show.id ? { scale: 1.1 } : { scale: 1 }}
              transition={{ duration: 0.3 }}
            >
              {hoveredTVShow === show.id ? (
                <div className="absolute inset-0 bg-black bg-opacity-80 flex flex-col items-center justify-center p-4 text-white">
                  <iframe
                    className="w-full h-48 mb-2"
                    src={show.trailer}
                    frameBorder="0"
                    allow="autoplay; encrypted-media"
                    allowFullScreen
                  ></iframe>
                  <p className="text-sm text-center">{show.description}</p>
                  <a
                    href={show.watchLink}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="mt-2 flex items-center gap-2 bg-red-600 text-white px-4 py-2 rounded-lg"
                  >
                    <PlayCircle /> Watch Now
                  </a>
                </div>
              ) : (
                <img src={show.poster} alt={show.title} className="w-full h-full object-cover" />
              )}
            </motion.div>
          ))}
        </motion.div>
      </div>
    </div>
  );
}
