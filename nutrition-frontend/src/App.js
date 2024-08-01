import React, { useState } from 'react';
import './App.css';

function App() {
  const [darkMode, setDarkMode] = useState(false);
  const [weight, setWeight] = useState(86); // Default weight
  const [height, setHeight] = useState(185); // Default height
  const [hip, setHip] = useState(87); // Default hip circumference
  const [waist, setWaist] = useState(103); // Default waist circumference
  const [age, setAge] = useState(22); // Default age
  const [exerciseDays, setExerciseDays] = useState(4); // Default exercise days
  const [email, setEmail] = useState(''); // State for email input
  const [selectedGoal, setSelectedGoal] = useState('gain-lean-muscle');
  const [selectedDiet, setSelectedDiet] = useState('any');

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
      <div className="container"> {/* Added container class */}
        <div className="input-container">
          {/* Input fields and radio buttons */}
          <div className="row">
            <label htmlFor="email" className="email-label">Email:</label>
            <input 
              id="email" 
              type="text" 
              className={`email-input ${darkMode ? 'dark-input' : 'light-input'}`}
              value={email} 
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email"
            />
          </div>
          <div className="row">
            <label htmlFor="age" className="age-label">Age:</label>
            <select 
              id="age" 
              className="age-combobox"
              value={age} 
              onChange={(e) => setAge(Number(e.target.value))}
            >
              {Array.from({ length: 100 }, (_, i) => i + 1).map(num => (
                <option key={num} value={num}>{num}</option>
              ))}
            </select>
            <label htmlFor="exerciseDays" className="exercise-label">Exercise Days per Week:</label>
            <select 
              id="exerciseDays" 
              className="exercise-combobox"
              value={exerciseDays} 
              onChange={(e) => setExerciseDays(Number(e.target.value))}
            >
              {Array.from({ length: 7 }, (_, i) => i + 1).map(num => (
                <option key={num} value={num}>{num}</option>
              ))}
            </select>
          </div>
          <div className="row">
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
          <div className="row">
            <label htmlFor="hip" className="hip-label">Hip Circumference (cm):</label>
            <select 
              id="hip" 
              className="hip-combobox"
              value={hip} 
              onChange={(e) => setHip(Number(e.target.value))}
            >
              {Array.from({ length: 200 }, (_, i) => i + 1).map(num => (
                <option key={num} value={num}>{num}</option>
              ))}
            </select>
            <label htmlFor="waist" className="waist-label">Waist Circumference (cm):</label>
            <select 
              id="waist" 
              className="waist-combobox"
              value={waist} 
              onChange={(e) => setWaist(Number(e.target.value))}
            >
              {Array.from({ length: 150 }, (_, i) => i + 1).map(num => (
                <option key={num} value={num}>{num}</option>
              ))}
            </select>
          </div>
          <div className="row">
            <div className="radio-group">
              <div className="radio-container">
                <div className="radio-label-container">
                  <label className="option-label">What is your goal?</label>
                  <div className="radio-options">
                    <label className="radio-label">
                      <input 
                        type="radio" 
                        name="goal" 
                        value="lose_weight" 
                        checked={selectedGoal === 'lose_weight'} 
                        onChange={(e) => setSelectedGoal(e.target.value)}
                      />
                      <span>Lose Weight</span>
                    </label>
                    <label className="radio-label">
                      <input 
                        type="radio" 
                        name="goal" 
                        value="gain_weight" 
                        checked={selectedGoal === 'gain_weight'} 
                        onChange={(e) => setSelectedGoal(e.target.value)}
                      />
                      <span>Gain Weight</span>
                    </label>
                    <label className="radio-label">
                      <input 
                        type="radio" 
                        name="goal" 
                        value="gain_lean_muscle" 
                        checked={selectedGoal === 'gain_lean_muscle'} 
                        onChange={(e) => setSelectedGoal(e.target.value)}
                      />
                      <span>Gain Lean Muscle</span>
                    </label>
                    <label className="radio-label">
                      <input 
                        type="radio" 
                        name="goal" 
                        value="maintain_weight" 
                        checked={selectedGoal === 'maintain_weight'} 
                        onChange={(e) => setSelectedGoal(e.target.value)}
                      />
                      <span>Maintain Weight</span>
                    </label>
                  </div>
                </div>
              </div>
              <div className="radio-container">
                <div className="radio-label-container">
                  <label className="option-label">What is your preferred diet type?</label>
                  <div className="radio-options">
                    <label className="radio-label">
                      <input 
                        type="radio" 
                        name="diet" 
                        value="paleo" 
                        checked={selectedDiet === 'paleo'} 
                        onChange={(e) => setSelectedDiet(e.target.value)}
                      />
                      <span>Paleo</span>
                    </label>
                    <label className="radio-label">
                      <input 
                        type="radio" 
                        name="diet" 
                        value="vegan" 
                        checked={selectedDiet === 'vegan'} 
                        onChange={(e) => setSelectedDiet(e.target.value)}
                      />
                      <span>Vegan</span>
                    </label>
                    <label className="radio-label">
                      <input 
                        type="radio" 
                        name="diet" 
                        value="keto" 
                        checked={selectedDiet === 'keto'} 
                        onChange={(e) => setSelectedDiet(e.target.value)}
                      />
                      <span>Keto</span>
                    </label>
                    <label className="radio-label">
                      <input 
                        type="radio" 
                        name="diet" 
                        value="mediterranean" 
                        checked={selectedDiet === 'mediterranean'} 
                        onChange={(e) => setSelectedDiet(e.target.value)}
                      />
                      <span>Mediterranean</span>
                    </label>
                    <label className="radio-label">
                      <input 
                        type="radio" 
                        name="diet" 
                        value="dash" 
                        checked={selectedDiet === 'dash'} 
                        onChange={(e) => setSelectedDiet(e.target.value)}
                      />
                      <span>Dash</span>
                    </label>
                    <label className="radio-label">
                      <input 
                        type="radio" 
                        name="diet" 
                        value="any" 
                        checked={selectedDiet === 'any'} 
                        onChange={(e) => setSelectedDiet(e.target.value)}
                      />
                      <span>Any</span>
                    </label>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="output-container">
          <h2>Output</h2>
          <p><strong>Email:</strong> {email}</p>
          <p><strong>Age:</strong> {age}</p>
          <p><strong>Exercise Days per Week:</strong> {exerciseDays}</p>
          <p><strong>Weight (kg):</strong> {weight}</p>
          <p><strong>Height (cm):</strong> {height}</p>
          <p><strong>Hip Circumference (cm):</strong> {hip}</p>
          <p><strong>Waist Circumference (cm):</strong> {waist}</p>
          <p><strong>Goal:</strong> {selectedGoal.replace(/_/g, ' ')}</p>
          <p><strong>Diet Type:</strong> {selectedDiet.replace(/_/g, ' ')}</p>
        </div>
      </div>
    </div>
  );
}

export default App;
