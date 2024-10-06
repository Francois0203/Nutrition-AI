import React, { useState, useEffect } from 'react';
import './App.css'; // Link to the CSS file
import Page1 from './components/Page1';
import Page2 from './components/Page2';
import Page3 from './components/Page3';
import Page4 from './components/Page4';
import darkVideoSrc from './components/Dark-Background.mp4'; 
import lightVideoSrc from './components/Light-Background.mp4';

function App() {
  const [darkMode, setDarkMode] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const [weight, setWeight] = useState(86);
  const [height, setHeight] = useState(185);
  const [hip, setHip] = useState(87);
  const [waist, setWaist] = useState(103);
  const [age, setAge] = useState(22);
  const [exerciseDays, setExerciseDays] = useState(4);
  const [email, setEmail] = useState('');
  const [selectedGoal, setSelectedGoal] = useState('gain_lean_muscle');
  const [selectedDiet, setSelectedDiet] = useState('any');
  const [output, setOutput] = useState(null);
  const [error, setError] = useState(null);
  const [isMale, setIsMale] = useState(true);
  const [loading, setLoading] = useState(false);

  const toggleTheme = () => {
    setDarkMode((prevMode) => !prevMode);
  };

  useEffect(() => {
    document.body.classList.toggle('dark-mode', darkMode);
    document.body.classList.toggle('light-mode', !darkMode);
  }, [darkMode]);

  const handleNextPage = () => {
    setCurrentPage((prev) => Math.min(prev + 1, 4));
  };

  const handlePrevPage = () => {
    setCurrentPage((prev) => Math.max(prev - 1, 1));
  };

  const handleCalculate = async () => {
    setError(null);
    setLoading(true);
    try {
      const response = await fetch('http://localhost:5000/calculate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          weight,
          height,
          hip,
          waist,
          age,
          exerciseDays,
          goal: selectedGoal,
          diet: selectedDiet,
          email,
          gender: isMale ? 1 : 0,
        }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      setOutput(data);
    } catch (error) {
      setError('There was an error processing your request. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const renderPage = () => {
    switch (currentPage) {
      case 1:
        return <Page1 darkMode={darkMode} email={email} setEmail={setEmail} />;
      case 2:
        return (
          <Page2
            darkMode={darkMode}
            weight={weight}
            setWeight={setWeight}
            height={height}
            setHeight={setHeight}
            hip={hip}
            setHip={setHip}
            waist={waist}
            setWaist={setWaist}
            age={age}
            setAge={setAge}
            exerciseDays={exerciseDays}
            setExerciseDays={setExerciseDays}
            isMale={isMale}
            setIsMale={setIsMale}
          />
        );
      case 3:
        return (
          <Page3
            darkMode={darkMode}
            selectedDiet={selectedDiet}
            setSelectedDiet={setSelectedDiet}
            selectedGoal={selectedGoal}
            setSelectedGoal={setSelectedGoal}
          />
        );
      case 4:
        return (
          <Page4
            darkMode={darkMode}
            output={output}
            error={error}
            handleCalculate={handleCalculate}
          />
        );
      default:
        return null;
    }
  };

  return (
    <div className={`App ${darkMode ? 'dark-mode' : 'light-mode'}`}>
      <video key={darkMode ? 'dark' : 'light'} autoPlay loop muted className="background-video">
        <source src={darkMode ? darkVideoSrc : lightVideoSrc} type="video/mp4" />
        Your browser does not support the video tag.
      </video>

      <div className="header">
        <h1 className="title animated-title">Nutrition AI</h1>
      </div>

      <div className="theme-toggle-checkbox">
        <label className="switch">
          <input 
            type="checkbox" 
            onChange={toggleTheme} 
            checked={darkMode} 
          />
          <span className="slider"></span>
        </label>
        <span className="mode-label">{darkMode ? 'Dark Mode' : 'Light Mode'}</span>
      </div>

      <div className="content">
        {loading ? <p>Loading...</p> : renderPage()}
        {error && <div className="error-message">{error}</div>}
      </div>

      <div className="navigation">
        <button 
          className="button prev" 
          onClick={handlePrevPage} 
          disabled={currentPage === 1} 
          aria-label="Previous page"
        >
          Previous
        </button>
        <button 
          className="button next" 
          onClick={handleNextPage} 
          disabled={currentPage === 4} 
          aria-label="Next page"
        >
          Next
        </button>
      </div>
    </div>
  );
}

export default App;