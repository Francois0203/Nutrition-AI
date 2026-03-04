"""
Utility helpers for creating pandas DataFrames from CSV files.

This module provides a single, generalised function `csv_to_dataframe`
that reads a CSV file whose first row contains the header and returns
a pandas DataFrame. It exposes common read options so callers can
customise parsing behaviour.
"""
from typing import Optional, Sequence, Union, Dict
import os
import pandas as pd


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
    """Read a CSV file into a pandas DataFrame.

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
    if not os.path.exists(filepath):
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
