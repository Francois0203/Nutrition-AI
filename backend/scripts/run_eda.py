"""
Example: Using the Exploratory Data Analysis Module
====================================================
This script demonstrates how to use the EDA functions on body measurement data.
"""

import sys
from pathlib import Path

# Ensure the project's `src` directory is on sys.path regardless of CWD
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
src_path = project_root / 'src'
sys.path.insert(0, str(src_path))

import pandas as pd
from exploratory_data_analysis import (
    generate_eda_report,
    print_report_summary,
    get_basic_statistics,
    find_high_correlations,
    detect_outliers_iqr,
    compare_groups
)

# Load the data
print("Loading data...")
# Resolve data directory relative to project root to avoid CWD issues
data_dir = project_root / 'Data'
data_file = data_dir / 'Body Measurements with Features.csv'
if not data_file.exists():
    # fallback to lowercase 'data' for environments using that folder
    data_dir = project_root / 'data'
    data_file = data_dir / 'Body Measurements with Features.csv'

if not data_file.exists():
    raise FileNotFoundError(f"Dataset not found: {data_file}\nPlease run scripts/generate_full_dataset.py or place the CSV in {project_root / 'Data'}")

df = pd.read_csv(str(data_file))
print(f"Loaded {len(df)} rows and {len(df.columns)} columns\n")

# =============================================================================
# OPTION 1: Quick Comprehensive Report
# =============================================================================
print("="*80)
print("GENERATING COMPREHENSIVE EDA REPORT")
print("="*80)

# Generate full report (this will take a moment)
# Adjust target and group_by based on your actual column names
report = generate_eda_report(
    df,
    target='bmi',           # Analyze importance relative to BMI
    group_by='Gender'       # Compare statistics by gender (if column exists)
)

# Print human-readable summary
print_report_summary(report)

# Access specific report sections
print("\n" + "="*80)
print("DETAILED INSIGHTS")
print("="*80)

# Top correlated features
print("\n📊 Top 10 Correlated Feature Pairs:")
print(report['high_correlations'].head(10))

# Features with most outliers
print("\n⚠️  Features with Most Outliers:")
outlier_summary = report['outliers_iqr']['summary']
print(outlier_summary.sort_values('outlier_pct', ascending=False).head(10))

# =============================================================================
# OPTION 2: Individual Analysis Functions
# =============================================================================
print("\n" + "="*80)
print("INDIVIDUAL ANALYSIS EXAMPLES")
print("="*80)

# Basic statistics for a few key features
print("\n1. Basic Statistics for Key Features:")
key_features = ['Height_cm', 'Weight_kg', 'bmi', 'BodyFatPct', 'MuscleMass_kg']
if all(f in df.columns for f in key_features):
    stats = get_basic_statistics(df[key_features])
    print(stats.round(2))

# Find multicollinear features
print("\n2. Highly Correlated Features (|r| > 0.85):")
high_corr = find_high_correlations(df, threshold=0.85)
if len(high_corr) > 0:
    print(high_corr.head(10))
else:
    print("  No features with correlation > 0.85")

# Outlier detection
print("\n3. Outlier Analysis Summary:")
outliers = detect_outliers_iqr(df)
print(outliers['summary'].sort_values('outlier_count', ascending=False).head(10))

# Group comparison (if Gender column exists)
if 'Gender' in df.columns:
    print("\n4. Gender-based Comparison (selected features):")
    comparison = compare_groups(
        df,
        group_col='Gender',
        numeric_cols=['Height_cm', 'Weight_kg', 'bmi', 'BodyFatPct']
    )
    print(comparison)

# =============================================================================
# SAVE RESULTS
# =============================================================================
print("\n" + "="*80)
print("SAVING RESULTS")
print("="*80)

# Save correlation matrix
out_dir = project_root / 'Data'
if not out_dir.exists():
    out_dir = project_root / 'data'

report['correlation_matrix'].to_csv(str(out_dir / 'correlation_matrix.csv'))
print(f"✓ Correlation matrix saved to '{out_dir / 'correlation_matrix.csv'}'")

# Save outlier summary
report['outliers_iqr']['summary'].to_csv(str(out_dir / 'outlier_summary.csv'), index=False)
print(f"✓ Outlier summary saved to '{out_dir / 'outlier_summary.csv'}'")

# Save basic statistics
report['basic_statistics'].to_csv(str(out_dir / 'basic_statistics.csv'))
print(f"✓ Basic statistics saved to '{out_dir / 'basic_statistics.csv'}'")

if report['feature_importance_rf'] is not None:
    report['feature_importance_rf'].to_csv(str(out_dir / 'feature_importance.csv'), index=False)
    print(f"✓ Feature importance saved to '{out_dir / 'feature_importance.csv'}'")

print("\n" + "="*80)
print("EDA COMPLETE!")
print("="*80)
