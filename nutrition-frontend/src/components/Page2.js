import React from 'react';

const Page2 = ({
  darkMode,
  weight,
  setWeight,
  height,
  setHeight,
  hip,
  setHip,
  waist,
  setWaist,
  age,
  setAge,
  exerciseDays,
  setExerciseDays,
  isMale,
  setIsMale
}) => {
  return (
    <div className="page-container"> {/* Changed to page-container */}
      <div className="title-container">
        <h2 className="page-title">Body Measurements</h2>
      </div>

      <div className="input-container"> {/* Changed to input-container */}
        <div className="radiogroup-container form-row"> {/* Changed to radiogroup-container */}
          <label htmlFor="age" className="form-label">Age:</label>
          <select 
            id="age" 
            value={age} 
            onChange={(e) => setAge(Number(e.target.value))} 
            className={`combobox-container ${darkMode ? 'dark-select' : 'light-select'}`} 
          >
            {Array.from({ length: 100 }, (_, i) => i + 1).map(num => (
              <option key={num} value={num}>{num}</option>
            ))}
          </select>
        </div>

        <div className="form-row">
          <label htmlFor="weight" className="form-label">Weight (kg):</label>
          <select 
            id="weight" 
            value={weight} 
            onChange={(e) => setWeight(Number(e.target.value))} 
            className={`combobox-container ${darkMode ? 'dark-select' : 'light-select'}`} 
          >
            {Array.from({ length: 150 }, (_, i) => i + 1).map(num => (
              <option key={num} value={num}>{num}</option>
            ))}
          </select>

          <label htmlFor="height" className="form-label">Height (cm):</label>
          <select 
            id="height" 
            value={height} 
            onChange={(e) => setHeight(Number(e.target.value))} 
            className={`combobox-container ${darkMode ? 'dark-select' : 'light-select'}`} 
          >
            {Array.from({ length: 250 }, (_, i) => i + 1).map(num => (
              <option key={num} value={num}>{num}</option>
            ))}
          </select>
        </div>

        <div className="form-row">
          <label htmlFor="hip" className="form-label">Hip Circumference (cm):</label>
          <select 
            id="hip" 
            value={hip} 
            onChange={(e) => setHip(Number(e.target.value))} 
            className={`combobox-container ${darkMode ? 'dark-select' : 'light-select'}`} 
          >
            {Array.from({ length: 200 }, (_, i) => i + 1).map(num => (
              <option key={num} value={num}>{num}</option>
            ))}
          </select>

          <label htmlFor="waist" className="form-label">Waist Circumference (cm):</label>
          <select 
            id="waist" 
            value={waist} 
            onChange={(e) => setWaist(Number(e.target.value))} 
            className={`combobox-container ${darkMode ? 'dark-select' : 'light-select'}`} 
          >
            {Array.from({ length: 150 }, (_, i) => i + 1).map(num => (
              <option key={num} value={num}>{num}</option>
            ))}
          </select>
        </div>

        <div className="form-row">
          <label className="form-label">Gender:</label>
          <div className="switch-container form-gender-toggle"> {/* Changed to switch-container */}
            <input 
              type="checkbox" 
              checked={isMale} 
              onChange={(e) => setIsMale(e.target.checked)} 
              className="gender-checkbox"
            />
            <span className="gender-label">{isMale ? 'Male' : 'Female'}</span>
          </div>
        </div>

        <div className="form-row">
          <label htmlFor="exerciseDays" className="form-label">Exercise Days per Week:</label>
          <select 
            id="exerciseDays" 
            value={exerciseDays} 
            onChange={(e) => setExerciseDays(Number(e.target.value))} 
            className={`combobox-container ${darkMode ? 'dark-select' : 'light-select'}`} 
          >
            {Array.from({ length: 7 }, (_, i) => i + 1).map(num => (
              <option key={num} value={num}>{num}</option>
            ))}
          </select>
        </div>
      </div>
    </div>
  );
};

export default Page2;