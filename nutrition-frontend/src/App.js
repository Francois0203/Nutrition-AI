import React, { useState } from 'react';
import './App.css';

function App() {
  const [darkMode, setDarkMode] = useState(false);
  const [weight, setWeight] = useState(87); // Default weight
  const [height, setHeight] = useState(185); // Default height
  const [email, setEmail] = useState(''); // State for email input

  const toggleTheme = () => {
    setDarkMode(!darkMode);
  };

  return (
    <div className={`App ${darkMode ? 'dark-mode' : 'light-mode'}`}>
      <h1 className="animated-title">Nutrition AI</h1>
      <div className="switch-container">
        <label className="switch">
          <input type="checkbox" onChange={toggleTheme} checked={darkMode} />
          <span className="slider round"></span>
        </label>
        <span className="mode-label">{darkMode ? 'Dark Mode' : 'Light Mode'}</span>
      </div>
      <div className="input-container">
        <label htmlFor="email" className="email-label">Email:</label>
        <input 
          id="email" 
          type="text" 
          className={`email-input ${darkMode ? 'dark-input' : 'light-input'}`}
          value={email} 
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Enter your email"
        />
        <label htmlFor="weight" className="weight-label">Weight (kg):</label>
        <select 
          id="weight" 
          className="weight-combobox"
          value={weight} 
          onChange={(e) => setWeight(Number(e.target.value))}
        >
          {Array.from({ length: 150 }, (_, i) => i + 1).map(num => (
            <option key={num} value={num}>{num}</option>
          ))}
        </select>
        <label htmlFor="height" className="height-label">Height (cm):</label>
        <select 
          id="height" 
          className="height-combobox"
          value={height} 
          onChange={(e) => setHeight(Number(e.target.value))}
        >
          {Array.from({ length: 250 }, (_, i) => i + 1).map(num => (
            <option key={num} value={num}>{num}</option>
          ))}
        </select>
      </div>
    </div>
  );
}

export default App;
