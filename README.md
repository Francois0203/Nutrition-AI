# 🏋️ Nutrition AI - Body Composition Prediction

<div align="center">

**AI-Powered Body Fat & Muscle Mass Prediction using Machine Learning**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg)](https://reactjs.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3%2B-000000.svg)](https://flask.palletsprojects.com/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.13%2B-FF6F00.svg)](https://www.tensorflow.org/)

</div>

---

## 📋 Table of Contents

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

## 🎯 Overview

Nutrition AI is a full-stack machine learning application that predicts body composition metrics (body fat percentage and muscle mass) based on body measurements. The system uses 6 different ML algorithms to provide accurate predictions and model comparisons.

### What It Does

- 📊 **Predicts** body fat percentage and muscle mass from body measurements
- 🧠 **Compares** 6 different ML models (Linear, Lasso, Gradient Boosting, XGBoost, Neural Network, K-Means)
- 📈 **Analyzes** feature importance and model performance
- 🎨 **Visualizes** predictions with a modern, responsive UI
- 🌓 **Supports** dark and light themes

---

## ✨ Features

### Backend (Python/Flask)
- ✅ 6 trained ML models ready to use
- ✅ RESTful API with CORS support
- ✅ Automatic data preprocessing
- ✅ Model performance comparison
- ✅ Feature importance analysis
- ✅ Input validation

### Frontend (React)
- ✅ Modern, responsive UI
- ✅ Dark/Light theme with system detection
- ✅ Interactive prediction form
- ✅ Model comparison dashboard
- ✅ Real-time predictions
- ✅ Toast notifications
- ✅ Error boundary for stability

---

## 🛠️ Tech Stack

### Backend
- **Python 3.8+** - Core language
- **Flask** - Web framework
- **Scikit-learn** - ML algorithms
- **XGBoost** - Gradient boosting
- **TensorFlow/Keras** - Neural networks
- **Pandas & NumPy** - Data processing

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool
- **CSS Modules** - Scoped styling
- **Fetch API** - HTTP requests

---

## 🚀 Quick Start

Get the entire application running in 3 steps:

### Prerequisites

- **Python 3.8+** and pip
- **Node.js 16+** and npm
- **Git** (to clone the repository)

### Step 1: Clone & Setup Backend

```bash
# Clone the repository
git clone https://github.com/Francois0203/Nutrition-AI.git
cd Nutrition-AI/backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\Activate.ps1
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run automated setup (preprocessing + training)
python setup.py
```

The setup script will:
- ✓ Preprocess the data
- ✓ Train all 6 ML models
- ✓ Generate model comparisons
- ✓ Verify everything is ready

This takes **5-10 minutes** depending on your hardware.

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

# Install dependencies
npm install

# Create environment file
cp .env.example .env

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

### 🎉 You're Ready!

Open your browser to `http://localhost:5173` and start making predictions!

---

## 📚 Detailed Setup

### Backend Setup (Detailed)

#### 1. Environment Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate       # macOS/Linux

# Install all dependencies
pip install -r requirements.txt
```

#### 2. Data Preprocessing

```bash
python scripts/run_preprocessing.py
```

This creates:
- `Data/preprocessed/preprocessed_train.csv`
- `Data/preprocessed/preprocessed_test.csv`
- `Data/preprocessor.pkl`

#### 3. Train Models

```bash
python scripts/train_all_models.py
```

This trains all models and creates:
- `models/linear_regression/` - Linear Regression model
- `models/lasso_regression/` - Lasso model
- `models/gradient_boosting/` - Gradient Boosting model
- `models/xgboost/` - XGBoost model
- `models/neural_network/` - Neural Network model
- `models/clustering/` - K-Means clustering
- `models/model_comparison.csv` - Performance comparison

#### 4. Start API Server

```bash
python app.py
```

#### 5. Test API

```bash
# Health check
curl http://localhost:5000/api/health

# Get available models
curl http://localhost:5000/api/models

# Get model comparison
curl http://localhost:5000/api/models/comparison
```

### Frontend Setup (Detailed)

#### 1. Install Dependencies

```bash
cd frontend
npm install
```

#### 2. Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env if needed (default is correct)
# VITE_API_BASE_URL=http://localhost:5000/api
```

#### 3. Start Development Server

```bash
npm run dev
```

App available at: `http://localhost:5173`

#### 4. Build for Production

```bash
npm run build
npm run preview
```

---

## 📖 Usage Guide

### Making Predictions

1. **Navigate to Predict Page**
   - Click "Predict" in the navigation menu

2. **Enter Measurements**
   - Required: Age, Sex, Height, Weight
   - Optional: Waist, Hip, Chest, Neck, etc.
   - Use "Fill Sample" button for test data

3. **Select Model**
   - Choose "All Models" to compare
   - Or select a specific model

4. **Get Results**
   - Click "Get Predictions"
   - View body fat percentage and muscle mass

### Viewing Model Performance

1. **Navigate to Models Page**
   - Click "Models" in navigation

2. **Review Metrics**
   - MAE (Mean Absolute Error)
   - RMSE (Root Mean Square Error)
   - R² Score (0-1, higher is better)

3. **View Details**
   - Click any model card
   - See feature importance
   - Read model descriptions

### Understanding the Process

1. **Navigate to About Page**
   - Learn about data collection
   - Understand preprocessing steps
   - See model training process

---

## 🔌 API Documentation

### Base URL

```
http://localhost:5000/api
```

### Endpoints

#### Health Check
```http
GET /api/health
```

Response:
```json
{
  "status": "ok",
  "models_loaded": 5,
  "available_models": ["linear_regression", "xgboost", ...],
  "preprocessor_loaded": true
}
```

#### Get All Models
```http
GET /api/models
```

#### Get Model Comparison
```http
GET /api/models/comparison
```

Response:
```json
{
  "models": [
    {
      "name": "XGBoost",
      "mae": 3.2,
      "rmse": 4.5,
      "r2": 0.93,
      "description": "Advanced gradient boosting"
    },
    ...
  ]
}
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
    "Hip_cm": 100,
    ...
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

{
  "measurements": { ... }
}
```

Response:
```json
{
  "models": {
    "linear_regression": {
      "body_fat_percentage": 19.2,
      "muscle_mass": 59.8
    },
    "xgboost": {
      "body_fat_percentage": 18.5,
      "muscle_mass": 60.2
    },
    ...
  },
  "success": true
}
```

#### Validate Measurements
```http
POST /api/validate
Content-Type: application/json

{
  "measurements": { ... }
}
```

#### Get Data Statistics
```http
GET /api/data/stats
```

---

## 📁 Project Structure

```
Nutrition-AI/
├── backend/
│   ├── app.py                    # Flask API server ⭐
│   ├── setup.py                  # Automated setup script ⭐
│   ├── requirements.txt          # Python dependencies
│   ├── .env.example             # Environment variables template
│   ├── Data/
│   │   ├── Body Measurements.csv          # Training data
│   │   ├── preprocessor.pkl              # Trained preprocessor
│   │   └── preprocessed/                 # Processed data
│   ├── models/                           # Trained models
│   │   ├── linear_regression/
│   │   ├── lasso_regression/
│   │   ├── gradient_boosting/
│   │   ├── xgboost/
│   │   ├── neural_network/
│   │   ├── clustering/
│   │   └── model_comparison.csv
│   ├── scripts/
│   │   ├── run_preprocessing.py          # Data preprocessing
│   │   ├── train_all_models.py           # Train all models
│   │   └── ...
│   ├── src/
│   │   ├── preprocessing/                # Preprocessing modules
│   │   ├── models/                       # Model implementations
│   │   └── features/                     # Feature engineering
│   └── utils/                            # Utility functions
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx                       # Main app component
│   │   ├── main.jsx                      # Entry point
│   │   ├── components/                   # Reusable components
│   │   │   ├── Error Boundary/
│   │   │   ├── Navigation Bar/
│   │   │   ├── Settings/
│   │   │   ├── Toast Notifications/
│   │   │   └── ...
│   │   ├── pages/                        # Page components
│   │   │   ├── Home.jsx                  # Landing page
│   │   │   ├── Predict.jsx               # Prediction form
│   │   │   ├── Models.jsx                # Model comparison
│   │   │   └── About.jsx                 # Information page
│   │   ├── services/
│   │   │   └── api.js                    # API client ⭐
│   │   ├── hooks/
│   │   │   └── useTheme.js               # Theme management
│   │   └── styles/                       # Global styles
│   ├── package.json                      # Node dependencies
│   ├── .env.example                      # Frontend env template
│   └── vite.config.js                    # Vite configuration
│
└── README.md                             # This file ⭐
```

---

## 🧠 Models

### 1. Linear Regression
- **Type:** Linear model
- **Use:** Baseline comparison
- **Speed:** ⚡ Very fast
- **Accuracy:** ⭐⭐⭐

### 2. Lasso Regression
- **Type:** Linear with L1 regularization
- **Use:** Feature selection
- **Speed:** ⚡ Very fast
- **Accuracy:** ⭐⭐⭐⭐

### 3. Gradient Boosting
- **Type:** Ensemble (Decision Trees)
- **Use:** Robust predictions
- **Speed:** ⚡⚡ Fast
- **Accuracy:** ⭐⭐⭐⭐

### 4. XGBoost
- **Type:** Optimized gradient boosting
- **Use:** Best overall performance
- **Speed:** ⚡⚡ Fast
- **Accuracy:** ⭐⭐⭐⭐⭐

### 5. Neural Network
- **Type:** Deep learning
- **Use:** Complex patterns
- **Speed:** ⚡⚡⚡ Medium
- **Accuracy:** ⭐⭐⭐⭐⭐

### 6. K-Means Clustering
- **Type:** Unsupervised learning
- **Use:** Body type categorization
- **Speed:** ⚡ Very fast
- **Accuracy:** ⭐⭐⭐

---

## 💻 Development

### Backend Development

```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # macOS/Linux

# Run with auto-reload
python app.py
# Or
flask run --reload

# Run tests
pytest tests/

# Format code
black .
flake8 .
```

### Frontend Development

```bash
# Start dev server with hot reload
npm run dev

# Run linter
npm run lint

# Format code
npm run format

# Build for production
npm run build

# Preview production build
npm run preview
```

### Adding New Features

#### Backend: Add New API Endpoint

```python
# In backend/app.py
@app.route('/api/your-endpoint', methods=['GET', 'POST'])
def your_function():
    # Your logic here
    return jsonify({'result': 'data'})
```

#### Frontend: Add New Page

```jsx
// In frontend/src/pages/YourPage.jsx
import { useTheme } from '../hooks/useTheme';
import styles from './YourPage.module.css';

const YourPage = () => {
  const { theme } = useTheme();
  
  return (
    <div className={styles.container} data-theme={theme}>
      {/* Your content */}
    </div>
  );
};

export default YourPage;
```

---

## 🔧 Troubleshooting

### Backend Issues

#### ❌ Models Not Found

**Problem:** API returns "No models loaded"

**Solution:**
```bash
cd backend
python setup.py
# Or manually:
python scripts/run_preprocessing.py
python scripts/train_all_models.py
```

#### ❌ Import Errors

**Problem:** `ModuleNotFoundError`

**Solution:**
```bash
# Make sure venv is activated
pip install -r requirements.txt
```

#### ❌ Port 5000 Already in Use

**Problem:** "Address already in use"

**Solution:**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:5000 | xargs kill -9
```

### Frontend Issues

#### ❌ API Connection Failed

**Problem:** Cannot connect to backend

**Solution:**
1. Check backend is running: `http://localhost:5000/api/health`
2. Verify `.env` has correct URL: `VITE_API_BASE_URL=http://localhost:5000/api`
3. Check CORS is enabled in `app.py`
4. Clear browser cache and restart dev server

#### ❌ Module Not Found

**Problem:** "Cannot find module"

**Solution:**
```bash
rm -rf node_modules package-lock.json
npm install
```

#### ❌ npm install Fails

**Problem:** Package installation errors

**Solution:**
```bash
# Clear npm cache
npm cache clean --force

# Use different registry
npm install --registry=https://registry.npmjs.org/

# Update npm
npm install -g npm@latest
```

### Common Issues

#### ❌ Predictions Are Inaccurate

**Causes:**
- Models not properly trained
- Input features missing or incorrect
- Preprocessor not loaded

**Solution:**
```bash
# Retrain models
cd backend
python setup.py
# Choose option 2 to retrain
```

#### ❌ Theme Not Switching

**Solution:**
- Clear browser localStorage
- Check browser console for errors
- Verify theme CSS variables in `Theme.css`

---

## 🚀 Deployment

### Backend Deployment

**Options:**
- Heroku
- Google Cloud Run
- AWS Elastic Beanstalk
- DigitalOcean App Platform

**Example (Heroku):**
```bash
# Install Heroku CLI
heroku create nutrition-ai-api
git push heroku main
```

### Frontend Deployment

**Options:**
- Vercel (recommended)
- Netlify
- GitHub Pages
- AWS S3 + CloudFront

**Example (Vercel):**
```bash
# Install Vercel CLI
npm install -g vercel
cd frontend
vercel
```

---

## 📝 License

MIT License - feel free to use this project for learning or commercial purposes.

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

## 🙏 Acknowledgments

- Training data from body composition research
- ML models built with Scikit-learn, XGBoost, and TensorFlow
- UI components inspired by modern web design principles

---

<div align="center">

**Built with ❤️ using Python, React, and Machine Learning**

⭐ Star this repo if you find it useful!

</div>
