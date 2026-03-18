"""
CSV file utility functions for reading, writing, and appending data.

Provides functions for common CSV operations like appending rows,
getting next ID values, and row counts.
"""
import csv
import pandas as pd
from typing import List, Optional
from .file_utils import file_exists, ensure_directory, ensure_trailing_newline


def get_next_id(filepath: str, id_column: str = 'ID') -> int:
    """
    Get the next available ID from a CSV file.
    
    Args:
        filepath: Path to the CSV file
        id_column: Name of the ID column (default: 'ID')
        
    Returns:
        Next available ID (1 if file doesn't exist or is empty)
    """
    if not file_exists(filepath):
        return 1
    
    try:
        df = pd.read_csv(filepath)
        if df.empty or id_column not in df.columns:
            return 1
        return int(df[id_column].max()) + 1
    except (pd.errors.EmptyDataError, ValueError):
        return 1


def append_to_csv(filepath: str, data: List[dict], create_if_missing: bool = True) -> int:
    """
    Append data to a CSV file. Creates the file if it doesn't exist.
    
    Args:
        filepath: Path to the CSV file
        data: List of dictionaries containing the data to append
        create_if_missing: If True, creates file with headers if it doesn't exist
        
    Returns:
        Number of rows appended
    """
    if not data:
        return 0
    
    ensure_directory(filepath)

    file_is_new = not file_exists(filepath)

    # If file exists, ensure it ends with a newline so appended rows start on
    # a new line rather than continuing the last line.
    if not file_is_new:
        ensure_trailing_newline(filepath)

    with open(filepath, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())

        # Write header only for new files
        if file_is_new and create_if_missing:
            writer.writeheader()

        writer.writerows(data)
    
    return len(data)


def get_row_count(filepath: str) -> int:
    """
    Get the number of rows in a CSV file (excluding header).
    
    Args:
        filepath: Path to the CSV file
        
    Returns:
        Number of rows, or 0 if file doesn't exist
    """
    if not file_exists(filepath):
        return 0
    
    try:
        df = pd.read_csv(filepath)
        return len(df)
    except Exception:
        return 0
