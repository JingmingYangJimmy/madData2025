import React from 'react';
import ReactDOM from 'react-dom';

function App() {
  const handleClick = () => {
    alert('Button clicked!');
  };

  return (
    <div>
      <h1>Hello, JSX!</h1>
      <input type="text" placeholder="Type something..." />
      <button onClick={handleClick}>Click Me!</button>
    </div>
  );
}

ReactDOM.render(<App />, document.getElementById('root'));