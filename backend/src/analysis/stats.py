"""
stats.py
========
Data analysis utilities for body composition datasets.

Provides functions for statistical analysis, data validation,
and exploratory data analysis.
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple


def get_basic_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Get basic statistical summary of DataFrame.
    
    Args:
        df: Input DataFrame
        
    Returns:
        DataFrame with descriptive statistics
    """
    return df.describe()


def check_missing_values(df: pd.DataFrame) -> pd.Series:
    """
    Check for missing values in DataFrame.
    
    Args:
        df: Input DataFrame
        
    Returns:
        Series with count of missing values per column
    """
    return df.isnull().sum()


def get_correlation_matrix(df: pd.DataFrame, columns: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Calculate correlation matrix for numeric columns.
    
    Args:
        df: Input DataFrame
        columns: Optional list of columns to include (default: all numeric columns)
        
    Returns:
        Correlation matrix DataFrame
    """
    if columns is not None:
        df = df[columns]
    
    return df.select_dtypes(include=[np.number]).corr()


def check_outliers_iqr(df: pd.DataFrame, column: str) -> Tuple[pd.Series, int]:
    """
    Identify outliers using IQR method.
    
    Args:
        df: Input DataFrame
        column: Column name to check for outliers
        
    Returns:
        Tuple of (boolean series of outliers, count of outliers)
    """
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = (df[column] < lower_bound) | (df[column] > upper_bound)
    
    return outliers, outliers.sum()


def get_feature_distributions(df: pd.DataFrame, by_column: str = 'Sex') -> Dict[str, pd.DataFrame]:
    """
    Get feature distributions grouped by a categorical column.
    
    Args:
        df: Input DataFrame
        by_column: Column to group by (e.g., 'Sex')
        
    Returns:
        Dictionary mapping group values to their statistical summaries
    """
    if by_column not in df.columns:
        raise ValueError(f"Column '{by_column}' not found in DataFrame")
    
    distributions = {}
    for group_value, group_df in df.groupby(by_column):
        distributions[group_value] = group_df.describe()
    
    return distributions
