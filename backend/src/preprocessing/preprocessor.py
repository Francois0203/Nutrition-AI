"""
Data Preprocessor Module
=========================
Handles feature selection, scaling, and data preparation for ML models.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Import data cleaning functions
from .data_cleaning import clean_data, generate_quality_report, print_quality_report


class DataPreprocessor:
    """
    Preprocesses body measurement data for machine learning models.
    
    Features:
    - Removes highly correlated features (multicollinearity)
    - Handles outliers
    - Scales numerical features
    - Splits data into train/test sets
    """
    
    def __init__(self, correlation_threshold=0.95, outlier_std=4):
        """
        Initialize the preprocessor.
        
        Args:
            correlation_threshold: Threshold for removing correlated features (default: 0.95)
            outlier_std: Number of standard deviations for outlier detection (default: 4)
        """
        self.correlation_threshold = correlation_threshold
        self.outlier_std = outlier_std
        self.scaler = StandardScaler()
        self.feature_columns = None
        self.target_columns = ['BodyFatPct', 'MuscleMass_kg']
        self.removed_features = []
        
    def remove_correlated_features(self, df):
        """
        Remove highly correlated features to reduce multicollinearity.
        
        Args:
            df: DataFrame with features
            
        Returns:
            DataFrame with reduced features
        """
        # Calculate correlation matrix
        corr_matrix = df.corr().abs()
        
        # Select upper triangle of correlation matrix
        upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
        
        # Find features with correlation greater than threshold
        to_drop = [column for column in upper.columns if any(upper[column] > self.correlation_threshold)]
        
        self.removed_features = to_drop
        print(f"  Removing {len(to_drop)} highly correlated features: {to_drop}")
        
        return df.drop(columns=to_drop)
    
    def handle_outliers(self, df):
        """
        Cap outliers at N standard deviations from mean.
        
        Args:
            df: DataFrame with numerical features
            
        Returns:
            DataFrame with capped outliers
        """
        df_copy = df.copy()
        outlier_count = 0
        
        for col in df_copy.columns:
            if df_copy[col].dtype in ['float64', 'int64']:
                mean = df_copy[col].mean()
                std = df_copy[col].std()
                
                lower_bound = mean - self.outlier_std * std
                upper_bound = mean + self.outlier_std * std
                
                outliers = ((df_copy[col] < lower_bound) | (df_copy[col] > upper_bound)).sum()
                outlier_count += outliers
                
                # Cap outliers
                df_copy[col] = df_copy[col].clip(lower=lower_bound, upper=upper_bound)
        
        print(f"  Capped {outlier_count} outlier values")
        return df_copy
    
    def fit_transform(self, df):
        """
        Fit the preprocessor and transform the data.
        
        Args:
            df: DataFrame with all features and targets
            
        Returns:
            X_scaled: Scaled feature matrix
            y: Target matrix
            feature_names: List of feature names after preprocessing
        """
        print("Starting preprocessing...")
        
        # Separate features and targets
        target_cols_present = [col for col in self.target_columns if col in df.columns]
        y = df[target_cols_present].copy()
        
        # Get feature columns (exclude targets and non-numeric columns)
        exclude_cols = target_cols_present + ['Sex']  # Exclude Sex as it's categorical
        X = df.drop(columns=exclude_cols, errors='ignore')
        
        # Encode Sex if present
        if 'Sex' in df.columns:
            sex_encoded = pd.get_dummies(df['Sex'], prefix='Sex', drop_first=True)
            X = pd.concat([X, sex_encoded], axis=1)
        
        print(f"  Initial features: {X.shape[1]}")
        
        # Remove highly correlated features
        X = self.remove_correlated_features(X)
        
        # Handle outliers
        X = self.handle_outliers(X)
        
        # Store feature names
        self.feature_columns = X.columns.tolist()
        print(f"  Final features: {len(self.feature_columns)}")
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        print("Preprocessing complete!")
        return X_scaled, y.values, self.feature_columns
    
    def transform(self, df):
        """
        Transform new data using fitted preprocessor.
        
        Args:
            df: DataFrame with features
            
        Returns:
            X_scaled: Scaled feature matrix
        """
        # Process same as fit_transform but without fitting
        exclude_cols = self.target_columns + ['Sex']
        X = df.drop(columns=exclude_cols, errors='ignore')
        
        if 'Sex' in df.columns:
            sex_encoded = pd.get_dummies(df['Sex'], prefix='Sex', drop_first=True)
            X = pd.concat([X, sex_encoded], axis=1)
        
        # Remove same features as during training
        X = X.drop(columns=self.removed_features, errors='ignore')
        
        # Ensure same column order
        X = X[self.feature_columns]
        
        # Scale
        X_scaled = self.scaler.transform(X)
        
        return X_scaled
    
    def save(self, filepath):
        """Save the fitted preprocessor."""
        joblib.dump(self, filepath)
        print(f"Preprocessor saved to {filepath}")
    
    @staticmethod
    def load(filepath):
        """Load a fitted preprocessor."""
        return joblib.load(filepath)


def load_and_preprocess_data(data_path, test_size=0.2, random_state=42, 
                             clean_dirty_data=True, use_knn_imputation=False):
    """
    Load data from CSV and preprocess it.
    
    Args:
        data_path: Path to CSV file
        test_size: Proportion of data to use for testing
        random_state: Random seed for reproducibility
        clean_dirty_data: Whether to apply data cleaning pipeline (recommended for real data)
        use_knn_imputation: Use KNN imputation (better but slower)
        
    Returns:
        Tuple of (X_train, X_test, y_train, y_test, preprocessor, feature_names)
    """
    print(f"Loading data from {data_path}...")
    df = pd.read_csv(data_path)
    print(f"Loaded {len(df)} samples with {len(df.columns)} columns")
    
    # Apply data cleaning pipeline if requested
    if clean_dirty_data:
        df_before = df.copy()
        df = clean_data(
            df,
            target_cols=['BodyFatPct', 'MuscleMass_kg'],
            imputation_strategy='median',
            use_knn_imputation=use_knn_imputation,
            remove_exact_duplicates=True,
            remove_near_duplicates=True,
            cap_outliers=True,
            outlier_method='iqr'
        )
        
        # Generate quality report
        report = generate_quality_report(df_before, df)
        print_quality_report(report)
    
    # Initialize and fit preprocessor
    preprocessor = DataPreprocessor()
    X_scaled, y, feature_names = preprocessor.fit_transform(df)
    
    # Split into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=test_size, random_state=random_state
    )
    
    print(f"\nData split:")
    print(f"  Training samples: {X_train.shape[0]}")
    print(f"  Testing samples: {X_test.shape[0]}")
    print(f"  Features: {X_train.shape[1]}")
    print(f"  Targets: {y_train.shape[1]} (BodyFatPct, MuscleMass_kg)")
    
    return X_train, X_test, y_train, y_test, preprocessor, feature_names


def save_preprocessed_data(X_train, X_test, y_train, y_test, feature_names, output_dir):
    """
    Save preprocessed data to CSV files.
    
    Args:
        X_train, X_test: Feature matrices
        y_train, y_test: Target matrices
        feature_names: List of feature names
        output_dir: Directory to save files
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)
    
    # Create DataFrames
    train_df = pd.DataFrame(X_train, columns=feature_names)
    train_df['BodyFatPct'] = y_train[:, 0]
    train_df['MuscleMass_kg'] = y_train[:, 1]
    
    test_df = pd.DataFrame(X_test, columns=feature_names)
    test_df['BodyFatPct'] = y_test[:, 0]
    test_df['MuscleMass_kg'] = y_test[:, 1]
    
    # Save to CSV
    train_path = output_dir / 'preprocessed_train.csv'
    test_path = output_dir / 'preprocessed_test.csv'
    
    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)
    
    print(f"\nPreprocessed data saved:")
    print(f"  Training: {train_path}")
    print(f"  Testing: {test_path}")
    
    return train_path, test_path
