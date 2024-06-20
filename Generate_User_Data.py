import csv, random

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

# Generate data entries (or adjust this number as needed)
num_entries = 10000
data = generate_data(num_entries)

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

    for row in data:
        writer.writerow(row)