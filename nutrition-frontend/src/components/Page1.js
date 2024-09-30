import React from 'react';
import videoSrc from 'C:/Personal Projects/Nutrition-AI/nutrition-frontend/src/components/Nutrition-Logo.mp4';

const Page1 = ({ darkMode, email, setEmail }) => {
  return (
    <div className={`page-container ${darkMode ? 'dark-mode' : 'light-mode'}`}>
      <div className="video-container">
        <video autoPlay loop muted className="nutrition-video">
          <source src={videoSrc} type="video/mp4" />
          Your browser does not support the video tag.
        </video>
      </div>

      <div className="input-container">
        <div className="label-container">
          <label htmlFor="email" className="form-label">
            Email:
          </label>
        </div>
        <div className="textbox-container">
          <input
            id="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className={`textbox-container input ${darkMode ? 'dark-input' : 'light-input'}`}
            placeholder="Enter your email"
          />
        </div>
      </div>
    </div>
  );
};

export default Page1;