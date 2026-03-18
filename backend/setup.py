"""
Setup script for Nutrition AI Backend
Automatically prepares the backend: preprocessing, training models, and setup
"""

import sys
import subprocess
from pathlib import Path
import os

def run_command(command, description):
    """Run a command and print status"""
    print(f"\n{'='*60}")
    print(f"  {description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(command, check=True, capture_output=False)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed with error code {e.returncode}")
        return False
    except Exception as e:
        print(f"✗ {description} failed: {e}")
        return False

def check_path(path, description):
    """Check if a path exists"""
    if path.exists():
        print(f"✓ {description} exists")
        return True
    else:
        print(f"✗ {description} not found")
        return False

def main():
    print("\n" + "="*60)
    print("  Nutrition AI - Backend Setup")
    print("="*60)
    
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    # Check data
    data_file = backend_dir / "Data" / "Body Measurements.csv"
    if not check_path(data_file, "Training data"):
        print("\n⚠ Error: Training data not found!")
        print(f"  Expected: {data_file}")
        return False
    
    # Check if models already exist
    models_dir = backend_dir / "models"
    preprocessor_file = backend_dir / "Data" / "preprocessor.pkl"
    
    models_exist = models_dir.exists() and len(list(models_dir.glob("*/*.pkl"))) > 0
    preprocessor_exists = preprocessor_file.exists()
    
    if models_exist and preprocessor_exists:
        print("\n✓ Models and preprocessor already exist!")
        print("\nOptions:")
        print("  1. Use existing models (recommended)")
        print("  2. Retrain all models")
        
        choice = input("\nEnter choice (1 or 2): ").strip()
        
        if choice == "1":
            print("\n✓ Using existing models")
            print("\nSetup complete! You can now run:")
            print("  python app.py")
            return True
        elif choice != "2":
            print("Invalid choice. Exiting.")
            return False
    
    # Step 1: Run preprocessing
    print("\n" + "="*60)
    print("  Step 1: Data Preprocessing")
    print("="*60)
    
    preprocess_script = backend_dir / "scripts" / "run_preprocessing.py"
    if not check_path(preprocess_script, "Preprocessing script"):
        print("⚠ Cannot proceed without preprocessing script")
        return False
    
    if not run_command([sys.executable, str(preprocess_script)], "Data preprocessing"):
        print("\n⚠ Preprocessing failed. Please check errors above.")
        return False
    
    # Step 2: Train all models
    print("\n" + "="*60)
    print("  Step 2: Training ML Models")
    print("="*60)
    print("  This may take several minutes...")
    
    train_script = backend_dir / "scripts" / "train_all_models.py"
    if not check_path(train_script, "Training script"):
        print("⚠ Cannot proceed without training script")
        return False
    
    if not run_command([sys.executable, str(train_script)], "Model training"):
        print("\n⚠ Training failed. Please check errors above.")
        return False
    
    # Verify setup
    print("\n" + "="*60)
    print("  Verifying Setup")
    print("="*60)
    
    all_good = True
    all_good &= check_path(backend_dir / "Data" / "preprocessor.pkl", "Preprocessor")
    all_good &= check_path(backend_dir / "models", "Models directory")
    
    if all_good:
        print("\n" + "="*60)
        print("  ✓ Setup Complete!")
        print("="*60)
        print("\nBackend is ready! You can now:")
        print("  1. Start the API server:")
        print("     python app.py")
        print("\n  2. Test the API:")
        print("     curl http://localhost:5000/api/health")
        print("\n  3. Start the frontend (in another terminal):")
        print("     cd ../frontend")
        print("     npm install")
        print("     npm run dev")
        return True
    else:
        print("\n⚠ Setup incomplete. Some files are missing.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
