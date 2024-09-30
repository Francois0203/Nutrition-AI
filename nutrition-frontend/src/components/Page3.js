import React from 'react';

const Page3 = ({ darkMode, selectedDiet, setSelectedDiet, selectedGoal, setSelectedGoal }) => {
  return (
    <div className={`page-container ${darkMode ? 'dark-mode' : 'light-mode'}`}>
      <div className="title-container">
        <h2 className="page-title">Select Your Goals and Diet Type</h2>
      </div>

      <div className="input-container">
        <div className="radiogroup-container">
          <h3 className="section-title">Your Goal:</h3>
          {['lose_weight', 'gain_weight', 'gain_lean_muscle', 'maintain_weight'].map((goal) => (
            <div className="radio-option" key={goal}>
              <label className={`radio-label ${darkMode ? 'dark-label' : 'light-label'}`}>
                <input
                  type="radio"
                  name="goal"
                  value={goal}
                  checked={selectedGoal === goal}
                  onChange={(e) => setSelectedGoal(e.target.value)}
                  className="radio-input"
                />
                {goal.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase())}
              </label>
            </div>
          ))}
        </div>

        <div className="radiogroup-container">
          <h3 className="section-title">Preferred Diet Type:</h3>
          {['paleo', 'vegan', 'keto', 'mediterranean', 'dash', 'any'].map((diet) => (
            <div className="radio-option" key={diet}>
              <label className={`radio-label ${darkMode ? 'dark-label' : 'light-label'}`}>
                <input
                  type="radio"
                  name="diet"
                  value={diet}
                  checked={selectedDiet === diet}
                  onChange={(e) => setSelectedDiet(e.target.value)}
                  className="radio-input"
                />
                {diet.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase())}
              </label>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Page3;