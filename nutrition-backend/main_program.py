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
    waist = 87
    hip = 103
    weight = 85
    height = 185
    exercise_days = 7
    goal = "gain lean muscle"
    diet = "any" 

    bmi = UC.calculate_bmi(weight, height)
    bai = UC.calculate_bai(hip, height)
    whr = UC.calculate_whr(gender, waist, hip)
    body_fat = AUM.predict_body_fat(age, gender, weight, height, exercise_days, hip, waist)
    body_mass = AUM.predict_muscle_mass(age, gender, weight, height, exercise_days, hip, waist)
    exercise_category = UC.calculate_exercise_level(exercise_days)
    main_cals = UC.calculate_maintenance_calories(age, weight, height, gender, exercise_category)
    optimal_macros = UC.calculate_optimal_macros(weight, body_mass, exercise_days, main_cals, goal)
    meals = AN.optimise_meals(goal, diet, optimal_macros, 3)

    print("BMI: ", bmi)
    print("BAI: ", bai)
    print("WHR: ", whr)
    print("Body Fat %: ", body_fat)
    print("Body mass %: ", body_mass)
    print("Exercise Category: ", exercise_category)
    print("Maintenance Calories: ", main_cals)
    print("Optimal Macros: ", optimal_macros)
    print("Meals: ", meals)

if __name__ == '__main__':
    __main__()