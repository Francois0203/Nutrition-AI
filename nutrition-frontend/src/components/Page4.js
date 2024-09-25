import React from 'react';

const Page4 = ({ darkMode, output, error, handleCalculate }) => {
  return (
    <div className="page-container"> {/* Container for the page */}
      <div className="title-container">
        <h2 className="page-title">Results</h2>
      </div>

      <div className="output-container"> {/* Container for output results */}
        {error && <div className="error-container">{error}</div>}
        {output && (
          <>
            <div className="personal-info">
              <h3 className="section-title">Personal Information</h3>
              <div className="info-container">
                <p><strong>BMI:</strong> <span className="highlight">{output.bmi || 'N/A'}</span></p>
                <p><strong>Body Fat:</strong> <span className="highlight">{output.body_fat || 'N/A'}</span></p>
                <p><strong>Maintenance Calories:</strong> <span className="highlight">{output.main_calories || 'N/A'}</span></p>
                <p><strong>Optimal Protein (g):</strong> <span className="highlight">{output.optimal_protein || 'N/A'}</span></p>
                <p><strong>Optimal Carbs (g):</strong> <span className="highlight">{output.optimal_carbs || 'N/A'}</span></p>
                <p><strong>Optimal Fats (g):</strong> <span className="highlight">{output.optimal_fats || 'N/A'}</span></p>
              </div>
            </div>

            <div className="daily-meal-info">
              <h3 className="section-title">Daily Meal Information</h3>
              <div className="info-container">
                <p><strong>Total Calories:</strong> <span className="highlight">{output.total_calories || 'N/A'}</span></p>
                {output.meals && output.meals.length > 0 ? (
                  <ul className="meal-list">
                    {output.meals.map((meal, index) => (
                      <li key={index} className="meal-item">
                        <p><strong>Diet Type:</strong> {meal.Diet_type || 'N/A'}</p>
                        <p><strong>Recipe Name:</strong> {meal.Recipe_name || 'N/A'}</p>
                        <p><strong>Protein (g):</strong> {meal['Protein(g)'] || 'N/A'}</p>
                        <p><strong>Carbs (g):</strong> {meal['Carbs(g)'] || 'N/A'}</p>
                        <p><strong>Fat (g):</strong> {meal['Fat(g)'] || 'N/A'}</p>
                        <p><strong>Calories:</strong> {meal.Calories || 'N/A'}</p>
                        <hr className="meal-divider" />
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p>No meal information available.</p>
                )}
              </div>
            </div>
          </>
        )}
      </div>

      <div className="button-container"> {/* Container for buttons */}
        <button className="calculate-button" onClick={handleCalculate}>
          Calculate Macros
        </button>
      </div>
    </div>
  );
};

export default Page4;