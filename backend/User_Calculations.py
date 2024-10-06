# Calculate body mass index and classify accordingly
def calculate_bmi(weight, height):
    height = height / 100 # Convert height from cm to m
    bmi = weight / (height ** 2) # Calculate bmi
    classification = ""

    if bmi < 18.5: classification = "Underweight"
    elif 18.5 <= bmi < 25: classification = "Normal Weight"
    elif 25 <= bmi < 30: classification = "Overweight"
    else: classification = "Obese"

    return bmi

# Calculate body adiposity index and classify accordingly
def calculate_bai(hip_circumference, height):
    height = height / 100
    bai = (hip_circumference / (height ** 1.5)) - 18
    classification = ""

    if bai <= 20: classification = "Underweight"
    elif 20 < bai <= 25: classification = "Normal Weight"
    elif 25 < bai <= 30: classification = "Overweight"
    else: classification = "Obese"

    return bai

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

    return whr

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

def calculate_optimal_macros(weight, muscle_percent, exercise_per_week, tdee, goal):
    protein_per_kg = 1.2 + (0.3 * muscle_percent / 100) + (0.05 * exercise_per_week)
    
    if goal.lower() == "lose_weight":
        protein_per_kg += 0.2  # Increase protein for satiety and muscle preservation
        tdee *= 0.85  # Create a calorie deficit (15% reduction)
    elif goal.lower() == "gain_weight":
        tdee *= 1.15  # Create a calorie surplus (15% increase)
    elif goal.lower() == "gain_lean_muscle":
        protein_per_kg += 0.4  # Increase protein for muscle building
        tdee *= 1.05  # Slight calorie surplus (5% increase)
    elif goal.lower() != "maintain_weight":
        raise ValueError("Invalid goal. Please enter 'lose_weight', 'gain_weight', 'gain_lean_muscle', or 'maintain_weight'.")

    protein_grams = protein_per_kg * weight

    # --- Fat ---
    # Adjusted slightly based on goal
    if goal.lower() == "lose_weight":
        fat_calories = 0.20 * tdee  # Lower fat for weight loss
    else:
        fat_calories = 0.25 * tdee  # 25% for other goals
    fat_grams = fat_calories / 9

    # --- Carbohydrates ---
    # Remaining calories after protein and fat
    carb_calories = tdee - (protein_grams * 4) - fat_calories
    carb_grams = carb_calories / 4

    # return {
    #     "protein grams": round(protein_grams),
    #     "carb grams": round(carb_grams),
    #     "fat grams": round(fat_grams),
    #     "total calories": round(tdee)
    # }

    return round(protein_grams), round(carb_grams), round(fat_grams), round(tdee)

def __main__():
    #df = DF.csv_to_dataframe(os.path.join(os.getcwd(), "Resources", "Data", 'fitness.csv'), ",") # Create dataframe

    #data = pd.DataFrame([[22, 1, 87, 185, 4, 85, 103]], columns = df.drop(["Body Fat(%)", "Muscle(%)", "Daily Average Calorie Intake", "Daily Average Protein Intake(g)", "Daily Average Fat Intake(g)" , "Daily Average Carb Intake(g)", "Daily Average Sugar Intake(g)"], axis = 1).columns) # Francois
    data = [22, 1, 87, 185, 4, 85, 103]
    
    # Predict maintenance calories
    main_cals = calculate_maintenance_calories(22, 87, 185, 1, calculate_exercise_level(4))
    print("Maintenance calories: ", main_cals)

    print(calculate_optimal_macros(data[2], 55, data[4], main_cals, "gain_lean_muscle"))

if __name__ == '__main__':
    __main__()