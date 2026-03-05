"""
DataFrame utility functions.

Provides functions for reading various file formats into pandas DataFrames
with common parsing options and error handling.
"""
from typing import Optional, Sequence, Union, Dict
import pandas as pd
from .file_utils import file_exists


def csv_to_dataframe(
    filepath: str,
    sep: str = ',',
    encoding: str = 'utf-8',
    header_row: int = 0,
    dtype: Optional[Union[type, Dict[str, type]]] = None,
    parse_dates: Optional[Union[str, Sequence[str], bool]] = None,
    usecols: Optional[Sequence[str]] = None,
    na_values: Optional[Union[str, Sequence[str]]] = None,
    keep_default_na: bool = True,
    skip_blank_lines: bool = True,
) -> pd.DataFrame:
    """
    Read a CSV file into a pandas DataFrame.

    The function assumes the first row of the CSV file contains the
    column headers by default (`header_row=0`). It returns a pandas
    DataFrame or raises an informative exception if the file cannot be
    read.

    Args:
        filepath: Path to the CSV file.
        sep: Column separator character (default: ',').
        encoding: File encoding (default: 'utf-8').
        header_row: Row index to use as column names (default: 0).
        dtype: Data type or dict of column->type to apply.
        parse_dates: Columns to parse as dates.
        usecols: Subset of columns to read.
        na_values: Additional strings to consider as NA/NaN.
        keep_default_na: Whether to include the default NA values.
        skip_blank_lines: Whether to skip blank lines rather than parse as NaN.

    Returns:
        pandas.DataFrame: The loaded DataFrame.

    Raises:
        FileNotFoundError: If the `filepath` does not exist.
        pd.errors.EmptyDataError: If the file is empty.
        pd.errors.ParserError: If parsing fails.
    """
    if not file_exists(filepath):
        raise FileNotFoundError(f"CSV file not found: {filepath}")

    # pandas uses 0-based index for header rows; pass header_row directly
    df = pd.read_csv(
        filepath,
        sep=sep,
        encoding=encoding,
        header=header_row,
        dtype=dtype,
        parse_dates=parse_dates,
        usecols=usecols,
        na_values=na_values,
        keep_default_na=keep_default_na,
        skip_blank_lines=skip_blank_lines,
    )

    return df


def read_csv(filepath: str) -> Optional[pd.DataFrame]:
    """
    Read a CSV file into a pandas DataFrame with default settings.
    
    Args:
        filepath: Path to the CSV file
        
    Returns:
        DataFrame if successful, None if file doesn't exist or error occurs
    """
    if not file_exists(filepath):
        return None
    
    try:
        return pd.read_csv(filepath)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return None


def dataframe_to_csv(
    df: pd.DataFrame,
    filepath: str,
    index: bool = False,
    encoding: str = 'utf-8',
    **kwargs
) -> bool:
    """
    Write a DataFrame to a CSV file.
    
    Args:
        df: DataFrame to write
        filepath: Path to the output CSV file
        index: Whether to write row indices (default: False)
        encoding: File encoding (default: 'utf-8')
        **kwargs: Additional arguments passed to df.to_csv()
        
    Returns:
        True if successful, False otherwise
    """
    try:
        from .file_utils import ensure_directory
        ensure_directory(filepath)
        df.to_csv(filepath, index=index, encoding=encoding, **kwargs)
        return True
    except Exception as e:
        print(f"Error writing CSV: {e}")
        return False
