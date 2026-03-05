"""
Utility modules for the Nutrition-AI backend.

Provides file operations, CSV handling, and DataFrame utilities.
"""
from .file_utils import (
    file_exists,
    ensure_directory,
    ensure_trailing_newline,
    get_file_size,
    delete_file,
)
from .csv_utils import (
    get_next_id,
    append_to_csv,
    get_row_count,
)
from .dataframe_utils import (
    csv_to_dataframe,
    read_csv,
    dataframe_to_csv,
)

__all__ = [
    # File utilities
    "file_exists",
    "ensure_directory",
    "ensure_trailing_newline",
    "get_file_size",
    "delete_file",
    # CSV utilities
    "get_next_id",
    "append_to_csv",
    "get_row_count",
    # DataFrame utilities
    "csv_to_dataframe",
    "read_csv",
    "dataframe_to_csv",
]


__all__ = [
    'file_exists',
    'ensure_directory',
    'get_next_id',
    'append_to_csv',
    'read_csv',
    'get_row_count',
    'csv_to_dataframe',
]