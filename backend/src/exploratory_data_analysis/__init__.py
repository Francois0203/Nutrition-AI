"""
Exploratory Data Analysis Module
=================================
Comprehensive toolkit for analyzing body measurement data.

Quick Start
-----------
>>> from exploratory_data_analysis import generate_eda_report, print_report_summary
>>> import pandas as pd
>>> df = pd.read_csv("Body Measurements.csv")
>>> report = generate_eda_report(df, target="Weight_kg", group_by="Gender")
>>> print_report_summary(report)

Available Functions
-------------------
Statistical Summaries:
- get_basic_statistics: Descriptive statistics for all numeric features
- get_percentile_distribution: Percentile analysis
- test_normality: Statistical tests for normal distribution

Correlation Analysis:
- get_correlation_matrix: Compute correlation matrices
- find_high_correlations: Identify multicollinear features
- calculate_vif: Variance Inflation Factor analysis

Outlier Detection:
- detect_outliers_iqr: IQR-based outlier detection
- detect_outliers_zscore: Z-score-based outlier detection
- detect_outliers_isolation_forest: ML-based multivariate outlier detection

Missing Data:
- analyze_missing_data: Missing value analysis per column
- identify_missing_patterns: Pattern discovery in missing data

Group Comparisons:
- compare_groups: Statistical comparison across groups
- stratify_by_percentile: Create percentile-based groups

Feature Analysis:
- analyze_feature_importance: Feature importance using RF/mutual info/correlation
- find_nonlinear_relationships: Multi-method correlation analysis

Data Quality:
- check_data_quality: Comprehensive quality checks
- validate_numeric_ranges: Range validation for features

Reports:
- generate_eda_report: Complete EDA report generation
- print_report_summary: Human-readable report summary
"""

from .exploratory_data_analysis import (
    # Statistical summaries
    get_basic_statistics,
    get_percentile_distribution,
    test_normality,
    
    # Correlation analysis
    get_correlation_matrix,
    find_high_correlations,
    calculate_vif,
    
    # Outlier detection
    detect_outliers_iqr,
    detect_outliers_zscore,
    detect_outliers_isolation_forest,
    
    # Missing data analysis
    analyze_missing_data,
    identify_missing_patterns,
    
    # Group comparisons
    compare_groups,
    stratify_by_percentile,
    
    # Feature relationships
    analyze_feature_importance,
    find_nonlinear_relationships,
    
    # Data quality checks
    check_data_quality,
    validate_numeric_ranges,
    
    # Report generation
    generate_eda_report,
    print_report_summary,
)

__all__ = [
    # Statistical summaries
    'get_basic_statistics',
    'get_percentile_distribution',
    'test_normality',
    
    # Correlation analysis
    'get_correlation_matrix',
    'find_high_correlations',
    'calculate_vif',
    
    # Outlier detection
    'detect_outliers_iqr',
    'detect_outliers_zscore',
    'detect_outliers_isolation_forest',
    
    # Missing data analysis
    'analyze_missing_data',
    'identify_missing_patterns',
    
    # Group comparisons
    'compare_groups',
    'stratify_by_percentile',
    
    # Feature relationships
    'analyze_feature_importance',
    'find_nonlinear_relationships',
    
    # Data quality checks
    'check_data_quality',
    'validate_numeric_ranges',
    
    # Report generation
    'generate_eda_report',
    'print_report_summary',
]

__version__ = '1.0.0'
