import os, csv, random
import numpy as np, matplotlib.pyplot as plt, pandas as pd
from scipy.stats import norm, truncnorm

def generate_data(n):
    data = []
    np.random.seed(42)

    for _ in range(n):
        # ==================== Age, Gender ====================
        age = np.random.randint(18, 80)
        gender = np.random.choice([0, 1])

        # ==================== Weight, Height ====================
        weight = np.where(gender == 0,
                np.random.normal(70, 15),  # Female
                np.random.normal(85, 20))  # Male
        
        height = np.where(gender == 0,
                np.random.normal(165, 10),  # Female
                np.random.normal(175, 10))  # Male
        
        # ==================== Waist, Hip, Exercise Per Week ====================
        waist_circumference = weight / height * 45 + np.random.normal(0, 5)
        hip_circumference = weight / height * 50 + np.random.normal(0, 5)
        exercise = np.random.choice([0, 1, 2, 3, 4, 5, 6, 7])

        # ==================== Body Fat %, Muscle % ====================
        body_fat = 0.1 * weight + 0.5 * exercise - 0.2 * age + np.where(gender == 0, 5, 10) + np.random.normal(0, 2)
        muscle = 0.3 * weight + 0.2 * exercise + 0.1 * height - 0.2 * age + np.random.normal(0, 3)

        data.append([age, gender, weight, height, muscle, body_fat, exercise, waist_circumference, hip_circumference])

    return data

def write_to_csv(data):
        # Write data to CSV
    with open("Resources/Data/fit_data.csv", mode = 'w', newline = '') as file:
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
    num_entries = 20000
    data_1 = generate_data(num_entries)

    write_to_csv(data_1)

if __name__ == "__main__":
    __main__()