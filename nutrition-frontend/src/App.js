import React, { useState, useEffect } from 'react';
import './App.css';
import Page1 from './components/Page1';
import Page2 from './components/Page2';
import Page3 from './components/Page3';
import Page4 from './components/Page4';

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

  const toggleTheme = () => {
    setDarkMode(prevMode => !prevMode);
  };

  // Effect to apply dark mode class to body
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
      <div className="title-container">
        <h1 className="title-container">Nutrition AI</h1>
      </div>
      <div className="switch-container">
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
      {renderPage()}
      <div className="button-container">
        <button className="button" onClick={handlePrevPage} disabled={currentPage === 1}>Previous</button>
        <button className="button" onClick={handleNextPage} disabled={currentPage === 4}>Next</button>
      </div>
    </div>
  );
}

export default App;