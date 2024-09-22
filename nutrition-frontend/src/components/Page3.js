import React from 'react';

const Page3 = ({ darkMode, selectedDiet, setSelectedDiet, selectedGoal, setSelectedGoal }) => {
  return (
    <div className="page-container">
      <div className="title-container">
        <h2>Select Your Goals and Diet Type</h2>
      </div>
      <div className="input-container">
        <div className="radiogroup-container">
          <div className="title-container">
            <h3>Your Goal:</h3>
          </div>
          {['lose_weight', 'gain_weight', 'gain_lean_muscle', 'maintain_weight'].map((goal) => (
            <div className="label-container" key={goal}>
              <label>
                <input
                  type="radio"
                  name="goal"
                  value={goal}
                  checked={selectedGoal === goal}
                  onChange={(e) => setSelectedGoal(e.target.value)}
                />
                {goal.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase())}
              </label>
            </div>
          ))}
        </div>
        <div className="radiogroup-container">
          <div className="title-container">
            <h3>Preferred Diet Type:</h3>
          </div>
          {['paleo', 'vegan', 'keto', 'mediterranean', 'dash', 'any'].map((diet) => (
            <div className="label-container" key={diet}>
              <label>
                <input
                  type="radio"
                  name="diet"
                  value={diet}
                  checked={selectedDiet === diet}
                  onChange={(e) => setSelectedDiet(e.target.value)}
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