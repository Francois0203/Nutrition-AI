# Quick Start Guide - ML Preprocessing and Training

## Summary

✅ **Preprocessing Complete!**

Your data has been successfully preprocessed and is ready for model training.

### What Was Done

1. **Feature Engineering**: Started with 43 features
2. **Multicollinearity Removal**: Removed 4 highly correlated features:
   - `bsa_mosteller`
   - `fat_mass_index`
   - `abdominal_volume_index`
   - `hip_waist_difference`
3. **Outlier Handling**: Capped 40 outlier values (±4 standard deviations)
4. **Feature Scaling**: Normalized all features using StandardScaler
5. **Data Split**: 80/20 train/test split
   - Training: 1,600 samples
   - Testing: 400 samples
   - Final features: 37

### Generated Files

```
backend/
├── Data/
│   ├── preprocessed/
│   │   ├── preprocessed_train.csv  ✅ (1,600 rows × 39 columns)
│   │   └── preprocessed_test.csv   ✅ (400 rows × 39 columns)
│   └── preprocessor.pkl            ✅ (Fitted StandardScaler & settings)
```

Both CSV files contain:
- **37 normalized features** (all numerical, scaled)
- **2 target columns**: `BodyFatPct`, `MuscleMass_kg`

---

## Next Steps: Train Models

### Option 1: Train All Models at Once (Recommended)

This will train all 5 regression models + clustering and generate a comparison report:

```powershell
cd c:\Projects\Nutrition-AI\backend
.\venv\Scripts\Activate.ps1
python scripts\train_all_models.py
```

**Expected output:**
- Trained models in `backend/models/` (each in its own folder)
- Performance metrics for each model
- Prediction plots (actual vs. predicted)
- Feature importance plots (for tree-based models)
- `model_comparison.csv` with side-by-side metrics

**Estimated time:**
- Linear Regression: < 1 second
- Lasso Regression: ~5 seconds (includes hyperparameter tuning)
- Gradient Boosting: ~10-30 seconds
- XGBoost: ~10-30 seconds
- Neural Network: 2-5 minutes (100 epochs with early stopping)
- Clustering: ~5 seconds

**Total: ~5-10 minutes**

---

### Option 2: Train Individual Models

Train specific models one at a time:

#### Linear Regression (Fastest)
```powershell
python src\models\linear_regression\train.py
```

#### Lasso Regression (with feature selection)
```powershell
python src\models\lasso_regression\train.py
```

#### Gradient Boosting
```powershell
python src\models\gradient_boosting\train.py
```

#### XGBoost (Often best performance)
```powershell
python src\models\xgboost_model\train.py
```

#### Neural Network (Deep Learning)
```powershell
python src\models\neural_network\train.py
```

#### Clustering (Body Type Categorization)
```powershell
python src\models\clustering\train.py
```

---

## Understanding the Output

### Model Metrics

Each model will show:

```
============================================================
[MODEL NAME] - Test Set Metrics
============================================================

BodyFatPct:
  MSE: [value]      # Mean Squared Error (lower is better)
  RMSE: [value]     # Root Mean Squared Error (in % units)
  MAE: [value]      # Mean Absolute Error (average error in %)
  R2: [value]       # R-squared (0-1, closer to 1 is better)

MuscleMass_kg:
  MSE: [value]
  RMSE: [value]     # In kg units
  MAE: [value]      # Average error in kg
  R2: [value]       # Proportion of variance explained
```

### Interpreting R² Scores

- **0.90-1.00**: Excellent prediction
- **0.80-0.90**: Very good
- **0.70-0.80**: Good
- **0.60-0.70**: Acceptable
- **< 0.60**: May need improvement

---

## Expected Results

Based on typical performance with similar datasets:

| Model | Body Fat % R² | Muscle Mass R² | Speed |
|-------|---------------|----------------|-------|
| **XGBoost** | ~0.85-0.92 | ~0.90-0.95 | Fast |
| **Gradient Boosting** | ~0.83-0.90 | ~0.88-0.93 | Fast |
| **Neural Network** | ~0.82-0.90 | ~0.87-0.92 | Slow |
| **Lasso** | ~0.75-0.85 | ~0.82-0.88 | Very Fast |
| **Linear Regression** | ~0.73-0.82 | ~0.80-0.87 | Very Fast |

**Note:** XGBoost and Gradient Boosting typically perform best on this type of tabular data.

---

## Model Outputs

After training, each model folder contains:

```
models/
└── [model_name]/
    ├── [model_name]_model.pkl/.keras   # Trained model
    ├── [model_name]_metrics.csv        # Performance metrics
    ├── [model_name]_predictions.png    # Actual vs. Predicted plot
    └── [model_name]_feature_importance.png  # (if applicable)
```

### Clustering Output

```
models/
└── clustering/
    ├── clustering_model.pkl        # Trained KMeans model
    ├── cluster_profiles.csv        # Statistics for each body type
    ├── clustering_2d.png           # 2D visualization (PCA projection)
    └── clustering_heatmap.png      # Feature profiles heatmap
```

---

## Using Trained Models

### Load and Make Predictions

```python
import joblib
import pandas as pd
from tensorflow import keras

# Load preprocessor
preprocessor = joblib.load('Data/preprocessor.pkl')

# Load your best model (e.g., XGBoost)
model = joblib.load('models/xgboost/xgboost_model.pkl')

# Load new data
new_data = pd.read_csv('new_measurements.csv')

# Preprocess
X_scaled = preprocessor.transform(new_data)

# Predict
predictions = model.predict(X_scaled)
body_fat_pct = predictions[:, 0]
muscle_mass_kg = predictions[:, 1]

print(f"Body Fat %: {body_fat_pct}")
print(f"Muscle Mass (kg): {muscle_mass_kg}")
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'sklearn'"

**Solution:**
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Issue: Neural Network training is very slow

**Solution:** Edit `src/models/neural_network/train.py` and reduce epochs:
```python
model = train_neural_network(
    X_train, X_test, y_train, y_test,
    epochs=50,  # Reduced from 100
    batch_size=32,
    save_dir=save_dir
)
```

### Issue: Out of memory

**Solution:** Train models individually instead of all at once, or use simpler models (Linear, Lasso).

---

## Next Actions

1. **Train all models**: `python scripts\train_all_models.py`
2. **Review comparison**: Open `models/model_comparison.csv`
3. **Choose best model**: Based on R² scores for your targets
4. **Deploy**: Integrate the best model into your application

---

## Additional Resources

- **Full Documentation**: See `ML_MODELS_README.md` for detailed information
- **Preprocessing Details**: See `src/preprocessing/preprocessor.py`
- **Model Code**: Browse `src/models/[model_name]/model.py`

---

**Status: Ready to train! 🚀**
