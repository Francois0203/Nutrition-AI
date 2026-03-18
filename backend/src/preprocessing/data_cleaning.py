"""
Data Cleaning Module
====================
Handles real-world dirty data issues:
- Inconsistent categorical encoding (Sex variants)
- Missing values (imputation strategies)
- Unit errors (inches → cm, lbs → kg detection)
- Duplicate records (exact and near-duplicates)
- Missing target values
- Outliers and transcription errors
"""

import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer, KNNImputer
import warnings
warnings.filterwarnings('ignore')


# =============================================================================
# Sex Encoding Normalization
# =============================================================================

SEX_MAPPING = {
    # Male variants (case-insensitive)
    'M': 'M', 'MALE': 'M', 'male': 'M', 'm': 'M',
    # Female variants
    'F': 'F', 'FEMALE': 'F', 'female': 'F', 'f': 'F',
}


def normalize_sex(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize inconsistent Sex encoding to standard 'M' or 'F'.
    
    Args:
        df: DataFrame with 'Sex' column
        
    Returns:
        DataFrame with normalized 'Sex' column
    """
    if 'Sex' not in df.columns:
        return df
    
    df = df.copy()
    
    # Convert to string and strip whitespace
    df['Sex'] = df['Sex'].astype(str).str.strip()
    
    # Map to standard encoding
    df['Sex'] = df['Sex'].map(SEX_MAPPING)
    
    # Handle any unmapped values (set to most common)
    if df['Sex'].isna().any():
        most_common = df['Sex'].mode()[0] if len(df['Sex'].mode()) > 0 else 'M'
        df['Sex'].fillna(most_common, inplace=True)
        print(f"  Warning: Found unmapped Sex values, filled with '{most_common}'")
    
    print(f"  Sex normalized: {df['Sex'].value_counts().to_dict()}")
    return df


# =============================================================================
# Unit Error Detection & Correction
# =============================================================================

def detect_and_fix_unit_errors(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detect and fix common unit errors in measurements.
    
    Heuristics:
    - Height_cm < 100 → likely inches, convert to cm
    - Weight_kg > 150 → likely lbs, convert to kg
    - Other _cm fields < expected_min → likely inches
    
    Args:
        df: DataFrame with measurement columns
        
    Returns:
        DataFrame with corrected units
    """
    df = df.copy()
    corrections = 0
    
    # Height: if < 100 cm, likely entered in inches
    if 'Height_cm' in df.columns:
        height_mask = (df['Height_cm'] < 100) & (df['Height_cm'].notna())
        if height_mask.any():
            df.loc[height_mask, 'Height_cm'] *= 2.54
            corrections += height_mask.sum()
            print(f"  Fixed {height_mask.sum()} Height values (inches → cm)")
    
    # Weight: if > 150 kg (very heavy), likely entered in lbs
    if 'Weight_kg' in df.columns:
        weight_mask = (df['Weight_kg'] > 150) & (df['Weight_kg'].notna())
        if weight_mask.any():
            df.loc[weight_mask, 'Weight_kg'] /= 2.205
            corrections += weight_mask.sum()
            print(f"  Fixed {weight_mask.sum()} Weight values (lbs → kg)")
    
    # Other circumference measurements: if suspiciously small, likely inches
    cm_fields = [col for col in df.columns if col.endswith('_cm') and col != 'Height_cm']
    for field in cm_fields:
        # Heuristic: if value < 10 cm (very small), likely inches
        mask = (df[field] < 10) & (df[field].notna())
        if mask.any():
            df.loc[mask, field] *= 2.54
            corrections += mask.sum()
            print(f"  Fixed {mask.sum()} {field} values (inches → cm)")
    
    if corrections > 0:
        print(f"  Total unit corrections: {corrections}")
    
    return df


# =============================================================================
# Missing Value Handling
# =============================================================================

def handle_missing_values(df: pd.DataFrame, strategy: str = 'median', use_knn: bool = False) -> pd.DataFrame:
    """
    Handle missing values with imputation.
    
    Args:
        df: DataFrame with missing values
        strategy: 'median', 'mean', or 'most_frequent' for SimpleImputer
        use_knn: If True, use KNNImputer for better results (slower)
        
    Returns:
        DataFrame with imputed values
    """
    df = df.copy()
    
    # Count missing values
    missing_counts = df.isna().sum()
    missing_cols = missing_counts[missing_counts > 0]
    
    if len(missing_cols) == 0:
        print("  No missing values found")
        return df
    
    print(f"  Missing values found in {len(missing_cols)} columns")
    
    # Separate numeric and categorical columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    # Handle numeric columns
    if numeric_cols:
        missing_numeric = [col for col in numeric_cols if df[col].isna().any()]
        if missing_numeric:
            if use_knn:
                print(f"  Using KNN imputation for {len(missing_numeric)} numeric columns")
                imputer = KNNImputer(n_neighbors=5)
            else:
                print(f"  Using {strategy} imputation for {len(missing_numeric)} numeric columns")
                imputer = SimpleImputer(strategy=strategy)
            
            df[numeric_cols] = imputer.fit_transform(df[numeric_cols])
    
    # Handle categorical columns
    if categorical_cols:
        missing_categorical = [col for col in categorical_cols if df[col].isna().any()]
        if missing_categorical:
            print(f"  Using most_frequent imputation for {len(missing_categorical)} categorical columns")
            imputer = SimpleImputer(strategy='most_frequent')
            df[categorical_cols] = imputer.fit_transform(df[categorical_cols].values.reshape(-1, len(categorical_cols)))
    
    return df


# =============================================================================
# Duplicate Record Handling
# =============================================================================

def remove_duplicates(df: pd.DataFrame, subset=None, keep='first', near_duplicate_threshold: float = None) -> pd.DataFrame:
    """
    Remove exact and near-duplicate records.
    
    Args:
        df: DataFrame to deduplicate
        subset: Columns to consider for duplicates (None = all)
        keep: Which duplicate to keep ('first', 'last', False)
        near_duplicate_threshold: If set, also remove near-duplicates where
                                  numeric columns differ by < threshold (e.g., 0.01)
        
    Returns:
        Deduplicated DataFrame
    """
    df = df.copy()
    initial_rows = len(df)
    
    # Remove exact duplicates
    df = df.drop_duplicates(subset=subset, keep=keep)
    exact_dupes_removed = initial_rows - len(df)
    
    if exact_dupes_removed > 0:
        print(f"  Removed {exact_dupes_removed} exact duplicate records")
    
    # Remove near-duplicates (optional)
    if near_duplicate_threshold is not None:
        # Round numeric columns to remove near-duplicates
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df_rounded = df.copy()
        for col in numeric_cols:
            df_rounded[col] = df_rounded[col].round(1)
        
        df = df_rounded.drop_duplicates(subset=subset, keep=keep)
        near_dupes_removed = initial_rows - exact_dupes_removed - len(df)
        
        if near_dupes_removed > 0:
            print(f"  Removed {near_dupes_removed} near-duplicate records")
    
    return df


# =============================================================================
# Target Value Handling
# =============================================================================

def handle_missing_targets(df: pd.DataFrame, target_cols: list) -> pd.DataFrame:
    """
    Handle missing target values (BodyFatPct, MuscleMass_kg).
    
    Strategy: Drop rows where ANY target is missing, since we need both for training.
    
    Args:
        df: DataFrame with target columns
        target_cols: List of target column names
        
    Returns:
        DataFrame with complete target values
    """
    df = df.copy()
    initial_rows = len(df)
    
    # Check which targets exist in the DataFrame
    existing_targets = [col for col in target_cols if col in df.columns]
    
    if not existing_targets:
        print("  No target columns found in DataFrame")
        return df
    
    # Drop rows with any missing targets
    df = df.dropna(subset=existing_targets)
    
    rows_dropped = initial_rows - len(df)
    if rows_dropped > 0:
        print(f"  Dropped {rows_dropped} rows with missing target values")
    
    return df


# =============================================================================
# Outlier Detection & Handling (Enhanced)
# =============================================================================

def detect_outliers_iqr(df: pd.DataFrame, columns=None, multiplier: float = 1.5) -> pd.DataFrame:
    """
    Detect outliers using IQR method.
    
    Args:
        df: DataFrame
        columns: Columns to check (None = all numeric)
        multiplier: IQR multiplier (1.5 = standard, 3.0 = extreme outliers only)
        
    Returns:
        DataFrame with boolean mask for outliers
    """
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns
    
    outlier_mask = pd.DataFrame(False, index=df.index, columns=columns)
    
    for col in columns:
        if col in df.columns and df[col].notna().any():
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - multiplier * IQR
            upper_bound = Q3 + multiplier * IQR
            
            outlier_mask[col] = (df[col] < lower_bound) | (df[col] > upper_bound)
    
    return outlier_mask


def cap_outliers_iqr(df: pd.DataFrame, columns=None, multiplier: float = 1.5) -> pd.DataFrame:
    """
    Cap outliers to IQR bounds instead of removing them.
    
    Args:
        df: DataFrame
        columns: Columns to cap (None = all numeric)
        multiplier: IQR multiplier
        
    Returns:
        DataFrame with capped outliers
    """
    df = df.copy()
    
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns
    
    total_capped = 0
    
    for col in columns:
        if col in df.columns and df[col].notna().any():
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - multiplier * IQR
            upper_bound = Q3 + multiplier * IQR
            
            # Cap values
            capped = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
            df[col] = df[col].clip(lower=lower_bound, upper=upper_bound)
            
            total_capped += capped
    
    if total_capped > 0:
        print(f"  Capped {total_capped} outlier values using IQR method")
    
    return df


# =============================================================================
# Complete Cleaning Pipeline
# =============================================================================

def clean_data(df: pd.DataFrame, 
               target_cols: list = ['BodyFatPct', 'MuscleMass_kg'],
               imputation_strategy: str = 'median',
               use_knn_imputation: bool = False,
               remove_exact_duplicates: bool = True,
               remove_near_duplicates: bool = False,
               cap_outliers: bool = True,
               outlier_method: str = 'iqr') -> pd.DataFrame:
    """
    Complete data cleaning pipeline for dirty body measurement data.
    
    Steps:
    1. Normalize Sex encoding
    2. Detect and fix unit errors (inches/lbs)
    3. Handle missing values (imputation)
    4. Remove duplicate records
    5. Handle missing target values (drop rows)
    6. Cap/remove outliers
    
    Args:
        df: Raw DataFrame
        target_cols: List of target column names
        imputation_strategy: 'median', 'mean', or 'most_frequent'
        use_knn_imputation: Use KNN imputer (better but slower)
        remove_exact_duplicates: Remove exact duplicate rows
        remove_near_duplicates: Remove near-duplicate rows
        cap_outliers: Cap outliers instead of removing
        outlier_method: 'iqr' or 'std' (IQR recommended)
        
    Returns:
        Cleaned DataFrame
    """
    print("\n" + "="*70)
    print("DATA CLEANING PIPELINE")
    print("="*70)
    
    initial_rows = len(df)
    print(f"Initial dataset: {initial_rows} rows, {len(df.columns)} columns")
    
    # Step 1: Normalize Sex encoding
    print("\n1. Normalizing Sex encoding...")
    df = normalize_sex(df)
    
    # Step 2: Fix unit errors
    print("\n2. Detecting and fixing unit errors...")
    df = detect_and_fix_unit_errors(df)
    
    # Step 3: Handle missing values (before dropping target rows)
    print("\n3. Handling missing values...")
    # First, handle missing in feature columns only (not targets yet)
    feature_cols = [col for col in df.columns if col not in target_cols]
    df_features = df[feature_cols]
    df_features = handle_missing_values(df_features, strategy=imputation_strategy, use_knn=use_knn_imputation)
    
    # Recombine with targets
    for col in feature_cols:
        df[col] = df_features[col]
    
    # Step 4: Remove duplicates
    if remove_exact_duplicates or remove_near_duplicates:
        print("\n4. Removing duplicate records...")
        threshold = 0.01 if remove_near_duplicates else None
        df = remove_duplicates(df, near_duplicate_threshold=threshold)
    
    # Step 5: Handle missing targets (drop rows)
    print("\n5. Handling missing target values...")
    df = handle_missing_targets(df, target_cols)
    
    # Step 6: Cap outliers
    if cap_outliers:
        print("\n6. Capping outliers...")
        if outlier_method == 'iqr':
            # Use IQR method (more robust to outliers)
            df = cap_outliers_iqr(df, multiplier=1.5)
        else:
            # Use standard deviation method (existing approach)
            pass  # Keep existing std-based capping in preprocessor
    
    final_rows = len(df)
    rows_removed = initial_rows - final_rows
    
    print("\n" + "="*70)
    print("CLEANING COMPLETE")
    print("="*70)
    print(f"Final dataset: {final_rows} rows, {len(df.columns)} columns")
    print(f"Rows removed: {rows_removed} ({rows_removed/initial_rows*100:.1f}%)")
    print(f"Remaining data: {final_rows/initial_rows*100:.1f}% of original")
    
    return df


# =============================================================================
# Data Quality Report
# =============================================================================

def generate_quality_report(df_before: pd.DataFrame, df_after: pd.DataFrame) -> dict:
    """
    Generate a data quality report comparing before and after cleaning.
    
    Args:
        df_before: DataFrame before cleaning
        df_after: DataFrame after cleaning
        
    Returns:
        Dictionary with quality metrics
    """
    report = {
        'rows_before': len(df_before),
        'rows_after': len(df_after),
        'rows_removed': len(df_before) - len(df_after),
        'pct_retained': len(df_after) / len(df_before) * 100,
        'missing_before': df_before.isna().sum().sum(),
        'missing_after': df_after.isna().sum().sum(),
        'columns_before': len(df_before.columns),
        'columns_after': len(df_after.columns),
    }
    
    return report


def print_quality_report(report: dict):
    """Print a formatted data quality report."""
    print("\n" + "="*70)
    print("DATA QUALITY REPORT")
    print("="*70)
    print(f"Rows:           {report['rows_before']:,} → {report['rows_after']:,} "
          f"(-{report['rows_removed']:,}, {report['pct_retained']:.1f}% retained)")
    print(f"Missing values: {report['missing_before']:,} → {report['missing_after']:,}")
    print(f"Columns:        {report['columns_before']} → {report['columns_after']}")
    print("="*70)
