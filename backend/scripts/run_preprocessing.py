"""
Run preprocessing on the dataset and generate preprocessed CSV files.
Handles dirty data with cleaning pipeline.
"""

import sys
from pathlib import Path

# Add src to path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
src_path = project_root / 'src'
sys.path.insert(0, str(src_path))

from preprocessing import load_and_preprocess_data, save_preprocessed_data

def main():
    """Main preprocessing pipeline with data cleaning."""
    # Paths
    data_path = project_root / 'Data' / 'Body Measurements with Features.csv'
    output_dir = project_root / 'Data' / 'preprocessed'
    preprocessor_path = project_root / 'Data' / 'preprocessor.pkl'
    
    # Load and preprocess data with cleaning enabled
    X_train, X_test, y_train, y_test, preprocessor, feature_names = load_and_preprocess_data(
        data_path=data_path,
        test_size=0.2,
        random_state=42,
        clean_dirty_data=True,      # ✅ Enable data cleaning pipeline
        use_knn_imputation=False    # Set to True for better imputation (slower)
    )
    
    # Save preprocessed data to CSV
    save_preprocessed_data(
        X_train, X_test, y_train, y_test, 
        feature_names, 
        output_dir
    )
    
    # Save the preprocessor for future use
    preprocessor.save(preprocessor_path)
    
    print("\n✅ Preprocessing complete!")
    print(f"   Preprocessor saved to: {preprocessor_path}")
    print(f"   Ready for model training!")

if __name__ == '__main__':
    main()
