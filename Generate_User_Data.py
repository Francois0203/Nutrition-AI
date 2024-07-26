import os, csv, random
import numpy as np, matplotlib.pyplot as plt, pandas as pd
from scipy.stats import norm, truncnorm

def generate_data_distributions(num_entries):
    data = []
    for _ in range(num_entries):
        # Age: Bimodal distribution (younger and older fitness enthusiasts)
        if random.random() < 0.6:  # Adjusted probability for younger group
            age = round(np.random.normal(25, 4))  # Slightly younger and less spread
        else:
            age = round(np.random.normal(58, 8))  # Slightly older and less spread
        age = max(18, min(80, age))

        # Biological Sex (0 for female, 1 for male)
        biological_sex = random.randint(0, 1)

        # Body Fat Percentage: More realistic distribution based on age and sex
        if biological_sex == 0:  # Female
            body_fat_mean = 22 + 0.15 * (age - 25)  # Body fat increases with age
            body_fat_std_dev = 6  
        else:  # Male
            body_fat_mean = 12 + 0.1 * (age - 25) 
            body_fat_std_dev = 5  
        body_fat = round(truncnorm.rvs(-2.5, 2.5, loc=body_fat_mean, scale=body_fat_std_dev))
        body_fat = max(5, min(45, body_fat))  # Wider range, but still realistic

        # Weight and Height: Account for wider range of body types
        bmi = np.random.normal(22, 3)  # Wider BMI range for diversity
        height = round(np.random.normal(163 if biological_sex == 0 else 175, 8))  # More height variation
        weight = round(bmi * (height / 100) ** 2)

        # Muscle Mass:  Refined estimate based on age and sex
        if biological_sex == 0:
            muscle = round((100 - body_fat - 15) * (1 - 0.005 * (age - 25)))  # Decreases slightly with age
        else:
            muscle = round((100 - body_fat - 10) * (1 - 0.003 * (age - 25)))

        # Exercise per week: More realistic distribution (most people exercise less)
        exercise = round(np.random.gamma(1.5, 1.5))  # Skewed more towards lower values
        exercise = max(0, min(7, exercise))

        # Daily Calorie Intake: Revised based on updated body composition
        base_calories = 10 * weight + 6.25 * height - 5 * age + 5 if biological_sex == 1 else -161
        activity_factor = 1.2 + 0.2 * exercise  # Stronger influence of exercise on calories

        # Waist and Hip Circumference: Rough estimates, highly variable in reality
        if biological_sex == 0:  # Female
            waist = round(weight * 0.4 + np.random.normal(0, 5))
            hips = round(weight * 0.55 + np.random.normal(0, 8))
        else:                   # Male
            waist = round(weight * 0.45 + np.random.normal(0, 6))
            hips = round(weight * 0.5 + np.random.normal(0, 6))

        data.append([age, biological_sex, weight, height, muscle, body_fat, exercise, waist, hips])
    return data

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
    data_2 = generate_data_distributions(num_entries)

    write_to_csv(data_1)

if __name__ == "__main__":
    __main__()