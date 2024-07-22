import os, sys
import Dataframe_Functions as DF, File_Handling as FH, User_Calculations as UC, Analyse_Nutrients as AN, Analyse_User_Model as AUM

def __main__():
    # Variables
    # name = input("Please enter your name and surname: ")
    # age = int(input("Please enter your age: "))
    # gender = int(input("Please enter the number that represents your gender (0 = Female, 1 = Male): "))
    # waist_circumference = int(input("Please enter your waist circumference (cm): "))
    # hip_circumference = int(input("Please enter your hip circumference (cm): "))
    # weight = int(input("Please enter your weight (kg): "))
    # height = int(input("Please enter your height (cm): "))
    # exercise_per_week = int(input("How many times do you exercise on a scale of 0 to 10?: "))
    # goal = input("What would you like to achieve? ") # lose weight, gain weight, gain lean muscle, maintain weight
    # diet_type = input("What are your dietary preferences? ") # any, vegan, paleo, keto, mediterranean, dash

    name = "Francois Meiring"
    age = 22
    gender = 1
    waist_circumference = 87
    hip_circumference = 103
    weight = 85
    height = 185
    exercise_per_week = 7
    goal = "gain lean muscle"
    diet_type = "any" 

    # Input validation


    # User calculations
    bmi = UC.calculate_bmi(weight, height)
    bai = UC.calculate_bai(hip_circumference, height)
    whr = UC.calculate_whr(gender, waist_circumference, hip_circumference)
    #fat_percentage, muscle_percentage = AUM.predict_composition()
    fat_percentage, muscle_percentage = 20, 40
    exercise_category = UC.calculate_exercise_level(exercise_per_week)
    main_cals = UC.calculate_maintenance_calories(age, weight, height, gender, exercise_category)
    optimal_macros = UC.calculate_optimal_macros(weight, muscle_percentage, exercise_per_week, main_cals, goal)

    # Calculate recommended meals for the day
    meal_df = DF.csv_to_dataframe(os.path.join(os.getcwd(), "Resources", "Data", "all_diets.csv"), ',')
    meals = AN.optimise_meals(meal_df, goal, diet_type, optimal_macros, 2)

    # Save user info to csv file
    

    # Show output
    print("To maintain your current weight you need to consume ", main_cals, " calories")
    print("Your recommended daily macronutrient intake: ", optimal_macros)
    AN.format_meal_recommendations(meals)

if __name__ == '__main__':
    __main__()