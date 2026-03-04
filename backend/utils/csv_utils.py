"""
Reusable CSV file utility functions for data generation.
"""
import os
import csv
import pandas as pd
from typing import List, Optional


def file_exists(filepath: str) -> bool:
    """
    Check if a file exists at the given path.
    
    Args:
        filepath: Path to the file to check
        
    Returns:
        True if file exists, False otherwise
    """
    return os.path.exists(filepath)


def ensure_directory(filepath: str) -> None:
    """
    Ensure the directory for the given filepath exists.
    Creates parent directories if they don't exist.
    
    Args:
        filepath: Path to a file whose directory should exist
    """
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)


def ensure_trailing_newline(filepath: str) -> None:
    """
    Ensure the file ends with a newline character. If the file exists and does
    not end with a newline, append one. This prevents appended CSV rows from
    being placed on the same line as the last existing row.
    """
    try:
        if not os.path.exists(filepath):
            return
        if os.path.getsize(filepath) == 0:
            return
        # Open in binary to safely check last byte
        with open(filepath, 'rb') as f:
            f.seek(-1, os.SEEK_END)
            last = f.read(1)
            if last not in (b"\n", b"\r"):
                # Append a newline in text mode
                with open(filepath, 'a', encoding='utf-8', newline='') as fa:
                    fa.write('\n')
    except (OSError, ValueError):
        # If unable to check (e.g., small file), skip gracefully
        return


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


def read_csv(filepath: str) -> Optional[pd.DataFrame]:
    """
    Read a CSV file into a pandas DataFrame.
    
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
