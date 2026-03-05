"""
synthetic.py
===========
Generate synthetic body measurements data using normal distributions.

Data is generated to closely match real-world population statistics.
All measurements are generated with realistic correlations and constraints.
"""
import random
import numpy as np
from typing import Dict


# Normal distribution parameters (mean, std_dev) based on real population data
# Age follows a uniform distribution to ensure diverse age representation
AGE_RANGE = (18, 65)

# Body measurements with realistic means and standard deviations
DISTRIBUTIONS = {
    'Height_cm': {
        'M': {'mean': 176.5, 'std': 7.5},  # Average adult male height
        'F': {'mean': 163.0, 'std': 6.5}   # Average adult female height
    },
    'Weight_kg': {
        'M': {'mean': 82.0, 'std': 15.0},  # Average adult male weight
        'F': {'mean': 65.0, 'std': 13.0}   # Average adult female weight
    },
    'Wrist_cm': {
        'M': {'mean': 18.0, 'std': 0.8},
        'F': {'mean': 15.5, 'std': 0.7}
    },
    'Waist_cm': {
        'M': {'mean': 88.0, 'std': 10.0},
        'F': {'mean': 76.0, 'std': 10.5}
    },
    'Hip_cm': {
        'M': {'mean': 98.0, 'std': 7.0},
        'F': {'mean': 100.0, 'std': 8.0}
    },
    'Neck_cm': {
        'M': {'mean': 38.5, 'std': 2.0},
        'F': {'mean': 33.5, 'std': 1.5}
    },
    'UpperArm_cm': {
        'M': {'mean': 32.0, 'std': 2.5},
        'F': {'mean': 28.0, 'std': 2.0}
    },
    'Thigh_cm': {
        'M': {'mean': 56.0, 'std': 4.0},
        'F': {'mean': 52.0, 'std': 3.5}
    },
    'Calf_cm': {
        'M': {'mean': 38.5, 'std': 2.5},
        'F': {'mean': 35.5, 'std': 2.0}
    },
    'Forearm_cm': {
        'M': {'mean': 28.5, 'std': 2.0},
        'F': {'mean': 24.5, 'std': 1.5}
    },
    'Chest_cm': {
        'M': {'mean': 100.0, 'std': 8.0},
        'F': {'mean': 90.0, 'std': 8.0}
    },
    'Shoulder_cm': {
        'M': {'mean': 41.5, 'std': 2.5},
        'F': {'mean': 36.5, 'std': 2.0}
    },
    'Ankle_cm': {
        'M': {'mean': 23.5, 'std': 1.5},
        'F': {'mean': 21.5, 'std': 1.2}
    },
    'Bicep_cm': {
        'M': {'mean': 35.0, 'std': 2.5},
        'F': {'mean': 30.0, 'std': 2.0}
    },
    'BodyFatPct': {
        'M': {'mean': 20.0, 'std': 5.0},   # Typical male body fat percentage
        'F': {'mean': 28.0, 'std': 5.5}    # Typical female body fat percentage
    }
}


def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp a value between min and max."""
    return max(min_val, min(max_val, value))


def calculate_muscle_mass(weight: float, body_fat_pct: float) -> float:
    """
    Calculate approximate muscle mass based on weight and body fat percentage.
    
    Args:
        weight: Body weight in kg
        body_fat_pct: Body fat percentage
        
    Returns:
        Estimated muscle mass in kg
    """
    lean_mass = weight * (1 - body_fat_pct / 100)
    # Muscle is approximately 42% of body weight with some variation
    muscle_pct = np.random.normal(0.42, 0.03)
    muscle_mass = weight * clamp(muscle_pct, 0.30, 0.55)
    return round(muscle_mass, 1)


def generate_measurement() -> Dict:
    """
    Generate a single realistic body measurement record using normal distributions.
    Measurements are correlated where appropriate (e.g., height and weight).
        
    Returns:
        Dictionary containing all body measurements
    """
    age = random.randint(*AGE_RANGE)
    sex = random.choice(['M', 'F'])
    
    # Generate height from normal distribution
    height_params = DISTRIBUTIONS['Height_cm'][sex]
    height = np.random.normal(height_params['mean'], height_params['std'])
    height = clamp(height, 145, 210)  # Reasonable bounds
    height = round(height)
    
    # Generate weight with correlation to height (taller people tend to weigh more)
    weight_params = DISTRIBUTIONS['Weight_kg'][sex]
    height_factor = (height - height_params['mean']) / height_params['std']  # z-score
    weight_mean_adjusted = weight_params['mean'] + height_factor * 5  # Correlation adjustment
    weight = np.random.normal(weight_mean_adjusted, weight_params['std'])
    weight = clamp(weight, 40, 150)
    weight = round(weight)
    
    # Calculate BMI to adjust body fat percentage realistically
    bmi = weight / ((height / 100) ** 2)
    
    # Generate body fat percentage (correlated with BMI)
    body_fat_params = DISTRIBUTIONS['BodyFatPct'][sex]
    bmi_adjustment = (bmi - 22) * 1.5  # Adjust based on BMI deviation from normal
    body_fat_pct = np.random.normal(body_fat_params['mean'] + bmi_adjustment, body_fat_params['std'])
    body_fat_pct = clamp(body_fat_pct, 8, 45)
    body_fat_pct = round(body_fat_pct)
    
    # Generate other measurements from normal distributions
    wrist = round(np.random.normal(loc=DISTRIBUTIONS['Wrist_cm'][sex]['mean'], scale=DISTRIBUTIONS['Wrist_cm'][sex]['std']))
    wrist = clamp(wrist, 13, 23)
    
    # Waist correlated with body fat and weight
    waist_params = DISTRIBUTIONS['Waist_cm'][sex]
    waist_mean_adjusted = waist_params['mean'] + (body_fat_pct - body_fat_params['mean']) * 0.8
    waist = round(np.random.normal(waist_mean_adjusted, waist_params['std']))
    waist = clamp(waist, 55, 130)
    
    hip = round(np.random.normal(loc=DISTRIBUTIONS['Hip_cm'][sex]['mean'], scale=DISTRIBUTIONS['Hip_cm'][sex]['std']))
    hip = clamp(hip, 75, 130)
    
    neck = round(np.random.normal(loc=DISTRIBUTIONS['Neck_cm'][sex]['mean'], scale=DISTRIBUTIONS['Neck_cm'][sex]['std']))
    neck = clamp(neck, 28, 48)
    
    upper_arm = round(np.random.normal(loc=DISTRIBUTIONS['UpperArm_cm'][sex]['mean'], scale=DISTRIBUTIONS['UpperArm_cm'][sex]['std']))
    upper_arm = clamp(upper_arm, 22, 45)
    
    thigh = round(np.random.normal(loc=DISTRIBUTIONS['Thigh_cm'][sex]['mean'], scale=DISTRIBUTIONS['Thigh_cm'][sex]['std']))
    thigh = clamp(thigh, 40, 75)
    
    calf = round(np.random.normal(loc=DISTRIBUTIONS['Calf_cm'][sex]['mean'], scale=DISTRIBUTIONS['Calf_cm'][sex]['std']))
    calf = clamp(calf, 28, 48)
    
    forearm = round(np.random.normal(loc=DISTRIBUTIONS['Forearm_cm'][sex]['mean'], scale=DISTRIBUTIONS['Forearm_cm'][sex]['std']))
    forearm = clamp(forearm, 20, 38)
    
    # Chest correlated with weight and height
    chest_params = DISTRIBUTIONS['Chest_cm'][sex]
    chest_mean_adjusted = chest_params['mean'] + (weight - weight_params['mean']) / weight_params['std'] * 2
    chest = round(np.random.normal(chest_mean_adjusted, chest_params['std']))
    chest = clamp(chest, 70, 140)
    
    shoulder = round(np.random.normal(loc=DISTRIBUTIONS['Shoulder_cm'][sex]['mean'], scale=DISTRIBUTIONS['Shoulder_cm'][sex]['std']))
    shoulder = clamp(shoulder, 32, 52)
    
    ankle = round(np.random.normal(loc=DISTRIBUTIONS['Ankle_cm'][sex]['mean'], scale=DISTRIBUTIONS['Ankle_cm'][sex]['std']))
    ankle = clamp(ankle, 18, 30)
    
    bicep = round(np.random.normal(loc=DISTRIBUTIONS['Bicep_cm'][sex]['mean'], scale=DISTRIBUTIONS['Bicep_cm'][sex]['std']))
    bicep = clamp(bicep, 24, 48)
    
    # Calculate derived measurements
    muscle_mass = calculate_muscle_mass(weight, body_fat_pct)
    
    return {
        'Age': age,
        'Sex': sex,
        'Height_cm': height,
        'Weight_kg': weight,
        'Wrist_cm': wrist,
        'Waist_cm': waist,
        'Hip_cm': hip,
        'Neck_cm': neck,
        'UpperArm_cm': upper_arm,
        'Thigh_cm': thigh,
        'Calf_cm': calf,
        'Forearm_cm': forearm,
        'Chest_cm': chest,
        'Shoulder_cm': shoulder,
        'Ankle_cm': ankle,
        'Bicep_cm': bicep,
        'BodyFatPct': body_fat_pct,
        'MuscleMass_kg': muscle_mass
    }


def generate_data(num_records: int, output_file: str) -> int:
    """
    Generate and save body measurement data.
    
    Args:
        num_records: Number of records to generate
        output_file: Path to the output CSV file
        
    Returns:
        Number of rows added to the file
    """
    from utils.csv_utils import append_to_csv, get_row_count
    from utils.file_utils import file_exists
    
    # Generate data
    print(f"Generating {num_records} records...")
    data = []
    for i in range(num_records):
        measurement = generate_measurement()
        data.append(measurement)
    
    # Save to CSV
    rows_added = append_to_csv(output_file, data)
    
    # Summary
    total_rows = get_row_count(output_file)
    file_status = "Updated existing file" if file_exists(output_file) else "Created new file"
    
    print(f"\n[OK] {file_status}: {output_file}")
    print(f"[OK] Added {rows_added} new records")
    print(f"[OK] Total records in file: {total_rows}")
    
    return rows_added
