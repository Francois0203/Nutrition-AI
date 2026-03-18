"""
Train Neural Network model.
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
from models.neural_network.model import train_neural_network


def main():
    """Main training script for Neural Network."""
    print("="*70)
    print("NEURAL NETWORK MODEL TRAINING")
    print("="*70)
    
    # Load preprocessed data
    data_dir = project_root / 'Data' / 'preprocessed'
    train_df = pd.read_csv(data_dir / 'preprocessed_train.csv')
    test_df = pd.read_csv(data_dir / 'preprocessed_test.csv')
    
    # Separate features and targets
    target_cols = ['BodyFatPct', 'MuscleMass_kg']
    X_train = train_df.drop(columns=target_cols).values
    y_train = train_df[target_cols].values
    X_test = test_df.drop(columns=target_cols).values
    y_test = test_df[target_cols].values
    
    print(f"\nTraining data shape: {X_train.shape}")
    print(f"Testing data shape: {X_test.shape}")
    
    # Train model
    save_dir = project_root / 'models' / 'neural_network'
    model = train_neural_network(
        X_train, X_test, y_train, y_test,
        epochs=100,
        batch_size=32,
        save_dir=save_dir
    )
    
    print("\n✅ Neural Network training complete!")


if __name__ == '__main__':
    main()
