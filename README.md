# Nutrition AI — Body Composition Prediction

<div align="center">

A full-stack machine learning application that predicts body fat percentage and muscle mass from body measurements, comparing 6 ML algorithms with a modern React frontend.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg)](https://reactjs.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3%2B-000000.svg)](https://flask.palletsprojects.com/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.13%2B-FF6F00.svg)](https://www.tensorflow.org/)

</div>

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Detailed Setup](#detailed-setup)
- [Usage Guide](#usage-guide)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Models](#models)
- [Development](#development)
- [Troubleshooting](#troubleshooting)

---

## Overview

Nutrition AI is a full-stack machine learning application that predicts body composition metrics (body fat percentage and muscle mass) based on body measurements. The system uses 6 different ML algorithms to provide accurate predictions and model comparisons.

### What It Does

- Predicts body fat percentage and muscle mass from body measurements
- Compares 6 different ML models (Linear, Lasso, Gradient Boosting, XGBoost, Neural Network, K-Means)
- Analyzes feature importance and model performance
- Visualizes predictions with a modern, responsive UI
- Supports dark and light themes

---

## Features

- Predicts body fat percentage and muscle mass from body measurements
- Compares 6 ML models with MAE, RMSE, and R² performance metrics
- RESTful Flask API with automatic data preprocessing and input validation
- Modern responsive UI with dark/light theme and real-time predictions

## Tech Stack

`Python · Flask · Scikit-learn · XGBoost · TensorFlow · Pandas · NumPy · React · Vite · CSS Modules`

---

## Quick Start

Get the entire application running in 3 steps:

### Prerequisites

- **Python 3.8+** and pip
- **Node.js 16+** and npm
- **Git** (to clone the repository)

### Step 1: Clone & Setup Backend

```bash
git clone https://github.com/Francois0203/Nutrition-AI.git
cd Nutrition-AI/backend

python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\Activate.ps1
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt

# Run automated setup (preprocessing + training)
python setup.py
```

The setup script will preprocess the data, train all 6 ML models, generate model comparisons, and verify everything is ready. This takes **5-10 minutes** depending on your hardware.

### Step 2: Start Backend API Server

```bash
# Make sure you're in backend/ directory with venv activated
python app.py
```

The API will be available at `http://localhost:5000`

### Step 3: Setup & Start Frontend

Open a **new terminal**:

```bash
cd Nutrition-AI/frontend
npm install
cp .env.example .env
npm run dev
```

The frontend will be available at `http://localhost:5173`

---

## Detailed Setup

### Backend Setup

#### 1. Environment Setup

```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate       # macOS/Linux
pip install -r requirements.txt
```

#### 2. Data Preprocessing

```bash
python scripts/run_preprocessing.py
```

Creates:
- `Data/preprocessed/preprocessed_train.csv`
- `Data/preprocessed/preprocessed_test.csv`
- `Data/preprocessor.pkl`

#### 3. Train Models

```bash
python scripts/train_all_models.py
```

Creates trained models in `models/` and `models/model_comparison.csv`.

#### 4. Start API Server

```bash
python app.py
```

#### 5. Test API

```bash
curl http://localhost:5000/api/health
curl http://localhost:5000/api/models
curl http://localhost:5000/api/models/comparison
```

### Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env
# Edit .env if needed: VITE_API_BASE_URL=http://localhost:5000/api
npm run dev
```

Build for production:

```bash
npm run build
npm run preview
```

---

## Usage Guide

### Making Predictions

1. Navigate to the **Predict** page
2. Enter measurements (Age, Sex, Height, Weight required; Waist, Hip, Chest, Neck optional)
3. Use **Fill Sample** to populate test data
4. Select a model or choose **All Models** to compare
5. Click **Get Predictions** to view body fat percentage and muscle mass

### Viewing Model Performance

Navigate to the **Models** page to review MAE, RMSE, and R² scores. Click any model card to see feature importance and a description of the algorithm.

---

## API Documentation

### Base URL

```
http://localhost:5000/api
```

### Endpoints

#### Health Check
```http
GET /api/health
```

#### Get All Models
```http
GET /api/models
```

#### Get Model Comparison
```http
GET /api/models/comparison
```

#### Predict with Specific Model
```http
POST /api/predict/{model_name}
Content-Type: application/json

{
  "measurements": {
    "Age": 35,
    "Sex": "Male",
    "Height_cm": 175,
    "Weight_kg": 80,
    "Waist_cm": 90,
    "Hip_cm": 100
  }
}
```

Response:
```json
{
  "model": "XGBoost",
  "body_fat_percentage": 18.5,
  "muscle_mass": 60.2,
  "success": true
}
```

#### Predict with All Models
```http
POST /api/predict/all
Content-Type: application/json

{ "measurements": { ... } }
```

#### Validate Measurements
```http
POST /api/validate
Content-Type: application/json

{ "measurements": { ... } }
```

#### Get Data Statistics
```http
GET /api/data/stats
```

---

## Project Structure

```
Nutrition-AI/
├── backend/
│   ├── app.py                    # Flask API server
│   ├── setup.py                  # Automated setup script
│   ├── requirements.txt
│   ├── Data/
│   │   ├── Body Measurements.csv
│   │   ├── preprocessor.pkl
│   │   └── preprocessed/
│   ├── models/
│   │   ├── linear_regression/
│   │   ├── lasso_regression/
│   │   ├── gradient_boosting/
│   │   ├── xgboost/
│   │   ├── neural_network/
│   │   ├── clustering/
│   │   └── model_comparison.csv
│   ├── scripts/
│   │   ├── run_preprocessing.py
│   │   └── train_all_models.py
│   └── src/
│       ├── preprocessing/
│       ├── models/
│       └── features/
│
└── frontend/
    └── src/
        ├── App.jsx
        ├── components/
        ├── pages/
        │   ├── Home.jsx
        │   ├── Predict.jsx
        │   ├── Models.jsx
        │   └── About.jsx
        ├── services/
        │   └── api.js
        └── hooks/
            └── useTheme.js
```

---

## Models

| Model | Type | Accuracy |
|---|---|---|
| Linear Regression | Linear baseline | ⭐⭐⭐ |
| Lasso Regression | Linear + L1 regularization | ⭐⭐⭐⭐ |
| Gradient Boosting | Ensemble (Decision Trees) | ⭐⭐⭐⭐ |
| XGBoost | Optimized gradient boosting | ⭐⭐⭐⭐⭐ |
| Neural Network | Deep learning | ⭐⭐⭐⭐⭐ |
| K-Means Clustering | Unsupervised (body type categorization) | ⭐⭐⭐ |

---

## Development

### Backend

```bash
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # macOS/Linux

python app.py        # Run with auto-reload
pytest tests/        # Run tests
black .              # Format code
flake8 .             # Lint
```

### Frontend

```bash
npm run dev          # Dev server with hot reload
npm run lint         # Linter
npm run build        # Production build
npm run preview      # Preview production build
```

---

## Troubleshooting

### Models not found

```bash
cd backend
python setup.py
```

### Import errors

```bash
pip install -r requirements.txt  # ensure venv is activated
```

### Port 5000 already in use

```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:5000 | xargs kill -9
```

### API connection failed

1. Confirm backend is running: `http://localhost:5000/api/health`
2. Check `.env`: `VITE_API_BASE_URL=http://localhost:5000/api`
3. Verify CORS is enabled in `app.py`

### Module not found (frontend)

```bash
rm -rf node_modules package-lock.json
npm install
```

---

## Deployment

**Backend:** Heroku, Google Cloud Run, AWS Elastic Beanstalk, DigitalOcean App Platform

**Frontend:** Vercel (recommended), Netlify, GitHub Pages

---

## License

MIT License — free to use for learning or commercial purposes.

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## Acknowledgments

- Training data from body composition research
- ML models built with Scikit-learn, XGBoost, and TensorFlow
- UI inspired by modern web design principles
