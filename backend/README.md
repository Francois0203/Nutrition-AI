# Nutrition-AI Backend

A well-structured backend for body composition analysis and nutritional AI features.

## 📁 Project Structure

```
backend/
├── data/                          # Data directory
│   ├── raw/                      # Raw data files
│   │   └── Body Measurements.csv
│   └── processed/                # Processed data with features
│       └── Body Measurements with Features.csv
│
├── scripts/                      # Entry point scripts
│   ├── generate_synthetic_data.py  # Generate synthetic body measurements
│   └── generate_features.py        # Generate CSV with engineered features
│
├── src/                          # Source code modules
│   ├── features/                 # Feature engineering
│   │   ├── __init__.py
│   │   └── engineering.py        # Body composition feature engineering
│   ├── analysis/                 # Data analysis utilities
│   │   ├── __init__.py
│   │   └── stats.py              # Statistical analysis functions
│   └── data_generation/          # Synthetic data generation
│       ├── __init__.py
│       └── synthetic.py          # Synthetic measurement generation
│
├── utils/                        # Utility modules
│   ├── __init__.py
│   ├── csv_utils.py              # CSV operations (read, write, append)
│   ├── file_utils.py             # File/folder operations
│   └── dataframe_utils.py        # DataFrame utilities
│
├── requirements.txt              # Python dependencies
├── .gitignore                    # Git ignore patterns
└── README.md                     # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate Synthetic Data

Generate sample body measurement data:

```bash
# Generate 100 records
python scripts/generate_synthetic_data.py --count 100

# Custom output file
python scripts/generate_synthetic_data.py -c 50 -o data/raw/custom.csv
```

### 3. Generate Features

Apply feature engineering to create derived features:

```bash
# Use default paths
python scripts/generate_features.py

# Custom input/output
python scripts/generate_features.py -i data/raw/custom.csv -o data/processed/features.csv
```

## 📊 Feature Engineering

The `generate_features.py` script generates **30+ research-backed features** in 4 categories:

### 1. Body Composition Indices
- BMI (Body Mass Index)
- BSA (Body Surface Area - Mosteller)
- Fat Mass Index (FMI)
- Fat-Free Mass Index (FFMI)
- Lean mass and fat mass calculations

### 2. Obesity & Adiposity Ratios
- Waist-Hip Ratio (WHR)
- Waist-Height Ratio (WHtR)
- Body Adiposity Index (BAI)
- Conicity Index
- Abdominal Volume Index (AVI)
- Waist-Neck Ratio

### 3. Limb Proportions
- Upper/Lower limb ratios
- Calf-Thigh ratio
- Arm-Trunk ratio
- Shoulder-Waist ratio (Adonis Index)
- Chest-Waist ratio
- Hip-Waist difference

### 4. Muscle & Frame Features
- Frame Size Index
- Relative Muscle Mass (RMM)
- Muscle-to-Fat Ratio
- Skeletal Muscle Index (SMI)
- Bicep-to-Wrist Ratio
- Calf Muscle Index

All features include scientific references in the source code.

## 🛠️ Utilities

### File Utilities (`utils/file_utils.py`)
- File existence checks
- Directory creation
- File metadata operations

### CSV Utilities (`utils/csv_utils.py`)
- Append rows to CSV
- Get next available ID
- Row counting

### DataFrame Utilities (`utils/dataframe_utils.py`)
- CSV to DataFrame conversion
- DataFrame to CSV export
- Flexible parsing options

## 📝 Module Usage

### Feature Engineering

```python
from src.features import engineer_all_features
from utils.dataframe_utils import csv_to_dataframe

# Load data
df = csv_to_dataframe("data/raw/Body Measurements.csv")

# Generate all features
df_with_features = engineer_all_features(df)

# Or apply specific feature groups
from src.features.engineering import (
    add_body_composition_indices,
    add_obesity_ratios,
    add_limb_proportions,
    add_muscle_and_frame_features
)

df = add_body_composition_indices(df)
df = add_obesity_ratios(df)
# etc.
```

### Synthetic Data Generation

```python
from src.data_generation import generate_measurement, generate_data

# Generate a single measurement
measurement = generate_measurement()

# Generate and save multiple records
generate_data(num_records=100, output_file="data/raw/output.csv")
```

### Data Analysis

```python
from src.analysis.stats import (
    get_basic_stats,
    check_missing_values,
    get_correlation_matrix,
    check_outliers_iqr
)

# Get statistical summary
stats = get_basic_stats(df)

# Check for missing values
missing = check_missing_values(df)

# Get correlations
corr_matrix = get_correlation_matrix(df)
```

## 🔬 Data Format

### Raw Data Columns
- `Age`: Age in years (18-65)
- `Sex`: M/F
- `Height_cm`: Height in centimeters
- `Weight_kg`: Weight in kilograms
- `BodyFatPct`: Body fat percentage
- `MuscleMass_kg`: Muscle mass in kilograms
- Circumference measurements: Wrist, Waist, Hip, Neck, UpperArm, Thigh, Calf, Forearm, Chest, Shoulder, Ankle, Bicep (all in cm)

## 📚 References

All feature engineering functions include scientific references from:
- WHO guidelines
- Peer-reviewed medical journals
- Validated anthropometric assessments

See inline documentation in `src/features/engineering.py` for specific citations.

## 🤝 Contributing

When adding new features:
1. Place core logic in appropriate `src/` subdirectory
2. Add utility functions to `utils/` if reusable
3. Create entry scripts in `scripts/` for user-facing operations
4. Update this README with new functionality

## 📄 License

[Add your license information here]
