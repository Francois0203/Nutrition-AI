#!/usr/bin/env python3
"""
generate_features.py
===================
Generate a new CSV file with all engineered features added to the dataset.

This script reads the raw body measurements data, applies all feature engineering
transformations, and outputs a new CSV file with the original data plus all
derived features.

Usage:
    python scripts/generate_features.py
    python scripts/generate_features.py -i data/raw/custom.csv -o data/processed/features.csv
"""
import argparse
import sys
import os

# Add parent directory to path to import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.features import engineer_all_features
from utils.dataframe_utils import csv_to_dataframe, dataframe_to_csv
from utils.file_utils import file_exists


# Configuration
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
DEFAULT_INPUT = os.path.join(DATA_DIR, "Body Measurements.csv")
DEFAULT_OUTPUT = os.path.join(DATA_DIR, "Body Measurements with Features.csv")


def generate_features_csv(input_file: str, output_file: str) -> None:
    """
    Read raw data, apply feature engineering, and save to output CSV.
    
    Args:
        input_file: Path to input CSV file with raw measurements
        output_file: Path to output CSV file with engineered features
    """
    # Validate input file
    if not file_exists(input_file):
        print(f"[ERROR] Input file not found: {input_file}")
        return
    
    print(f"Reading data from: {input_file}")
    
    # Read the raw data
    try:
        df = csv_to_dataframe(input_file)
        print(f"[OK] Loaded {len(df)} records with {len(df.columns)} columns")
    except Exception as e:
        print(f"[ERROR] Error reading CSV: {e}")
        return
    
    # Apply feature engineering
    print("\nApplying feature engineering...")
    try:
        df_features = engineer_all_features(df)
        new_features_count = len(df_features.columns) - len(df.columns)
        print(f"[OK] Generated {new_features_count} new features")
        print(f"[OK] Total columns: {len(df_features.columns)}")
    except Exception as e:
        print(f"[ERROR] Error during feature engineering: {e}")
        return
    
    # Save to output file
    print(f"\nSaving to: {output_file}")
    try:
        success = dataframe_to_csv(df_features, output_file)
        if success:
            print(f"[OK] Successfully saved {len(df_features)} records")
            print(f"[OK] Output file: {output_file}")
            
            # Display feature categories
            print("\n[INFO] Feature Categories:")
            print(f"   - Body Composition Indices: bmi, bsa_mosteller, ffmi, etc.")
            print(f"   - Obesity & Adiposity Ratios: waist_hip_ratio, waist_height_ratio, etc.")
            print(f"   - Limb Proportions: upper_lower_limb_ratio, calf_thigh_ratio, etc.")
            print(f"   - Muscle & Frame Features: frame_size_index, skeletal_muscle_index, etc.")
        else:
            print(f"[ERROR] Failed to save output file")
    except Exception as e:
        print(f"[ERROR] Error saving CSV: {e}")
        return


def main():
    """
    Main function to handle command-line arguments and generate features.
    """
    parser = argparse.ArgumentParser(
        description='Generate CSV with engineered features from body measurements',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                                  Use default input/output paths
  %(prog)s -i custom.csv                    Use custom input file
  %(prog)s -i raw.csv -o features.csv       Use custom input and output files
        """
    )
    
    parser.add_argument(
        '-i', '--input',
        type=str,
        default=DEFAULT_INPUT,
        help=f'Input CSV file path (default: {DEFAULT_INPUT})'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default=DEFAULT_OUTPUT,
        help=f'Output CSV file path (default: {DEFAULT_OUTPUT})'
    )
    
    args = parser.parse_args()
    
    # Generate features
    print("=" * 70)
    print("BODY MEASUREMENTS FEATURE ENGINEERING")
    print("=" * 70)
    generate_features_csv(args.input, args.output)
    print("=" * 70)


if __name__ == "__main__":
    main()