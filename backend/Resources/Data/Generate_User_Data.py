import csv, os
import numpy as np

def generate_data(n):
    data = []
    np.random.seed(42)

    for _ in range(n):
        # ==================== Age, Gender ====================
        age = np.random.randint(18, 80)
        gender = np.random.choice([0, 1])  # 0: Female, 1: Male

        # ==================== Weight, Height ====================
        if gender == 0:  # Female
            weight = np.random.normal(68, 12)  
            height = np.random.normal(162, 8)
        else:  # Male
            weight = np.random.normal(80, 15)
            height = np.random.normal(175, 10)
        
        # ==================== Waist, Hip, Exercise Per Week ====================
        waist_circumference = weight / height * 42 + np.random.normal(0, 3)  # Adjusted for more realistic waist-to-height ratio
        hip_circumference = waist_circumference + np.random.normal(6, 2)  # Average hip circumference larger than waist
        exercise = np.random.choice([0, 1, 2, 3, 4, 5, 6, 7])  # Weekly exercise days

        # ==================== Body Fat %, Muscle % ====================
        if gender == 0:  # Female
            # Body fat percentage typically higher in women; muscle mass lower
            body_fat = (
                0.25 * weight - 0.15 * exercise - 0.2 * age + 30 + np.random.normal(0, 1.5)
            )  # Females naturally have a higher body fat
            muscle = (
                0.2 * weight + 0.2 * exercise + 0.1 * height - 0.1 * age + np.random.normal(0, 2)
            )  # Muscle mass influenced by exercise and age in females
        else:  # Male
            body_fat = (
                0.2 * weight - 0.2 * exercise - 0.15 * age + 18 + np.random.normal(0, 1.5)
            )  # Males tend to have a lower body fat percentage
            muscle = (
                0.35 * weight + 0.25 * exercise + 0.1 * height - 0.15 * age + np.random.normal(0, 2)
            )  # Higher base muscle mass for men
        
        # Ensure body fat and muscle percentages stay within realistic bounds
        body_fat = max(5, min(body_fat, 50))  # Body fat should be between 5% and 50%
        muscle = max(25, min(muscle, 60))     # Muscle mass should be between 25% and 60%

        # Adjust waist-to-hip ratio for highly muscular individuals
        if muscle > 50:
            waist_circumference -= 2  # Lower waist size for more muscular people
        
        data.append([age, gender, weight, height, muscle, body_fat, exercise, waist_circumference, hip_circumference])

    return data

def write_to_csv(data):
    # Write data to CSV
    with open(os.path.join('backend', 'Resources', 'Data', 'fit_data.csv'), mode='w', newline='') as file:
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
    data = generate_data(num_entries)
    write_to_csv(data)

if __name__ == "__main__":
    __main__()