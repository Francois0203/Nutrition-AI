"""
Nutrition AI - Flask API Server
Serves trained ML models for body composition prediction
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import joblib
import pandas as pd
import numpy as np
from pathlib import Path
import traceback

# Add backend directory to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Add src directory to path (needed for loading preprocessor)
src_dir = backend_dir / 'src'
sys.path.insert(0, str(src_dir))

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Model paths
MODELS_DIR = backend_dir / 'models'
DATA_DIR = backend_dir / 'Data'
PREPROCESSOR_PATH = DATA_DIR / 'preprocessor.pkl'

# Global model storage
models = {}
preprocessor = None
model_comparison = None

# Model name mapping
MODEL_NAMES = {
    'linear_regression': 'Linear Regression',
    'lasso_regression': 'Lasso Regression',
    'gradient_boosting': 'Gradient Boosting',
    'xgboost': 'XGBoost',
    'neural_network': 'Neural Network'
}

def load_models():
    """Load all trained models and preprocessor"""
    global models, preprocessor, model_comparison
    
    print("Loading models...")
    
    # Load preprocessor
    if PREPROCESSOR_PATH.exists():
        try:
            preprocessor = joblib.load(PREPROCESSOR_PATH)
            print(f"✓ Loaded preprocessor")
        except Exception as e:
            print(f"✗ Error loading preprocessor: {e}")
            print("  This usually means the preprocessor needs to be retrained.")
            print("  Run: python setup.py")
            preprocessor = None
    else:
        print(f"⚠ Warning: Preprocessor not found at {PREPROCESSOR_PATH}")
        print("  Run: python scripts/run_preprocessing.py")
    
    # Load each model
    for model_key, model_name in MODEL_NAMES.items():
        model_path = MODELS_DIR / model_key / f'{model_key}_model.pkl'
        keras_model_path = MODELS_DIR / model_key / f'{model_key}_model.keras'
        
        try:
            if keras_model_path.exists():
                # Load Keras model
                from tensorflow import keras
                models[model_key] = keras.models.load_model(keras_model_path)
                print(f"✓ Loaded {model_name} (Keras)")
            elif model_path.exists():
                # Load scikit-learn/xgboost model
                models[model_key] = joblib.load(model_path)
                print(f"✓ Loaded {model_name}")
            else:
                print(f"⚠ Warning: {model_name} not found")
        except Exception as e:
            print(f"✗ Error loading {model_name}: {e}")
    
    # Load model comparison if available
    comparison_path = MODELS_DIR / 'model_comparison.csv'
    if comparison_path.exists():
        try:
            model_comparison = pd.read_csv(comparison_path)
            print(f"✓ Loaded model comparison data")
        except Exception as e:
            print(f"⚠ Could not load model comparison: {e}")
    
    if not models:
        print("\n⚠ WARNING: No models loaded!")
        print("Please train models first:")
        print("  cd backend")
        print("  python scripts/run_preprocessing.py")
        print("  python scripts/train_all_models.py\n")
    else:
        print(f"\n✓ Successfully loaded {len(models)} models\n")

def engineer_features_for_inference(measurements):
    """
    Engineer all features from raw measurements for model inference.
    
    Since some features in training were derived from the target variables
    (BodyFatPct, MuscleMass_kg), we estimate them using validated formulas
    before computing the derived features.
    """
    m = measurements  # alias for brevity
    
    height_cm = float(m.get('Height_cm', 0))
    weight_kg = float(m.get('Weight_kg', 0))
    age       = float(m.get('Age', 0))
    sex       = str(m.get('Sex', 'Male')).strip().lower()
    sex_m     = 1 if sex in ('male', 'm', '1') else 0
    
    height_m = height_cm / 100.0 if height_cm else 1
    
    # ── Estimate BodyFatPct (Deurenberg 1991 formula) ─────────────────────────
    bmi = weight_kg / (height_m ** 2) if height_m else 0
    # BF% = 1.20 × BMI + 0.23 × Age − 10.8 × sex_m − 5.4
    estimated_bf_pct = 1.20 * bmi + 0.23 * age - 10.8 * sex_m - 5.4
    estimated_bf_pct = max(3.0, min(60.0, estimated_bf_pct))  # clamp to plausible range
    
    # ── Estimate MuscleMass_kg ────────────────────────────────────────────────
    # Lean body mass ~ 85% of fat-free mass for males, 75% for females
    fat_mass_kg  = weight_kg * (estimated_bf_pct / 100.0)
    lean_mass_kg = weight_kg - fat_mass_kg
    muscle_fraction = 0.52 if sex_m else 0.46   # approximate skeletal-muscle fraction
    estimated_muscle_kg = lean_mass_kg * muscle_fraction
    
    # Helper reads
    wrist_cm    = float(m.get('Wrist_cm',    0))
    waist_cm    = float(m.get('Waist_cm',    0))
    hip_cm      = float(m.get('Hip_cm',      0))
    neck_cm     = float(m.get('Neck_cm',     0))
    upper_arm   = float(m.get('UpperArm_cm', 0))
    thigh_cm    = float(m.get('Thigh_cm',    0))
    calf_cm     = float(m.get('Calf_cm',     0))
    forearm_cm  = float(m.get('Forearm_cm',  0))
    chest_cm    = float(m.get('Chest_cm',    0))
    shoulder_cm = float(m.get('Shoulder_cm', 0))
    ankle_cm    = float(m.get('Ankle_cm',    0))
    bicep_cm    = float(m.get('Bicep_cm',    0))
    
    def safe_div(a, b, default=0.0):
        return a / b if b else default
    
    # ── All engineered features (match training order) ────────────────────────
    features = {
        'Age':                    age,
        'Height_cm':              height_cm,
        'Weight_kg':              weight_kg,
        'Wrist_cm':               wrist_cm,
        'Waist_cm':               waist_cm,
        'Hip_cm':                 hip_cm,
        'Neck_cm':                neck_cm,
        'UpperArm_cm':            upper_arm,
        'Thigh_cm':               thigh_cm,
        'Calf_cm':                calf_cm,
        'Forearm_cm':             forearm_cm,
        'Chest_cm':               chest_cm,
        'Shoulder_cm':            shoulder_cm,
        'Ankle_cm':               ankle_cm,
        'Bicep_cm':               bicep_cm,
        # Body composition indices
        'bmi':                    bmi,
        'bsa_mosteller':          np.sqrt(height_cm * weight_kg / 3600) if height_cm and weight_kg else 0,
        'fat_mass_kg':            fat_mass_kg,
        'lean_mass_kg':           lean_mass_kg,
        'fat_mass_index':         safe_div(fat_mass_kg,  height_m ** 2),
        'ffmi':                   safe_div(lean_mass_kg, height_m ** 2),
        # Obesity / adiposity ratios
        'waist_hip_ratio':                safe_div(waist_cm, hip_cm),
        'waist_height_ratio':             safe_div(waist_cm, height_cm),
        'body_adiposity_index':           safe_div(hip_cm, height_m ** 1.5) - 18,
        'conicity_index':                 safe_div(waist_cm, 0.109 * np.sqrt(safe_div(weight_kg, height_m))),
        'abdominal_volume_index':         (2 * waist_cm**2 + 0.7 * (waist_cm - hip_cm)**2) / 1000,
        'waist_neck_ratio':               safe_div(waist_cm, neck_cm),
        # Limb proportions
        'upper_lower_limb_ratio':         safe_div(upper_arm,  thigh_cm),
        'calf_thigh_ratio':               safe_div(calf_cm,    thigh_cm),
        'arm_trunk_ratio':                safe_div(upper_arm,  waist_cm),
        'forearm_upper_arm_ratio':        safe_div(forearm_cm, upper_arm),
        'shoulder_waist_ratio':           safe_div(shoulder_cm, waist_cm),
        'hip_waist_difference':           hip_cm - waist_cm,
        'chest_waist_ratio':              safe_div(chest_cm, waist_cm),
        # Muscle & frame
        'frame_size_index':               safe_div(wrist_cm, height_cm) * 100,
        'relative_muscle_mass':           safe_div(estimated_muscle_kg, weight_kg) * 100,
        'muscle_to_fat_ratio':            safe_div(estimated_muscle_kg, fat_mass_kg),
        'skeletal_muscle_index':          safe_div(estimated_muscle_kg, height_m ** 2),
        'bicep_to_wrist_ratio':           safe_div(bicep_cm, wrist_cm),
        'calf_muscle_index':              safe_div(calf_cm, height_cm) * 100,
        # One-hot encoded sex
        'Sex_M':                  float(sex_m),
    }
    
    return features


def preprocess_input(measurements):
    """Preprocess input measurements for prediction"""
    # Build full feature set (including engineered + encoded features)
    features = engineer_features_for_inference(measurements)
    df = pd.DataFrame([features])
    
    # Apply preprocessor if available (handles correlation removal + scaling)
    if preprocessor is not None:
        try:
            # Drop target columns if somehow present, then apply transform
            df_input = df.drop(columns=['BodyFatPct', 'MuscleMass_kg'], errors='ignore')
            df_input = df_input.drop(columns=['Sex'], errors='ignore')
            # Align to expected feature columns
            for col in preprocessor.feature_columns:
                if col not in df_input.columns:
                    df_input[col] = 0.0
            df_input = df_input[preprocessor.feature_columns]
            return preprocessor.scaler.transform(df_input)
        except Exception as e:
            print(f"Preprocessor error: {e}")
            # Fall back: drop non-numeric cols and return raw values
            df_num = df.select_dtypes(include=[np.number])
            return df_num.values
    else:
        # No preprocessor - return feature values directly
        df_num = df.select_dtypes(include=[np.number])
        return df_num.values

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'models_loaded': len(models),
        'available_models': list(models.keys()),
        'preprocessor_loaded': preprocessor is not None
    })

@app.route('/api/models', methods=['GET'])
def get_models():
    """Get list of available models"""
    available_models = []
    for model_key, model_name in MODEL_NAMES.items():
        available_models.append({
            'key': model_key,
            'name': model_name,
            'loaded': model_key in models
        })
    
    return jsonify({
        'models': available_models,
        'total': len(available_models),
        'loaded': len(models)
    })

@app.route('/api/models/comparison', methods=['GET'])
def get_model_comparison():
    """Get model performance comparison"""
    if model_comparison is None:
        # Return mock data if no comparison available
        return jsonify({
            'models': [
                {
                    'name': 'Linear Regression',
                    'mae': 4.2,
                    'rmse': 5.8,
                    'r2': 0.85,
                    'description': 'Baseline linear model'
                },
                {
                    'name': 'Lasso Regression',
                    'mae': 4.0,
                    'rmse': 5.5,
                    'r2': 0.87,
                    'description': 'L1 regularization with feature selection'
                },
                {
                    'name': 'Gradient Boosting',
                    'mae': 3.5,
                    'rmse': 4.8,
                    'r2': 0.91,
                    'description': 'Ensemble method with boosting'
                },
                {
                    'name': 'XGBoost',
                    'mae': 3.2,
                    'rmse': 4.5,
                    'r2': 0.93,
                    'description': 'Advanced gradient boosting'
                },
                {
                    'name': 'Neural Network',
                    'mae': 3.4,
                    'rmse': 4.6,
                    'r2': 0.92,
                    'description': 'Deep learning model'
                }
            ],
            'note': 'Mock data - train models to get real metrics'
        })
    
    # Parse actual comparison data
    models_data = []
    for _, row in model_comparison.iterrows():
        models_data.append({
            'name': row.get('Model', 'Unknown'),
            'mae': float(row.get('MAE', 0)),
            'rmse': float(row.get('RMSE', 0)),
            'r2': float(row.get('R2', 0)),
            'description': MODEL_NAMES.get(row.get('Model', '').lower().replace(' ', '_'), '')
        })
    
    return jsonify({'models': models_data})

@app.route('/api/models/<model_name>', methods=['GET'])
def get_model_info(model_name):
    """Get detailed information about a specific model"""
    if model_name not in models:
        return jsonify({'error': f'Model {model_name} not found'}), 404
    
    model_info = {
        'name': MODEL_NAMES.get(model_name, model_name),
        'key': model_name,
        'loaded': True,
        'description': f'Trained {MODEL_NAMES.get(model_name, model_name)} model'
    }
    
    # Add model-specific information
    model = models[model_name]
    if hasattr(model, 'feature_importances_'):
        # For tree-based models
        model_info['has_feature_importance'] = True
    elif hasattr(model, 'coef_'):
        # For linear models
        model_info['has_coefficients'] = True
    
    return jsonify(model_info)

@app.route('/api/predict/<model_name>', methods=['POST'])
def predict_single(model_name):
    """Get prediction from a specific model"""
    if model_name not in models:
        return jsonify({'error': f'Model {model_name} not found or not loaded'}), 404
    
    try:
        data = request.json
        measurements = data.get('measurements', data)
        
        # Preprocess input
        X = preprocess_input(measurements)
        
        # Get model
        model = models[model_name]
        
        # Make prediction
        prediction = model.predict(X)
        
        # Handle different prediction formats
        if prediction.shape[1] == 2:
            # Two outputs: body fat and muscle mass
            body_fat = float(prediction[0][0])
            muscle_mass = float(prediction[0][1])
        else:
            # Single output - assume body fat percentage
            body_fat = float(prediction[0])
            # Estimate muscle mass from weight and body fat
            weight = measurements.get('Weight_kg', 0)
            muscle_mass = weight * (1 - body_fat / 100) if weight else 0
        
        return jsonify({
            'model': MODEL_NAMES.get(model_name, model_name),
            'body_fat_percentage': round(body_fat, 2),
            'muscle_mass': round(muscle_mass, 2),
            'success': True
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc(),
            'success': False
        }), 400

@app.route('/api/predict/all', methods=['POST'])
def predict_all():
    """Get predictions from all available models"""
    try:
        data = request.json
        measurements = data.get('measurements', data)
        
        if not models:
            return jsonify({
                'error': 'No models loaded. Please train models first.',
                'success': False
            }), 503
        
        # Preprocess input once
        X = preprocess_input(measurements)
        
        # Get predictions from all models
        results = {}
        for model_key, model in models.items():
            try:
                prediction = model.predict(X)
                
                # Handle different prediction formats
                if len(prediction.shape) > 1 and prediction.shape[1] == 2:
                    body_fat = float(prediction[0][0])
                    muscle_mass = float(prediction[0][1])
                else:
                    body_fat = float(prediction[0])
                    weight = measurements.get('Weight_kg', 0)
                    muscle_mass = weight * (1 - body_fat / 100) if weight else 0
                
                results[model_key] = {
                    'body_fat_percentage': round(body_fat, 2),
                    'muscle_mass': round(muscle_mass, 2)
                }
            except Exception as e:
                results[model_key] = {
                    'error': str(e),
                    'body_fat_percentage': None,
                    'muscle_mass': None
                }
        
        return jsonify({
            'models': results,
            'success': True
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc(),
            'success': False
        }), 400

@app.route('/api/validate', methods=['POST'])
def validate_measurements():
    """Validate input measurements"""
    try:
        data = request.json
        measurements = data.get('measurements', data)
        
        # Required fields
        required = ['Age', 'Sex', 'Height_cm', 'Weight_kg']
        missing = [field for field in required if field not in measurements or measurements[field] == '']
        
        if missing:
            return jsonify({
                'valid': False,
                'errors': missing,
                'message': f'Missing required fields: {", ".join(missing)}'
            }), 400
        
        # Validate ranges
        errors = []
        if measurements.get('Age', 0) < 1 or measurements.get('Age', 0) > 120:
            errors.append('Age must be between 1 and 120')
        if measurements.get('Height_cm', 0) < 50 or measurements.get('Height_cm', 0) > 300:
            errors.append('Height must be between 50 and 300 cm')
        if measurements.get('Weight_kg', 0) < 20 or measurements.get('Weight_kg', 0) > 500:
            errors.append('Weight must be between 20 and 500 kg')
        
        if errors:
            return jsonify({
                'valid': False,
                'errors': errors,
                'message': 'Validation failed'
            }), 400
        
        return jsonify({
            'valid': True,
            'message': 'Measurements are valid'
        })
        
    except Exception as e:
        return jsonify({
            'valid': False,
            'error': str(e)
        }), 400

@app.route('/api/data/stats', methods=['GET'])
def get_data_stats():
    """Get dataset statistics"""
    try:
        # Load original dataset
        data_path = DATA_DIR / 'Body Measurements.csv'
        if not data_path.exists():
            return jsonify({'error': 'Dataset not found'}), 404
        
        df = pd.read_csv(data_path)
        
        stats = {
            'total_samples': len(df),
            'features': len(df.columns),
            'feature_names': df.columns.tolist(),
            'summary': df.describe().to_dict()
        }
        
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("Nutrition AI - API Server")
    print("=" * 60)
    
    # Load models on startup
    load_models()
    
    print("Starting Flask server...")
    print("API available at: http://localhost:5000")
    print("Health check: http://localhost:5000/api/health")
    print("=" * 60)
    
    # Run the server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
