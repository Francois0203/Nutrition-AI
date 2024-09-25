import React from 'react';
import videoSrc from 'C:/Personal Projects/Nutrition-AI/nutrition-frontend/src/components/Nutrition-Logo.mp4';

const Page1 = ({ darkMode, email, setEmail }) => {
  return (
    <div className="page-container"> {/* Main container for page content */}
      <div className="video-container"> {/* Video container */}
        <video autoPlay loop muted className="nutrition-video"> {/* Video styling */}
          <source src={videoSrc} type="video/mp4" />
          Your browser does not support the video tag.
        </video>
      </div>

      <div className="input-container"> {/* Container for input elements */}
        <div className="label-container"> {/* Label wrapper */}
          <label htmlFor="email" className="form-label">
            Email:
          </label>
        </div>
        <div className="textbox-container"> {/* Textbox wrapper */}
          <input
            id="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className={`textbox-container input ${darkMode ? 'dark-input' : 'light-input'}`} // Conditional styling for input
            placeholder="Enter your email"
          />
        </div>
      </div>
    </div>
  );
};

export default Page1;