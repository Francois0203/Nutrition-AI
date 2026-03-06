"""
Master script to train all models and compare performance.
"""

import sys
from pathlib import Path
import time

# Add src to path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
src_path = project_root / 'src'
sys.path.insert(0, str(src_path))

import pandas as pd
import numpy as np
from models.linear_regression.model import train_linear_regression
from models.lasso_regression.model import train_lasso_regression
from models.neural_network.model import train_neural_network
from models.gradient_boosting.model import train_gradient_boosting
from models.xgboost_model.model import train_xgboost
from models.clustering.model import perform_clustering


def train_all_models():
    """Train all models and save comparison results."""
    print("="*70)
    print("TRAINING ALL MODELS")
    print("="*70)
    
    # Load preprocessed data
    data_dir = project_root / 'Data' / 'preprocessed'
    train_df = pd.read_csv(data_dir / 'preprocessed_train.csv')
    test_df = pd.read_csv(data_dir / 'preprocessed_test.csv')
    
    # Separate features and targets
    target_cols = ['BodyFatPct', 'MuscleMass_kg']
    feature_names = [col for col in train_df.columns if col not in target_cols]
    
    X_train = train_df.drop(columns=target_cols).values
    y_train = train_df[target_cols].values
    X_test = test_df.drop(columns=target_cols).values
    y_test = test_df[target_cols].values
    
    print(f"\nData Summary:")
    print(f"  Training samples: {X_train.shape[0]}")
    print(f"  Testing samples: {X_test.shape[0]}")
    print(f"  Features: {X_train.shape[1]}")
    print(f"  Targets: {y_train.shape[1]} (BodyFatPct, MuscleMass_kg)")
    
    models_dir = project_root / 'models'
    all_results = []
    
    # Train each model
    models_to_train = [
        ('Linear Regression', 'linear_regression', 
         lambda: train_linear_regression(X_train, X_test, y_train, y_test, 
                                        save_dir=models_dir / 'linear_regression')),
        
        ('Lasso Regression', 'lasso_regression',
         lambda: train_lasso_regression(X_train, X_test, y_train, y_test, 
                                        feature_names=feature_names,
                                        save_dir=models_dir / 'lasso_regression')),
        
        ('Gradient Boosting', 'gradient_boosting',
         lambda: train_gradient_boosting(X_train, X_test, y_train, y_test, 
                                        feature_names=feature_names,
                                        save_dir=models_dir / 'gradient_boosting')),
        
        ('XGBoost', 'xgboost',
         lambda: train_xgboost(X_train, X_test, y_train, y_test, 
                              feature_names=feature_names,
                              save_dir=models_dir / 'xgboost')),
        
        ('Neural Network', 'neural_network',
         lambda: train_neural_network(X_train, X_test, y_train, y_test, 
                                      epochs=100, batch_size=32,
                                      save_dir=models_dir / 'neural_network'))
    ]
    
    for model_name, model_key, train_func in models_to_train:
        print("\n" + "="*70)
        print(f"Training {model_name}")
        print("="*70)
        
        start_time = time.time()
        model = train_func()
        training_time = time.time() - start_time
        
        # Collect metrics
        for target in ['BodyFatPct', 'MuscleMass_kg']:
            test_metrics = model.metrics['Test'][target]
            all_results.append({
                'Model': model_name,
                'Target': target,
                'MSE': test_metrics['MSE'],
                'RMSE': test_metrics['RMSE'],
                'MAE': test_metrics['MAE'],
                'R2': test_metrics['R2'],
                'Training_Time_sec': training_time
            })
    
    # Create comparison DataFrame
    comparison_df = pd.DataFrame(all_results)
    
    # Print comparison
    print("\n" + "="*70)
    print("MODEL COMPARISON - TEST SET PERFORMANCE")
    print("="*70)
    
    for target in ['BodyFatPct', 'MuscleMass_kg']:
        print(f"\n{target}:")
        target_df = comparison_df[comparison_df['Target'] == target][['Model', 'RMSE', 'MAE', 'R2']]
        target_df = target_df.sort_values('R2', ascending=False)
        print(target_df.to_string(index=False))
        
        # Identify best model
        best_model = target_df.iloc[0]['Model']
        best_r2 = target_df.iloc[0]['R2']
        print(f"\n  🏆 Best model: {best_model} (R² = {best_r2:.4f})")
    
    # Save comparison
    comparison_path = models_dir / 'model_comparison.csv'
    comparison_df.to_csv(comparison_path, index=False)
    print(f"\n✅ Model comparison saved to: {comparison_path}")
    
    # Train clustering model
    print("\n" + "="*70)
    print("CLUSTERING ANALYSIS")
    print("="*70)
    
    clustering_model = perform_clustering(
        X_train, y_train,
        feature_names=feature_names,
        n_clusters=5,
        save_dir=models_dir / 'clustering'
    )
    
    print("\n" + "="*70)
    print("✅ ALL MODELS TRAINED SUCCESSFULLY!")
    print("="*70)
    print(f"\nModels saved in: {models_dir}")
    print(f"Comparison report: {comparison_path}")
    

if __name__ == '__main__':
    train_all_models()
