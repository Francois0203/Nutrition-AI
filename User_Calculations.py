import os, sys, pandas as pd, numpy as np

# Import custom libraries
import Dataframe_Functions as DF, File_Handling as FH

# Calculate body mass index and classify accordingly
def calculate_bmi(weight, height):
    height = height / 100 # Convert height from cm to m
    bmi = weight / (height ** 2) # Calculate bmi
    classification = ""

    if bmi < 18.5: classification = "Underweight"
    elif 18.5 <= bmi < 25: classification = "Normal Weight"
    elif 25 <= bmi < 30: classification = "Overweight"
    else: classification = "Obese"

    return bmi, classification

# Calculate body adiposity index and classify accordingly
def calculate_bai(hip_circumference, height):
    height = height / 100
    bai = (hip_circumference / (height ** 1.5)) - 18
    classification = ""

    if bai <= 20: classification = "Underweight"
    elif 20 < bai <= 25: classification = "Normal Weight"
    elif 25 < bai <= 30: classification = "Overweight"
    else: classification = "Obese"

    return bai, classification

# Calculate waist-to-hip ratio and classify accordingly
def calculate_whr(gender, waist, hip):
    whr = waist / hip
    classification = ""

    if gender == 'M':
        if whr <= 0.95: classification = "Normal Weight"
        elif 0.95 < whr <= 1: classification = "Overweight"
        else: classification = "Obese"
    elif gender == 'F':
        if whr <= 0.8: classification = "Normal Weight"
        elif 0.8 < whr <= 0.84: classification = "Overweight"
        else: classification = "Obese"

    return whr, classification

def calculate_exercise_level(exercise_level):
    if (exercise_level == 0) or (exercise_level == 1) or (exercise_level == 2) or (exercise_level == 3):
        category = "sedentary"
    elif (exercise_level == 4) or (exercise_level == 5):
        category = "lightly active"
    elif (exercise_level == 6) or (exercise_level == 7):
        category = "moderately active"
    elif (exercise_level == 8) or (exercise_level == 9):
        category = "very active"
    elif (exercise_level == 10):
        "extra active"
    else:
        raise ValueError("Invalid exercise level. Please enter a number between 0 and 10. ")

    return category

# Calculate calories burned during a day with a certain exercise level
def calculate_maintenance_calories(age, weight, height, gender, exercise_category):
    if gender == 1:
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    elif gender == 0:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    else:
        raise ValueError("Invalid gender. Please enter 'male' or 'female'.")

    # Activity Level Multipliers
    activity_multipliers = {
        "sedentary": 1.2,
        "lightly active": 1.375,
        "moderately active": 1.55,
        "very active": 1.725,
        "extra active": 1.9,
    }

    # Calculate Total Daily Energy Expenditure (TDEE)
    tdee = bmr * activity_multipliers[exercise_category.lower()] # Mifflin-St. Jeor Equation

    return tdee

def __main__():
    df = DF.csv_to_dataframe(os.path.join(os.getcwd(), "Resources", "Data", 'fitness.csv'), ",") # Create dataframe

    data = pd.DataFrame([[22, 1, 87, 185, 4, 85, 103]], columns = df.drop(["Body Fat(%)", "Muscle(%)", "Daily Average Calorie Intake", "Daily Average Protein Intake(g)", "Daily Average Fat Intake(g)" , "Daily Average Carb Intake(g)", "Daily Average Sugar Intake(g)"], axis = 1).columns) # Francois
    
    # Predict maintenance calories
    main_cals = calculate_maintenance_calories(22, 87, 185, 1, calculate_exercise_level(4))
    print("Maintenance calories: ", main_cals)

if __name__ == '__main__':
    __main__()