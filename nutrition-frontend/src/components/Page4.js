import React from 'react';
const Page4 = ({ darkMode, output, error, handleCalculate }) => {
  return (
    <div className="page-container">
      <div className="title-container">
        <h2>Results</h2>
      </div>
      <div className="output-container">
        {error && <div className="textbox-container error-container">{error}</div>}
        {output && (
          <>
            <div className="personal-info">
              <div className="title-container">
                <h3>Personal Information</h3>
              </div>
              <div className="textbox-container">
                <p><div className="label-container"><strong>BMI:</strong></div> {output.bmi || 'N/A'}</p>
                <p><div className="label-container"><strong>Body Fat:</strong></div> {output.body_fat || 'N/A'}</p>
                <p><div className="label-container"><strong>Maintenance Calories:</strong></div> {output.main_calories || 'N/A'}</p>
                <p><div className="label-container"><strong>Optimal Protein (g):</strong></div> {output.optimal_protein || 'N/A'}</p>
                <p><div className="label-container"><strong>Optimal Carbs (g):</strong></div> {output.optimal_carbs || 'N/A'}</p>
                <p><div className="label-container"><strong>Optimal Fats (g):</strong></div> {output.optimal_fats || 'N/A'}</p>
              </div>
            </div>
            <div className="daily-meal-info">
              <div className="title-container">
                <h3>Daily Meal Information</h3>
              </div>
              <div className="textbox-container">
                <p><div className="label-container"><strong>Total Calories:</strong></div> {output.total_calories || 'N/A'}</p>
                {output.meals && output.meals.length > 0 ? (
                  <ul>
                    {output.meals.map((meal, index) => (
                      <li key={index}>
                        <p><div className="label-container"><strong>Diet Type:</strong></div> {meal.Diet_type || 'N/A'}</p>
                        <p><div className="label-container"><strong>Recipe Name:</strong></div> {meal.Recipe_name || 'N/A'}</p>
                        <p><div className="label-container"><strong>Protein (g):</strong></div> {meal['Protein(g)'] || 'N/A'}</p>
                        <p><div className="label-container"><strong>Carbs (g):</strong></div> {meal['Carbs(g)'] || 'N/A'}</p>
                        <p><div className="label-container"><strong>Fat (g):</strong></div> {meal['Fat(g)'] || 'N/A'}</p>
                        <p><div className="label-container"><strong>Calories:</strong></div> {meal.Calories || 'N/A'}</p>
                        <hr />
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
      <div className="button-container">
        <button className="button" onClick={handleCalculate}>Calculate Macros</button>
      </div>
    </div>
  );
};
export default Page4;