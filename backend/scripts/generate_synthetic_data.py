#!/usr/bin/env python3
"""
generate_synthetic_data.py
==========================
Entry point script for generating synthetic body measurement data.

Usage:
    python scripts/generate_synthetic_data.py --count 100
    python scripts/generate_synthetic_data.py -c 50 -o data/custom.csv
"""
import argparse
import sys
import os

# Add parent directory to path to import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_generation import generate_data


# Configuration
DATA_DIR = "data"
RAW_DATA_DIR = f"{DATA_DIR}/raw"
OUTPUT_FILE = f"{RAW_DATA_DIR}/Body Measurements.csv"


def main():
    """
    Main function to handle command-line arguments and generate data.
    """
    parser = argparse.ArgumentParser(
        description='Generate synthetic body measurements data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --count 100              Generate 100 records
  %(prog)s -c 50 -o custom.csv      Generate 50 records to custom file
  %(prog)s                          Generate 10 records (default)
        """
    )
    
    parser.add_argument(
        '-c', '--count',
        type=int,
        default=10,
        help='Number of records to generate (default: 10)'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default=OUTPUT_FILE,
        help=f'Output file path (default: {OUTPUT_FILE})'
    )
    
    args = parser.parse_args()
    
    # Validate input
    if args.count <= 0:
        print("Error: Count must be a positive number")
        return
    
    # Generate data
    generate_data(args.count, args.output)


if __name__ == "__main__":
    main()
