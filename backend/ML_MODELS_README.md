# Nutrition AI - Machine Learning Models

This project implements preprocessing and machine learning models to predict body composition metrics (Body Fat Percentage and Muscle Mass) based on body measurements.

## Project Structure

```
backend/
├── Data/
│   ├── Body Measurements with Features.csv  # Original dataset
│   ├── preprocessed/                        # Preprocessed data (generated)
│   │   ├── preprocessed_train.csv
│   │   └── preprocessed_test.csv
│   └── preprocessor.pkl                     # Fitted preprocessor
├── models/                                  # Trained models (generated)
│   ├── linear_regression/
│   ├── lasso_regression/
│   ├── gradient_boosting/
│   ├── xgboost/
│   ├── neural_network/
│   ├── clustering/
│   └── model_comparison.csv
├── scripts/
│   ├── run_preprocessing.py                 # Preprocess data
│   └── train_all_models.py                  # Train all models
└── src/
    ├── preprocessing/                       # Preprocessing module
    │   ├── __init__.py
    │   └── preprocessor.py
    └── models/                              # Model implementations
        ├── linear_regression/
        ├── lasso_regression/
        ├── gradient_boosting/
        ├── xgboost_model/
        ├── neural_network/
        └── clustering/
```

## Installation

1. Create and activate a virtual environment:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Install required packages:
```powershell
pip install -r requirements.txt
```

## Usage

### Step 1: Preprocess the Data

Run the preprocessing script to:
- Remove highly correlated features (multicollinearity reduction)
- Handle outliers
- Scale/normalize features
- Split into train/test sets
- Save preprocessed CSV files

```powershell
cd backend
python scripts/run_preprocessing.py
```

**Outputs:**
- `Data/preprocessed/preprocessed_train.csv` - Training data
- `Data/preprocessed/preprocessed_test.csv` - Testing data
- `Data/preprocessor.pkl` - Fitted preprocessor for inference

### Step 2: Train All Models

Train all models at once with comparison:

```powershell
python scripts/train_all_models.py
```

This will train:
1. **Linear Regression** - Baseline linear model
2. **Lasso Regression** - L1 regularization with feature selection
3. **Gradient Boosting** - Scikit-learn ensemble method
4. **XGBoost** - Advanced gradient boosting
5. **Neural Network** - Deep learning model (TensorFlow/Keras)
6. **Clustering** - Body type categorization (KMeans)

**Outputs for each model:**
- Trained model file (`.pkl` or `.keras`)
- Metrics CSV (MSE, RMSE, MAE, R²)
- Prediction plots (actual vs. predicted)
- Feature importance plots (where applicable)

**Final comparison:**
- `models/model_comparison.csv` - Performance comparison of all models

### Step 3: Train Individual Models (Optional)

Train specific models independently:

```powershell
# Linear Regression
python src/models/linear_regression/train.py

# Lasso Regression
python src/models/lasso_regression/train.py

# Neural Network
python src/models/neural_network/train.py

# Gradient Boosting
python src/models/gradient_boosting/train.py

# XGBoost
python src/models/xgboost_model/train.py

# Clustering
python src/models/clustering/train.py
```

## Model Details

### Regression Models

All regression models predict **two targets simultaneously**:
1. **Body Fat Percentage** - Percentage of body fat
2. **Muscle Mass (kg)** - Total muscle mass in kilograms

#### 1. Linear Regression
- **Type:** Multi-output linear regression
- **Use case:** Baseline model, interpretable coefficients
- **Pros:** Fast, simple, interpretable
- **Cons:** Assumes linear relationships

#### 2. Lasso Regression
- **Type:** L1 regularized regression with feature selection
- **Use case:** When you want automatic feature selection
- **Pros:** Reduces overfitting, identifies important features
- **Cons:** May underperform with highly correlated features
- **Hyperparameter:** Alpha (automatic tuning via cross-validation)

#### 3. Gradient Boosting
- **Type:** Ensemble of decision trees (scikit-learn)
- **Use case:** Strong baseline tree model
- **Pros:** Handles non-linear relationships, provides feature importance
- **Cons:** Can overfit, slower training
- **Optional:** Set `tune=True` for hyperparameter optimization

#### 4. XGBoost
- **Type:** Optimized gradient boosting implementation
- **Use case:** Often best-performing model for tabular data
- **Pros:** Fast, accurate, handles missing values
- **Cons:** More hyperparameters to tune
- **Optional:** Set `tune=True` for hyperparameter grid search

#### 5. Neural Network
- **Type:** Multi-layer perceptron (TensorFlow/Keras)
- **Architecture:** Input → 128 → 64 → 32 → 2 outputs
- **Use case:** Complex non-linear patterns
- **Pros:** Can learn complex patterns, flexible architecture
- **Cons:** Requires more data, longer training, less interpretable
- **Features:**
  - Dropout regularization (0.3)
  - Early stopping
  - Learning rate reduction on plateau
  - Automatic validation split (20%)

### Clustering Model

#### Body Type Clustering
- **Algorithm:** KMeans
- **Purpose:** Categorize individuals into body type groups
- **Features:**
  - Automatic optimal cluster selection (Elbow + Silhouette)
  - Cluster profiling with mean statistics
  - Body type naming based on body fat percentage
  - Visualization (2D PCA projection, heatmaps)
- **Typical categories:**
  - Athletic (low body fat, high muscle)
  - Fit
  - Average
  - Stocky
  - High Body Fat

## Preprocessing Details

The `DataPreprocessor` class performs:

1. **Multicollinearity Reduction**
   - Removes features with correlation > 0.95
   - Prevents model instability

2. **Outlier Handling**
   - Caps outliers at ±4 standard deviations
   - Preserves data while reducing extreme values

3. **Feature Scaling**
   - StandardScaler normalization (zero mean, unit variance)
   - Critical for neural networks and distance-based algorithms

4. **Categorical Encoding**
   - One-hot encoding for `Sex` feature
   - Drop first to avoid multicollinearity

5. **Train/Test Split**
   - 80% training, 20% testing
   - Stratified by default
   - Random seed = 42 for reproducibility

## Evaluation Metrics

All regression models report:
- **MSE** (Mean Squared Error) - Lower is better
- **RMSE** (Root Mean Squared Error) - Same units as target
- **MAE** (Mean Absolute Error) - Average prediction error
- **R²** (R-squared) - Proportion of variance explained (0-1, higher is better)

Clustering models report:
- **Silhouette Score** - Cluster separation quality (-1 to 1, higher is better)
- **Davies-Bouldin Index** - Cluster compactness (lower is better)
- **Calinski-Harabasz Index** - Ratio of between-cluster to within-cluster variance (higher is better)

## Loading Trained Models

Example code to load and use trained models:

```python
from pathlib import Path
import joblib
import pandas as pd
from tensorflow import keras

# Load preprocessor
preprocessor = joblib.load('Data/preprocessor.pkl')

# Load models
linear_model = joblib.load('models/linear_regression/linear_regression_model.pkl')
xgboost_model = joblib.load('models/xgboost/xgboost_model.pkl')
nn_model = keras.models.load_model('models/neural_network/neural_network_model.keras')
clustering_model = joblib.load('models/clustering/clustering_model.pkl')

# Make predictions on new data
new_data = pd.read_csv('new_measurements.csv')
X_scaled = preprocessor.transform(new_data)

# Predict body composition
predictions = xgboost_model.predict(X_scaled)
body_fat_pct = predictions[:, 0]
muscle_mass_kg = predictions[:, 1]

# Predict body type cluster
cluster_labels = clustering_model.predict(X_scaled)
```

## Performance Tips

1. **For best accuracy:** Use XGBoost or Neural Network with hyperparameter tuning
2. **For interpretability:** Use Lasso Regression (shows feature importance via coefficients)
3. **For speed:** Use Linear Regression or Lasso
4. **For deployment:** XGBoost offers best balance of performance and inference speed

## Customization

### Adjust Neural Network Architecture

Edit `src/models/neural_network/model.py`:
```python
model = NeuralNetworkModel(
    input_dim=X_train.shape[1],
    hidden_layers=[256, 128, 64],  # Change layer sizes
    dropout_rate=0.4  # Adjust dropout
)
```

### Change Clustering Algorithm

Edit `src/models/clustering/model.py`:
```python
model = BodyTypeClusteringModel(
    n_clusters=7,  # More clusters
    algorithm='kmeans'  # or 'dbscan'
)
```

### Tune Preprocessing

Edit `src/preprocessing/preprocessor.py`:
```python
preprocessor = DataPreprocessor(
    correlation_threshold=0.90,  # More aggressive multicollinearity removal
    outlier_std=3  # More aggressive outlier capping
)
```

## Troubleshooting

### Issue: "No module named 'tensorflow'"
**Solution:** Install TensorFlow: `pip install tensorflow>=2.13.0`

### Issue: "No module named 'xgboost'"
**Solution:** Install XGBoost: `pip install xgboost>=1.7.0`

### Issue: Neural Network taking too long
**Solution:** Reduce epochs or use smaller architecture in `neural_network/train.py`

### Issue: Memory error during training
**Solution:** Reduce batch size or use simpler models (Linear/Lasso)

## Next Steps

1. **Hyperparameter Tuning:** Set `tune=True` in XGBoost and Gradient Boosting training
2. **Ensemble Methods:** Combine predictions from multiple models
3. **Cross-Validation:** Implement K-fold CV for more robust evaluation
4. **Feature Engineering:** Add more domain-specific features
5. **Deploy Models:** Create REST API for predictions (FastAPI/Flask)

## License

This project is part of the Nutrition AI system.