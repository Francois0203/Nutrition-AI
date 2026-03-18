"""
Train Lasso Regression model.
"""

import sys
from pathlib import Path

# Add src to path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent.parent.parent
src_path = project_root / 'src'
sys.path.insert(0, str(src_path))

import pandas as pd
import numpy as np
from models.lasso_regression.model import train_lasso_regression


def main():
    """Main training script for Lasso Regression."""
    print("="*70)
    print("LASSO REGRESSION MODEL TRAINING")
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
    
    print(f"\nTraining data shape: {X_train.shape}")
    print(f"Testing data shape: {X_test.shape}")
    
    # Train model
    save_dir = project_root / 'models' / 'lasso_regression'
    model = train_lasso_regression(
        X_train, X_test, y_train, y_test, 
        feature_names=feature_names,
        save_dir=save_dir
    )
    
    print("\n✅ Lasso Regression training complete!")


if __name__ == '__main__':
    main()
