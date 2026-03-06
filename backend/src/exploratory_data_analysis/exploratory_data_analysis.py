"""
exploratory_data_analysis.py
=============================
Comprehensive exploratory data analysis (EDA) toolkit for body measurement data.

This module provides functions for:
- Statistical summaries and distributions
- Correlation and multicollinearity analysis
- Outlier detection and handling
- Missing data analysis
- Group comparisons (e.g., by gender, age groups)
- Feature importance and relationships
- Data quality checks
- Report generation

All functions accept pandas DataFrames and return structured results optimized
for both programmatic use and human interpretation.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Union
from scipy import stats
from scipy.stats import kstest, shapiro, normaltest


# =============================================================================
# 1. STATISTICAL SUMMARIES
# =============================================================================

def get_basic_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate comprehensive descriptive statistics for all numeric columns.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe with numeric columns.
    
    Returns
    -------
    pd.DataFrame
        Statistics including mean, median, std, quartiles, skewness, kurtosis,
        min, max, range, coefficient of variation.
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    stats_dict = {
        'count': df[numeric_cols].count(),
        'mean': df[numeric_cols].mean(),
        'median': df[numeric_cols].median(),
        'std': df[numeric_cols].std(),
        'min': df[numeric_cols].min(),
        'q25': df[numeric_cols].quantile(0.25),
        'q75': df[numeric_cols].quantile(0.75),
        'max': df[numeric_cols].max(),
        'range': df[numeric_cols].max() - df[numeric_cols].min(),
        'skewness': df[numeric_cols].skew(),
        'kurtosis': df[numeric_cols].kurtosis(),
        'cv': (df[numeric_cols].std() / df[numeric_cols].mean()) * 100  # Coefficient of variation
    }
    
    return pd.DataFrame(stats_dict).T


def get_percentile_distribution(df: pd.DataFrame, 
                                percentiles: List[float] = None) -> pd.DataFrame:
    """
    Calculate percentile distributions for all numeric columns.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    percentiles : List[float], optional
        List of percentiles (0-100). Default: [1, 5, 10, 25, 50, 75, 90, 95, 99]
    
    Returns
    -------
    pd.DataFrame
        Percentile values for each numeric column.
    """
    if percentiles is None:
        percentiles = [1, 5, 10, 25, 50, 75, 90, 95, 99]
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    percentile_values = [p/100 for p in percentiles]
    
    result = df[numeric_cols].quantile(percentile_values)
    result.index = [f'p{p}' for p in percentiles]
    
    return result


def test_normality(df: pd.DataFrame, alpha: float = 0.05) -> pd.DataFrame:
    """
    Test normality of distributions using multiple statistical tests.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    alpha : float
        Significance level for hypothesis testing. Default: 0.05
    
    Returns
    -------
    pd.DataFrame
        Results of Shapiro-Wilk and D'Agostino-Pearson tests with p-values
        and normality assessment.
        
    Notes
    -----
    - Shapiro-Wilk: Good for sample sizes < 5000
    - D'Agostino-Pearson: Tests based on skewness and kurtosis
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    results = []
    
    for col in numeric_cols:
        data = df[col].dropna()
        
        if len(data) < 3:
            continue
            
        # Shapiro-Wilk test (sample size < 5000 recommended)
        if len(data) <= 5000:
            shapiro_stat, shapiro_p = shapiro(data)
        else:
            shapiro_stat, shapiro_p = np.nan, np.nan
        
        # D'Agostino-Pearson test
        if len(data) >= 8:
            dagostino_stat, dagostino_p = normaltest(data)
        else:
            dagostino_stat, dagostino_p = np.nan, np.nan
        
        is_normal = (shapiro_p > alpha if not np.isnan(shapiro_p) else False) and \
                   (dagostino_p > alpha if not np.isnan(dagostino_p) else False)
        
        results.append({
            'feature': col,
            'shapiro_stat': shapiro_stat,
            'shapiro_pvalue': shapiro_p,
            'dagostino_stat': dagostino_stat,
            'dagostino_pvalue': dagostino_p,
            'is_normal': is_normal
        })
    
    return pd.DataFrame(results)


# =============================================================================
# 2. CORRELATION ANALYSIS
# =============================================================================

def get_correlation_matrix(df: pd.DataFrame, 
                           method: str = 'pearson',
                           min_periods: int = 1) -> pd.DataFrame:
    """
    Calculate correlation matrix for all numeric features.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    method : str
        Correlation method: 'pearson', 'spearman', or 'kendall'. Default: 'pearson'
    min_periods : int
        Minimum number of observations required per pair. Default: 1
    
    Returns
    -------
    pd.DataFrame
        Correlation matrix.
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    return df[numeric_cols].corr(method=method, min_periods=min_periods)


def find_high_correlations(df: pd.DataFrame, 
                           threshold: float = 0.8,
                           method: str = 'pearson') -> pd.DataFrame:
    """
    Identify pairs of features with high correlation (multicollinearity).
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    threshold : float
        Absolute correlation threshold. Default: 0.8
    method : str
        Correlation method: 'pearson', 'spearman', or 'kendall'. Default: 'pearson'
    
    Returns
    -------
    pd.DataFrame
        Pairs of features with correlation above threshold, sorted by absolute correlation.
    """
    corr_matrix = get_correlation_matrix(df, method=method)
    
    # Get upper triangle of correlation matrix
    upper_triangle = np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
    corr_matrix_upper = corr_matrix.where(upper_triangle)
    
    # Find high correlations
    high_corr = []
    for col in corr_matrix_upper.columns:
        for idx in corr_matrix_upper.index:
            value = corr_matrix_upper.loc[idx, col]
            if pd.notna(value) and abs(value) >= threshold:
                high_corr.append({
                    'feature_1': idx,
                    'feature_2': col,
                    'correlation': value,
                    'abs_correlation': abs(value)
                })
    
    result = pd.DataFrame(high_corr)
    if not result.empty:
        result = result.sort_values('abs_correlation', ascending=False)
    
    return result


def calculate_vif(df: pd.DataFrame, features: List[str] = None) -> pd.DataFrame:
    """
    Calculate Variance Inflation Factor (VIF) to detect multicollinearity.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    features : List[str], optional
        List of feature names to calculate VIF for. If None, uses all numeric columns.
    
    Returns
    -------
    pd.DataFrame
        VIF scores for each feature. VIF > 10 indicates high multicollinearity.
        
    Notes
    -----
    VIF interpretation:
    - VIF = 1: No correlation
    - 1 < VIF < 5: Moderate correlation
    - VIF > 5: High correlation
    - VIF > 10: Severe multicollinearity (consider removing feature)
    """
    if features is None:
        features = df.select_dtypes(include=[np.number]).columns.tolist()
    
    df_subset = df[features].dropna()
    
    vif_data = []
    for i, feature in enumerate(features):
        # Calculate VIF: 1 / (1 - R²)
        # R² is from regressing this feature on all other features
        X = df_subset.drop(columns=[feature])
        y = df_subset[feature]
        
        # Simple correlation-based R² calculation
        if X.shape[1] > 0:
            from sklearn.linear_model import LinearRegression
            model = LinearRegression()
            model.fit(X, y)
            r_squared = model.score(X, y)
            vif = 1 / (1 - r_squared) if r_squared < 1 else np.inf
        else:
            vif = 1.0
        
        vif_data.append({
            'feature': feature,
            'vif': vif,
            'multicollinearity': 'severe' if vif > 10 else 'high' if vif > 5 else 'moderate' if vif > 1 else 'none'
        })
    
    return pd.DataFrame(vif_data).sort_values('vif', ascending=False)


# =============================================================================
# 3. OUTLIER DETECTION
# =============================================================================

def detect_outliers_iqr(df: pd.DataFrame, 
                        multiplier: float = 1.5) -> Dict[str, pd.DataFrame]:
    """
    Detect outliers using the Interquartile Range (IQR) method.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    multiplier : float
        IQR multiplier for outlier boundaries. Default: 1.5 (standard)
        Use 3.0 for extreme outliers only.
    
    Returns
    -------
    Dict[str, pd.DataFrame]
        Dictionary with:
        - 'summary': Summary of outlier counts per feature
        - 'outlier_indices': Boolean mask of outliers
        - 'bounds': Lower and upper bounds for each feature
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    outlier_summary = []
    outlier_mask = pd.DataFrame(False, index=df.index, columns=numeric_cols)
    bounds_data = []
    
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - multiplier * IQR
        upper_bound = Q3 + multiplier * IQR
        
        outliers = (df[col] < lower_bound) | (df[col] > upper_bound)
        outlier_mask[col] = outliers
        
        outlier_summary.append({
            'feature': col,
            'outlier_count': outliers.sum(),
            'outlier_pct': (outliers.sum() / len(df)) * 100,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound
        })
        
        bounds_data.append({
            'feature': col,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound
        })
    
    return {
        'summary': pd.DataFrame(outlier_summary),
        'outlier_indices': outlier_mask,
        'bounds': pd.DataFrame(bounds_data)
    }


def detect_outliers_zscore(df: pd.DataFrame, 
                           threshold: float = 3.0) -> Dict[str, pd.DataFrame]:
    """
    Detect outliers using Z-score method (standard deviations from mean).
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    threshold : float
        Number of standard deviations to consider as outlier. Default: 3.0
    
    Returns
    -------
    Dict[str, pd.DataFrame]
        Dictionary with:
        - 'summary': Summary of outlier counts per feature
        - 'outlier_indices': Boolean mask of outliers
        - 'zscores': Z-scores for all values
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    zscores = df[numeric_cols].apply(lambda x: np.abs(stats.zscore(x, nan_policy='omit')))
    outlier_mask = zscores > threshold
    
    outlier_summary = []
    for col in numeric_cols:
        outlier_summary.append({
            'feature': col,
            'outlier_count': outlier_mask[col].sum(),
            'outlier_pct': (outlier_mask[col].sum() / len(df)) * 100,
            'max_zscore': zscores[col].max()
        })
    
    return {
        'summary': pd.DataFrame(outlier_summary),
        'outlier_indices': outlier_mask,
        'zscores': zscores
    }


def detect_outliers_isolation_forest(df: pd.DataFrame,
                                     contamination: float = 0.1,
                                     random_state: int = 42) -> Dict[str, Union[pd.Series, np.ndarray]]:
    """
    Detect multivariate outliers using Isolation Forest algorithm.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    contamination : float
        Expected proportion of outliers in the dataset. Default: 0.1 (10%)
    random_state : int
        Random seed for reproducibility. Default: 42
    
    Returns
    -------
    Dict
        Dictionary with:
        - 'outlier_labels': -1 for outliers, 1 for inliers
        - 'outlier_scores': Anomaly scores (lower = more anomalous)
        - 'is_outlier': Boolean mask
    """
    from sklearn.ensemble import IsolationForest
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df_clean = df[numeric_cols].dropna()
    
    iso_forest = IsolationForest(
        contamination=contamination,
        random_state=random_state,
        n_estimators=100
    )
    
    labels = iso_forest.fit_predict(df_clean)
    scores = iso_forest.score_samples(df_clean)
    
    # Map to original DataFrame index
    outlier_series = pd.Series(-1, index=df.index)
    outlier_series.loc[df_clean.index] = labels
    
    score_series = pd.Series(np.nan, index=df.index)
    score_series.loc[df_clean.index] = scores
    
    return {
        'outlier_labels': outlier_series,
        'outlier_scores': score_series,
        'is_outlier': outlier_series == -1,
        'outlier_count': (outlier_series == -1).sum(),
        'outlier_pct': ((outlier_series == -1).sum() / len(df)) * 100
    }


# =============================================================================
# 4. MISSING DATA ANALYSIS
# =============================================================================

def analyze_missing_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Comprehensive analysis of missing data patterns.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    
    Returns
    -------
    pd.DataFrame
        Missing data statistics per column including count, percentage,
        and data type.
    """
    missing_stats = []
    
    for col in df.columns:
        missing_count = df[col].isna().sum()
        missing_pct = (missing_count / len(df)) * 100
        
        missing_stats.append({
            'column': col,
            'missing_count': missing_count,
            'missing_pct': missing_pct,
            'present_count': len(df) - missing_count,
            'dtype': str(df[col].dtype)
        })
    
    result = pd.DataFrame(missing_stats)
    result = result.sort_values('missing_pct', ascending=False)
    
    return result


def identify_missing_patterns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Identify common patterns in missing data across rows.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    
    Returns
    -------
    pd.DataFrame
        Counts of common missing data patterns.
    """
    # Create a pattern string for each row
    missing_patterns = df.isna().apply(
        lambda row: '_'.join(row.index[row].tolist()), axis=1
    )
    
    pattern_counts = missing_patterns.value_counts()
    
    return pd.DataFrame({
        'pattern': pattern_counts.index,
        'count': pattern_counts.values,
        'pct': (pattern_counts.values / len(df)) * 100
    })


# =============================================================================
# 5. GROUP COMPARISONS
# =============================================================================

def compare_groups(df: pd.DataFrame,
                   group_col: str,
                   numeric_cols: List[str] = None,
                   test: str = 'auto') -> pd.DataFrame:
    """
    Compare numeric features across different groups (e.g., by gender).
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    group_col : str
        Column name to group by.
    numeric_cols : List[str], optional
        Numeric columns to compare. If None, uses all numeric columns.
    test : str
        Statistical test: 'auto', 't-test', 'mann-whitney', 'anova', 'kruskal'.
        Default: 'auto' (chooses based on normality and number of groups)
    
    Returns
    -------
    pd.DataFrame
        Comparison statistics including means, medians, std, and p-values.
    """
    if numeric_cols is None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    groups = df[group_col].unique()
    n_groups = len(groups)
    
    results = []
    
    for col in numeric_cols:
        group_data = [df[df[group_col] == g][col].dropna() for g in groups]
        
        # Calculate statistics per group
        group_stats = {}
        for i, g in enumerate(groups):
            group_stats[f'{g}_mean'] = group_data[i].mean()
            group_stats[f'{g}_median'] = group_data[i].median()
            group_stats[f'{g}_std'] = group_data[i].std()
            group_stats[f'{g}_count'] = len(group_data[i])
        
        # Statistical test
        if test == 'auto':
            # Choose test based on normality and number of groups
            if n_groups == 2:
                # Check normality
                is_normal = all(len(g) >= 3 and shapiro(g)[1] > 0.05 for g in group_data if len(g) > 0)
                if is_normal:
                    stat, pvalue = stats.ttest_ind(*group_data, equal_var=False)
                    test_used = 't-test'
                else:
                    stat, pvalue = stats.mannwhitneyu(*group_data, alternative='two-sided')
                    test_used = 'mann-whitney'
            else:
                # Multiple groups
                try:
                    stat, pvalue = stats.kruskal(*group_data)
                    test_used = 'kruskal-wallis'
                except:
                    stat, pvalue = np.nan, np.nan
                    test_used = 'none'
        elif test == 't-test' and n_groups == 2:
            stat, pvalue = stats.ttest_ind(*group_data, equal_var=False)
            test_used = 't-test'
        elif test == 'mann-whitney' and n_groups == 2:
            stat, pvalue = stats.mannwhitneyu(*group_data, alternative='two-sided')
            test_used = 'mann-whitney'
        elif test == 'anova':
            stat, pvalue = stats.f_oneway(*group_data)
            test_used = 'anova'
        elif test == 'kruskal':
            stat, pvalue = stats.kruskal(*group_data)
            test_used = 'kruskal-wallis'
        else:
            stat, pvalue = np.nan, np.nan
            test_used = 'none'
        
        result_row = {
            'feature': col,
            'test': test_used,
            'statistic': stat,
            'pvalue': pvalue,
            'significant': pvalue < 0.05 if not np.isnan(pvalue) else False,
            **group_stats
        }
        
        results.append(result_row)
    
    return pd.DataFrame(results)


def stratify_by_percentile(df: pd.DataFrame,
                           feature: str,
                           n_groups: int = 4) -> pd.DataFrame:
    """
    Stratify data into percentile-based groups (e.g., quartiles).
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    feature : str
        Feature to stratify by.
    n_groups : int
        Number of groups to create. Default: 4 (quartiles)
    
    Returns
    -------
    pd.DataFrame
        Original dataframe with added group column.
    """
    df = df.copy()
    df[f'{feature}_group'] = pd.qcut(
        df[feature],
        q=n_groups,
        labels=[f'Q{i+1}' for i in range(n_groups)],
        duplicates='drop'
    )
    return df


# =============================================================================
# 6. FEATURE RELATIONSHIPS
# =============================================================================

def analyze_feature_importance(df: pd.DataFrame,
                               target: str,
                               method: str = 'random_forest',
                               top_n: int = 20) -> pd.DataFrame:
    """
    Analyze feature importance relative to a target variable.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    target : str
        Target variable name.
    method : str
        Method: 'random_forest', 'mutual_info', or 'correlation'. Default: 'random_forest'
    top_n : int
        Number of top features to return. Default: 20
    
    Returns
    -------
    pd.DataFrame
        Feature importance scores sorted in descending order.
    """
    feature_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if target in feature_cols:
        feature_cols.remove(target)
    
    df_clean = df[feature_cols + [target]].dropna()
    X = df_clean[feature_cols]
    y = df_clean[target]
    
    if method == 'random_forest':
        from sklearn.ensemble import RandomForestRegressor
        model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
        model.fit(X, y)
        importances = model.feature_importances_
        
    elif method == 'mutual_info':
        from sklearn.feature_selection import mutual_info_regression
        importances = mutual_info_regression(X, y, random_state=42)
        
    elif method == 'correlation':
        importances = np.abs(df_clean[feature_cols].corrwith(df_clean[target]))
    
    else:
        raise ValueError(f"Unknown method: {method}")
    
    importance_df = pd.DataFrame({
        'feature': feature_cols,
        'importance': importances
    }).sort_values('importance', ascending=False)
    
    return importance_df.head(top_n)


def find_nonlinear_relationships(df: pd.DataFrame,
                                 feature1: str,
                                 feature2: str) -> Dict[str, float]:
    """
    Analyze relationship between two features using multiple correlation methods.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    feature1 : str
        First feature name.
    feature2 : str
        Second feature name.
    
    Returns
    -------
    Dict[str, float]
        Correlation coefficients: Pearson (linear), Spearman (monotonic),
        Kendall (concordance), and Distance correlation (general).
    """
    data = df[[feature1, feature2]].dropna()
    
    pearson_corr, pearson_p = stats.pearsonr(data[feature1], data[feature2])
    spearman_corr, spearman_p = stats.spearmanr(data[feature1], data[feature2])
    kendall_corr, kendall_p = stats.kendalltau(data[feature1], data[feature2])
    
    return {
        'feature1': feature1,
        'feature2': feature2,
        'pearson_r': pearson_corr,
        'pearson_p': pearson_p,
        'spearman_r': spearman_corr,
        'spearman_p': spearman_p,
        'kendall_tau': kendall_corr,
        'kendall_p': kendall_p,
        'n_samples': len(data)
    }


# =============================================================================
# 7. DATA QUALITY CHECKS
# =============================================================================

def check_data_quality(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """
    Comprehensive data quality assessment.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    
    Returns
    -------
    Dict[str, pd.DataFrame]
        Dictionary containing multiple quality check results:
        - 'overview': General statistics
        - 'duplicates': Duplicate row analysis
        - 'constant_features': Features with zero or near-zero variance
        - 'missing_data': Missing value summary
    """
    results = {}
    
    # Overview
    results['overview'] = pd.DataFrame({
        'metric': ['total_rows', 'total_columns', 'numeric_columns', 
                   'categorical_columns', 'memory_usage_mb'],
        'value': [
            len(df),
            len(df.columns),
            len(df.select_dtypes(include=[np.number]).columns),
            len(df.select_dtypes(include=['object', 'category']).columns),
            df.memory_usage(deep=True).sum() / 1024 / 1024
        ]
    })
    
    # Duplicates
    duplicate_count = df.duplicated().sum()
    results['duplicates'] = pd.DataFrame({
        'metric': ['duplicate_rows', 'duplicate_pct'],
        'value': [duplicate_count, (duplicate_count / len(df)) * 100]
    })
    
    # Constant or near-constant features
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    constant_features = []
    for col in numeric_cols:
        unique_count = df[col].nunique()
        unique_ratio = unique_count / len(df)
        if unique_count == 1 or unique_ratio < 0.01:
            constant_features.append({
                'feature': col,
                'unique_values': unique_count,
                'unique_ratio': unique_ratio
            })
    results['constant_features'] = pd.DataFrame(constant_features)
    
    # Missing data
    results['missing_data'] = analyze_missing_data(df)
    
    return results


def validate_numeric_ranges(df: pd.DataFrame,
                            expected_ranges: Dict[str, Tuple[float, float]]) -> pd.DataFrame:
    """
    Validate that numeric features fall within expected ranges.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    expected_ranges : Dict[str, Tuple[float, float]]
        Dictionary mapping feature names to (min, max) tuples.
    
    Returns
    -------
    pd.DataFrame
        Validation results with out-of-range counts.
    """
    validation_results = []
    
    for feature, (expected_min, expected_max) in expected_ranges.items():
        if feature not in df.columns:
            continue
        
        actual_min = df[feature].min()
        actual_max = df[feature].max()
        
        below_min = (df[feature] < expected_min).sum()
        above_max = (df[feature] > expected_max).sum()
        out_of_range = below_min + above_max
        
        validation_results.append({
            'feature': feature,
            'expected_min': expected_min,
            'expected_max': expected_max,
            'actual_min': actual_min,
            'actual_max': actual_max,
            'below_min_count': below_min,
            'above_max_count': above_max,
            'out_of_range_total': out_of_range,
            'out_of_range_pct': (out_of_range / len(df)) * 100,
            'is_valid': out_of_range == 0
        })
    
    return pd.DataFrame(validation_results)


# =============================================================================
# 8. COMPREHENSIVE REPORT GENERATION
# =============================================================================

def generate_eda_report(df: pd.DataFrame,
                       target: str = None,
                       group_by: str = None) -> Dict[str, Union[pd.DataFrame, Dict]]:
    """
    Generate a comprehensive EDA report with all available analyses.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    target : str, optional
        Target variable for feature importance analysis.
    group_by : str, optional
        Column to group by for comparison analysis.
    
    Returns
    -------
    Dict
        Comprehensive dictionary containing all analysis results.
    """
    report = {}
    
    print("Generating EDA Report...")
    
    # Basic statistics
    print("  1/10 Computing basic statistics...")
    report['basic_statistics'] = get_basic_statistics(df)
    
    # Normality tests
    print("  2/10 Testing normality...")
    report['normality_tests'] = test_normality(df)
    
    # Correlation analysis
    print("  3/10 Analyzing correlations...")
    report['correlation_matrix'] = get_correlation_matrix(df)
    report['high_correlations'] = find_high_correlations(df, threshold=0.7)
    
    # Outlier detection
    print("  4/10 Detecting outliers (IQR)...")
    report['outliers_iqr'] = detect_outliers_iqr(df)
    
    print("  5/10 Detecting outliers (Z-score)...")
    report['outliers_zscore'] = detect_outliers_zscore(df)
    
    # Missing data
    print("  6/10 Analyzing missing data...")
    report['missing_data'] = analyze_missing_data(df)
    
    # Data quality
    print("  7/10 Checking data quality...")
    report['data_quality'] = check_data_quality(df)
    
    # Group comparisons
    if group_by and group_by in df.columns:
        print(f"  8/10 Comparing groups by {group_by}...")
        report['group_comparison'] = compare_groups(df, group_by)
    else:
        print("  8/10 Skipping group comparison (no group_by specified)...")
        report['group_comparison'] = None
    
    # Feature importance
    if target and target in df.columns:
        print(f"  9/10 Analyzing feature importance for {target}...")
        try:
            report['feature_importance_rf'] = analyze_feature_importance(df, target, method='random_forest')
            report['feature_importance_corr'] = analyze_feature_importance(df, target, method='correlation')
        except Exception as e:
            print(f"    Warning: Could not compute feature importance: {e}")
            report['feature_importance_rf'] = None
            report['feature_importance_corr'] = None
    else:
        print("  9/10 Skipping feature importance (no target specified)...")
        report['feature_importance_rf'] = None
        report['feature_importance_corr'] = None
    
    # Percentile distribution
    print("  10/10 Computing percentile distributions...")
    report['percentile_distribution'] = get_percentile_distribution(df)
    
    print("EDA Report Complete!")
    
    return report


def print_report_summary(report: Dict) -> None:
    """
    Print a human-readable summary of the EDA report.
    
    Parameters
    ----------
    report : Dict
        Report dictionary generated by generate_eda_report().
    """
    print("\n" + "="*80)
    print("EXPLORATORY DATA ANALYSIS REPORT SUMMARY")
    print("="*80)
    
    # Basic info
    if 'data_quality' in report and 'overview' in report['data_quality']:
        overview = report['data_quality']['overview']
        print("\n📊 DATASET OVERVIEW")
        print("-" * 80)
        for _, row in overview.iterrows():
            print(f"  {row['metric']:.<30} {row['value']:.2f}")
    
    # Missing data
    if 'missing_data' in report:
        missing = report['missing_data']
        missing_cols = missing[missing['missing_count'] > 0]
        print(f"\n❓ MISSING DATA")
        print("-" * 80)
        if len(missing_cols) > 0:
            print(f"  Columns with missing data: {len(missing_cols)}")
            for _, row in missing_cols.head(5).iterrows():
                print(f"    {row['column']:.<30} {row['missing_count']} ({row['missing_pct']:.2f}%)")
        else:
            print("  ✓ No missing data found!")
    
    # Outliers
    if 'outliers_iqr' in report:
        outlier_summary = report['outliers_iqr']['summary']
        high_outliers = outlier_summary[outlier_summary['outlier_pct'] > 5]
        print(f"\n⚠️  OUTLIERS (IQR method)")
        print("-" * 80)
        if len(high_outliers) > 0:
            print(f"  Features with >5% outliers: {len(high_outliers)}")
            for _, row in high_outliers.head(5).iterrows():
                print(f"    {row['feature']:.<30} {row['outlier_count']} ({row['outlier_pct']:.2f}%)")
        else:
            print("  ✓ No features with excessive outliers (>5%)")
    
    # High correlations
    if 'high_correlations' in report:
        high_corr = report['high_correlations']
        print(f"\n🔗 HIGH CORRELATIONS (|r| > 0.7)")
        print("-" * 80)
        if len(high_corr) > 0:
            print(f"  Found {len(high_corr)} highly correlated feature pairs")
            for _, row in high_corr.head(5).iterrows():
                print(f"    {row['feature_1']} ↔ {row['feature_2']}: {row['correlation']:.3f}")
        else:
            print("  ✓ No high correlations found")
    
    # Feature importance
    if 'feature_importance_rf' in report and report['feature_importance_rf'] is not None:
        feat_imp = report['feature_importance_rf']
        print(f"\n⭐ TOP 10 MOST IMPORTANT FEATURES (Random Forest)")
        print("-" * 80)
        for i, row in feat_imp.head(10).iterrows():
            print(f"  {i+1:2d}. {row['feature']:.<30} {row['importance']:.4f}")
    
    print("\n" + "="*80 + "\n")
