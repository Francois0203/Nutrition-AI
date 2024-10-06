import React from 'react';

const Page4 = ({ darkMode, output, error, handleCalculate }) => {
  return (
    <div className={`page-container ${darkMode ? 'dark-mode' : 'light-mode'}`}>
      <div className="title-container">
        <h2 className="results-title">Results</h2>
      </div>
      <div className="output-container" aria-live="polite">
        {error && <div className="error-message">{error}</div>}
        {output ? (
          <div className="results-content">
            <div className="personal-info">
              <h3 className="section-title">Personal Information</h3>
              <div className="info-item">
                <strong>BMI:</strong> <span>{output.bmi || 'N/A'}</span>
              </div>
              <div className="info-item">
                <strong>Body Fat:</strong> <span>{output.body_fat || 'N/A'}</span>
              </div>
              <div className="info-item">
                <strong>Maintenance Calories:</strong> <span>{output.main_calories || 'N/A'}</span>
              </div>
              <div className="info-item">
                <strong>Optimal Protein (g):</strong> <span>{output.optimal_protein || 'N/A'}</span>
              </div>
              <div className="info-item">
                <strong>Optimal Carbs (g):</strong> <span>{output.optimal_carbs || 'N/A'}</span>
              </div>
              <div className="info-item">
                <strong>Optimal Fats (g):</strong> <span>{output.optimal_fats || 'N/A'}</span>
              </div>
            </div>
            <div className="daily-meal-info">
              <h3 className="section-title">Daily Meal Information</h3>
              <div className="info-item">
                <strong>Total Calories:</strong> <span>{output.total_calories || 'N/A'}</span>
              </div>
              {output.meals && output.meals.length > 0 ? (
                <ul className="meal-list">
                  {output.meals.map((meal, index) => (
                    <li key={index} className="meal-item">
                      <div className="meal-details">
                        <strong>Diet Type:</strong> <span>{meal.Diet_type || 'N/A'}</span>
                      </div>
                      <div className="meal-details">
                        <strong>Recipe Name:</strong> <span>{meal.Recipe_name || 'N/A'}</span>
                      </div>
                      <div className="meal-details">
                        <strong>Protein (g):</strong> <span>{meal['Protein(g)'] || 'N/A'}</span>
                      </div>
                      <div className="meal-details">
                        <strong>Carbs (g):</strong> <span>{meal['Carbs(g)'] || 'N/A'}</span>
                      </div>
                      <div className="meal-details">
                        <strong>Fat (g):</strong> <span>{meal['Fat(g)'] || 'N/A'}</span>
                      </div>
                      <div className="meal-details">
                        <strong>Calories:</strong> <span>{meal.Calories || 'N/A'}</span>
                      </div>
                      <hr />
                    </li>
                  ))}
                </ul>
              ) : (
                <p>No meal information available.</p>
              )}
            </div>
          </div>
        ) : (
          <p>No results to display.</p>
        )}
      </div>
      <div className="button-container">
        <button className="button" onClick={handleCalculate}>Calculate Macros</button>
      </div>
    </div>
  );
};

export default Page4;