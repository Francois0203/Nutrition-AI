import os, csv, random
import numpy as np
from scipy.stats import norm, truncnorm

def generate_data(num_entries):
    data = []
    for _ in range(num_entries):
        age = random.randint(18, 80)  # Age range
        gender = random.randint(0, 1)  # 0 for female, 1 for male
        weight = random.randint(40, 80)  # Weight range in kg
        height = random.randint(120, 200)  # Height range in cm
        muscle = random.randint(25, 55)  # Muscle mass % range
        body_fat = random.randint(0, 50)  # Body fat % range
        calories = random.randint(1000, 3500)  # Calorie intake range
        protein = random.randint(0, 200)  # Protein intake range in g
        fat = random.randint(0, 120)  # Fat intake range in g
        carbs = random.randint(0, 400)  # Carb intake range in g
        sugar = random.randint(0, 80)  # Sugar intake range in g
        exercise = random.randint(0, 7)  # Exercise days per week
        waist = random.randint(40, 120)  # Waist circumference range in cm
        hips = random.randint(50, 130)  # Hip circumference range in cm

        data.append([age, gender, weight, height, muscle, body_fat, calories, protein, fat, carbs, sugar, exercise, waist, hips])
    return data

def generate_data_distributions(num_entries):
    data = []
    for _ in range(num_entries):
        # Age: Bimodal distribution (younger and older fitness enthusiasts)
        if random.random() < 0.7:
            age = round(np.random.normal(28, 5))
        else:
            age = round(np.random.normal(55, 10))
        age = max(18, min(80, age))

        # Biological Sex (0 for female, 1 for male)
        biological_sex = random.randint(0, 1)

        # Weight (kg) and Height (cm): Adjusted based on biological sex
        if biological_sex == 0: # Female
            weight = round(np.random.normal(65, 12))
            height = round(np.random.normal(163, 7))
        else:                   # Male
            weight = round(np.random.normal(80, 15))
            height = round(np.random.normal(175, 8))
        weight = max(40, min(120, weight))
        height = max(140, min(200, height))

        # Muscle Mass (%) and Body Fat (%)
        muscle = round(truncnorm.rvs(-2, 2, loc=35, scale=8))
        muscle = max(20, min(50, muscle))
        body_fat = round(55 - muscle + np.random.normal(0, 3))
        body_fat = max(5, min(40, body_fat))
        
        # Exercise per week: Skewed towards lower values
        exercise = round(np.random.gamma(2, 1))
        exercise = max(0, min(7, exercise))
        
        # Daily Calorie Intake: Based on activity level, estimated from exercise
        base_calories = 2000 if biological_sex == 0 else 2500
        calorie_multiplier = 1 + (exercise / 7) * 0.2 # 20% increase per exercise day
        calories = round(base_calories * calorie_multiplier + np.random.normal(0, 200))

        # Macronutrient Intake (protein, fat, carbs):
        # These are rough estimates and can be fine-tuned based on specific goals
        protein = round(weight * 1.2 + np.random.normal(0, 20)) # 1.2g protein per kg body weight
        fat = round(calories * 0.3 / 9 + np.random.normal(0, 10)) # 30% of calories from fat
        carbs = round((calories - protein * 4 - fat * 9) / 4 + np.random.normal(0, 30))

        # Sugar Intake: A portion of total carb intake
        sugar = round(carbs * 0.2 + np.random.normal(0, 5))

        # Waist and Hip Circumference: Rough estimates, highly variable in reality
        if biological_sex == 0:  # Female
            waist = round(weight * 0.4 + np.random.normal(0, 5))
            hips = round(weight * 0.55 + np.random.normal(0, 8))
        else:                   # Male
            waist = round(weight * 0.45 + np.random.normal(0, 6))
            hips = round(weight * 0.5 + np.random.normal(0, 6))

        data.append([age, biological_sex, weight, height, muscle, body_fat, calories, protein, fat, carbs, sugar, exercise, waist, hips])
    return data

# Generate data entries (or adjust this number as needed)
num_entries = 10000
data_1 = generate_data(num_entries)
data_2 = generate_data_distributions(num_entries)

# Write data to CSV
with open("Resources/Data/fitness_data.csv", mode = 'w', newline = '') as file:
    writer = csv.writer(file)
    writer.writerow([
        "Age",
        "Gender",
        "Weight(Kg)",
        "Height(cm)",
        "Muscle(%)",
        "Body Fat(%)",
        "Daily Average Calorie Intake",
        "Daily Average Protein Intake(g)",
        "Daily Average Fat Intake(g)",
        "Daily Average Carb Intake(g)",
        "Daily Average Sugar Intake(g)",
        "Exercise per week",
        "Waist circumference (cm)",
        "Hip circumference (cm)",
    ])

    for row in data_1:
        writer.writerow(row)