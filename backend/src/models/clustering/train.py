"""
Train clustering model for body type categorization.
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
from models.clustering.model import perform_clustering


def main():
    """Main script for clustering analysis."""
    print("="*70)
    print("BODY TYPE CLUSTERING ANALYSIS")
    print("="*70)
    
    # Load preprocessed data
    data_dir = project_root / 'Data' / 'preprocessed'
    train_df = pd.read_csv(data_dir / 'preprocessed_train.csv')
    
    # Separate features and targets
    target_cols = ['BodyFatPct', 'MuscleMass_kg']
    feature_names = [col for col in train_df.columns if col not in target_cols]
    
    X_train = train_df.drop(columns=target_cols).values
    y_train = train_df[target_cols].values
    
    print(f"\nData shape: {X_train.shape}")
    print(f"Features: {len(feature_names)}")
    
    # Perform clustering
    save_dir = project_root / 'models' / 'clustering'
    model = perform_clustering(
        X_train, y_train,
        feature_names=feature_names,
        n_clusters=5,
        save_dir=save_dir
    )
    
    print("\n✅ Clustering analysis complete!")


if __name__ == '__main__':
    main()
