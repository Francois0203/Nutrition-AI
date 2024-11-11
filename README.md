# Nutrition-AI Project

## Table of Contents
- [Project Description](#project-description)
- [Components](#components)
  - [Frontend](#frontend)
  - [Backend](#backend)
  - [Random Forest Models](#random-forest-models)
- [Limitations](#limitations)
- [Packages Used](#packages-used)
- [License](#license)

## Project Description
The Nutrition-AI project is a web-based application designed to provide personalized nutrition recommendations based on a user’s health data. The project features a multi-page frontend built with React, providing an interactive user experience. The frontend communicates seamlessly with a Flask backend that calculates various health metrics and suggests meal plans based on the user's information, including weight, height, age, gender, exercise habits, and body measurements such as waist and hip circumference. The backend also incorporates machine learning models to predict body fat and muscle mass percentages using random forest algorithms.

## Components

### Frontend
The frontend of the Nutrition-AI project is developed with React, a JavaScript library that allows for the creation of dynamic, interactive user interfaces. The design follows a multi-page layout, with each page offering specific functionalities such as health data input, metric display, and meal recommendations.

Key features of the frontend include:
- **Dynamic Components**: React components are used to create reusable UI elements, enhancing maintainability and responsiveness.
- **Background Integration**: A background design is implemented to ensure an engaging and visually appealing user experience.
- **Interactive User Input**: Users can input personal health data, which is sent to the backend for processing and analysis.
- **Responsive Design**: The frontend is designed to be responsive across different screen sizes, ensuring accessibility for users on both desktop and mobile devices.

### Backend
The backend of the Nutrition-AI project is built with Flask, a lightweight Python web framework. Flask handles the user requests, performs calculations, and returns the necessary data to the frontend. 

Key functionalities of the backend:
- **Health Metrics Calculation**: The backend calculates key health metrics such as Body Mass Index (BMI), Body Adiposity Index (BAI), and Waist-to-Hip Ratio (WHR) based on user-provided data.
- **Meal Recommendations**: Based on the health metrics, the backend generates tailored meal recommendations to help the user achieve their health goals. 
- **Data Management**: The backend handles user input data securely and processes it efficiently to ensure accurate recommendations.
- **Flask-CORS Integration**: The `flask_cors` package is used to enable cross-origin resource sharing (CORS), allowing the frontend to interact with the backend from different origins.

### Random Forest Models
To predict body fat percentage and muscle mass percentage, the backend integrates two machine learning models trained using random forest algorithms. These models help provide personalized health predictions based on user input.

- **Data Generation**: The training data for the random forest models is synthetically generated using statistical models, including Gaussian and uniform distributions. This allows for the creation of a diverse dataset that can be adjusted to match specific population characteristics.
  - The dataset is designed to represent real-world distributions of health metrics.
  - The generated data can be customized based on mean and standard deviation values that reflect the target population.
  
- **Model Training**: The random forest models are trained using the generated data to predict body fat and muscle mass percentages.
- **Prediction**: The trained models are used to generate predictions based on user input, adding a layer of personalization to the health assessments.

## Limitations
- **Data Generation**: Since the random forest models are trained using generated data, their accuracy might be limited compared to models trained on real-world datasets. The data distribution may not perfectly reflect all populations.
- **Meal Recommendations**: The meal recommendation system does not account for financial constraints, as it is not connected to live datasets with up-to-date pricing information.

## Packages Used
- `pandas`: Data manipulation and analysis, especially for handling user input and generating synthetic datasets.
- `numpy`: Numerical operations, such as array manipulation and mathematical calculations.
- `scikit-learn`: Machine learning library for building and training random forest models.
- `flask`: Web framework for creating the backend of the application.
- `flask_cors`: Enables Cross-Origin Resource Sharing (CORS) for the Flask app.
- `pulp`: A linear programming library used for solving optimization problems related to meal planning.
- `matplotlib`: Visualization library for creating graphs and charts to display health metrics and model results.
- `tabulate`: Used to present data in tabular format, enhancing the readability of outputs.
- `seaborn`: Statistical data visualization library used for creating more advanced plots and graphs.

## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
