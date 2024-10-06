import csv
import numpy as np, pandas as pd
from scipy.stats import norm, truncnorm

def generate_data(n):
    data = []
    np.random.seed(42)

    for _ in range(n):
        # ==================== Age, Gender ====================
        age = np.random.randint(18, 80)
        gender = np.random.choice([0, 1])  # 0 for female, 1 for male

        # ==================== Weight, Height ====================
        weight = np.where(gender == 0,
                np.random.normal(65, 10),  # Average female weight
                np.random.normal(80, 15))  # Average male weight
        
        height = np.where(gender == 0,
                np.random.normal(165, 7),  # Average female height
                np.random.normal(175, 7))  # Average male height
        
        # ==================== Waist, Hip Circumference ====================
        waist_circumference = (weight / height * 40) + np.random.normal(0, 5)
        hip_circumference = (weight / height * 45) + np.random.normal(0, 5)
        
        # ==================== Exercise Per Week ====================
        exercise = np.random.choice([0, 1, 2, 3, 4, 5, 6, 7])

        # ==================== Body Fat % and Muscle % Calculation ====================
        # Body Fat Percentage
        body_fat = (1.20 * weight / ((height / 100) ** 2) + 0.23 * age - 10.8 * gender - 5.4 + 
                    np.random.normal(0, 2))  # Using Boer formula

        # Muscle Mass Percentage (approximated)
        muscle = (0.4 * weight + 0.1 * height - 0.25 * age + 0.15 * exercise + 
                  np.random.normal(0, 3)) / weight * 100  # As a percentage of total weight

        # Clipping values to valid ranges
        body_fat = np.clip(body_fat, 0, 100)  # Ensure body fat % is between 0 and 100
        muscle = np.clip(muscle, 0, 100)  # Ensure muscle % is between 0 and 100

        data.append([age, gender, weight, height, muscle, body_fat, exercise, waist_circumference, hip_circumference])

    return data

def write_to_csv(data):
        # Write data to CSV
    with open("fit_data.csv", mode = 'w', newline = '') as file:
        writer = csv.writer(file)
        writer.writerow([
            "Age",
            "Gender",
            "Weight(Kg)",
            "Height(cm)",
            "Muscle(%)",
            "Body Fat(%)",
            "Exercise per week",
            "Waist circumference (cm)",
            "Hip circumference (cm)",
        ])

        for row in data:
            writer.writerow(row)

def __main__():
    # Generate data entries 
    num_entries = 30000
    data_1 = generate_data(num_entries)

    write_to_csv(data_1)

if __name__ == "__main__":
    __main__()