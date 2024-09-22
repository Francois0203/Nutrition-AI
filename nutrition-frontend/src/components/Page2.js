import React from 'react';

const Page2 = ({ darkMode, weight, setWeight, height, setHeight, hip, setHip, waist, setWaist, age, setAge, exerciseDays, setExerciseDays, isMale, setIsMale }) => {
  return (
    <div className="page-container">
      <div className="title-container">
        <h2>Body Measurements</h2>
      </div>
      <div className="input-container">
        <div className="row">
          <div className="label-container">
            <label htmlFor="age">Age:</label>
          </div>
          <div className="combobox-container">
            <select id="age" value={age} onChange={(e) => setAge(Number(e.target.value))}>
              {Array.from({ length: 100 }, (_, i) => i + 1).map(num => (
                <option key={num} value={num}>{num}</option>
              ))}
            </select>
          </div>
        </div>
        <div className="row">
          <div className="label-container">
            <label htmlFor="weight">Weight (kg):</label>
          </div>
          <div className="combobox-container">
            <select id="weight" value={weight} onChange={(e) => setWeight(Number(e.target.value))}>
              {Array.from({ length: 150 }, (_, i) => i + 1).map(num => (
                <option key={num} value={num}>{num}</option>
              ))}
            </select>
          </div>
          <div className="label-container">
            <label htmlFor="height">Height (cm):</label>
          </div>
          <div className="combobox-container">
            <select id="height" value={height} onChange={(e) => setHeight(Number(e.target.value))}>
              {Array.from({ length: 250 }, (_, i) => i + 1).map(num => (
                <option key={num} value={num}>{num}</option>
              ))}
            </select>
          </div>
        </div>
        <div className="row">
          <div className="label-container">
            <label htmlFor="hip">Hip Circumference (cm):</label>
          </div>
          <div className="combobox-container">
            <select id="hip" value={hip} onChange={(e) => setHip(Number(e.target.value))}>
              {Array.from({ length: 200 }, (_, i) => i + 1).map(num => (
                <option key={num} value={num}>{num}</option>
              ))}
            </select>
          </div>
          <div className="label-container">
            <label htmlFor="waist">Waist Circumference (cm):</label>
          </div>
          <div className="combobox-container">
            <select id="waist" value={waist} onChange={(e) => setWaist(Number(e.target.value))}>
              {Array.from({ length: 150 }, (_, i) => i + 1).map(num => (
                <option key={num} value={num}>{num}</option>
              ))}
            </select>
          </div>
        </div>
        <div className="row">
          <div className="label-container">
            <label>Gender:</label>
          </div>
          <div className="checkbox-container">
            <input 
              type="checkbox" 
              checked={isMale} 
              onChange={(e) => setIsMale(e.target.checked)} 
            />
            <span>{isMale ? 'Male' : 'Female'}</span>
          </div>
        </div>
        <div className="row">
          <div className="label-container">
            <label htmlFor="exerciseDays">Exercise Days per Week:</label>
          </div>
          <div className="combobox-container">
            <select id="exerciseDays" value={exerciseDays} onChange={(e) => setExerciseDays(Number(e.target.value))}>
              {Array.from({ length: 7 }, (_, i) => i + 1).map(num => (
                <option key={num} value={num}>{num}</option>
              ))}
            </select>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Page2;