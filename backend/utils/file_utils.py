"""
File and folder utility functions.

Provides general file system operations like checking existence,
creating directories, and managing file metadata.
"""
import os
from typing import Optional


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
    
    Args:
        filepath: Path to the file to check
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


def get_file_size(filepath: str) -> int:
    """
    Get the size of a file in bytes.
    
    Args:
        filepath: Path to the file
        
    Returns:
        File size in bytes, or 0 if file doesn't exist
    """
    try:
        return os.path.getsize(filepath)
    except (OSError, FileNotFoundError):
        return 0


def delete_file(filepath: str) -> bool:
    """
    Delete a file if it exists.
    
    Args:
        filepath: Path to the file to delete
        
    Returns:
        True if file was deleted, False otherwise
    """
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False
    except OSError:
        return False
