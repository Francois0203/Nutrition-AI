"""
Preprocessing module for data preparation and feature engineering.
"""

from .preprocessor import (
    DataPreprocessor,
    load_and_preprocess_data,
    save_preprocessed_data
)

from .data_cleaning import (
    clean_data,
    normalize_sex,
    detect_and_fix_unit_errors,
    handle_missing_values,
    remove_duplicates,
    handle_missing_targets,
    cap_outliers_iqr,
    generate_quality_report,
    print_quality_report
)

__all__ = [
    'DataPreprocessor',
    'load_and_preprocess_data',
    'save_preprocessed_data',
    'clean_data',
    'normalize_sex',
    'detect_and_fix_unit_errors',
    'handle_missing_values',
    'remove_duplicates',
    'handle_missing_targets',
    'cap_outliers_iqr',
    'generate_quality_report',
    'print_quality_report'
]
