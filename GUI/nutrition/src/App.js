import React, { useState } from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
  const [darkMode, setDarkMode] = useState(false);

  const toggleTheme = () => {
    setDarkMode(!darkMode);
  };

  return (
    <div className={`App ${darkMode ? 'dark-mode' : 'light-mode'}`}>
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
      <div className="switch-container">
        <label className="switch">
          <input type="checkbox" onChange={toggleTheme} checked={darkMode} />
          <span className="slider round"></span>
        </label>
        <span className="mode-label">{darkMode ? 'Dark Mode' : 'Light Mode'}</span>
      </div>
    </div>
  );
}

export default App;
