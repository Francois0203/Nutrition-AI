import os, sys, random
import pandas as pd, numpy as np, tabulate as tb
from pulp import *

# Import custom libraries
import Dataframe_Functions as DF, File_Handling as FH, User_Calculations as UC

# Global variables
MEAL_DF = DF.csv_to_dataframe(os.path.join(os.getcwd(), "nutrition-backend", "Resources", "Data", "all_diets.csv"), ',')

def process_meal_calories(file_path):
    df = DF.csv_to_dataframe(file_path, ',')

    # Caloric values per gram
    PROTEIN_CALORIES_PER_GRAM = 4
    FAT_CALORIES_PER_GRAM = 9
    CARB_CALORIES_PER_GRAM = 4

    # Calculate calories per meal
    df["Calories"] = df["Protein(g)"]*PROTEIN_CALORIES_PER_GRAM + df["Carbs(g)"]*FAT_CALORIES_PER_GRAM + df["Fat(g)"]*CARB_CALORIES_PER_GRAM
    df.to_csv(file_path, index = False)  # index = False to avoid adding an index colum

def optimise_meals(goal, diet_type, num_meals, optimal_protein, optimal_carbs, optimal_fats):
    global MEAL_DF

    # Filter by diet type (if specified)
    if diet_type.lower() != "any":
        MEAL_DF = MEAL_DF[MEAL_DF["Diet_type"].str.lower() == diet_type.lower()]

    # Calculate macro ranges for each meal 
    macro_ranges = {
        "Protein(g)": (optimal_protein / num_meals * 0.8, optimal_protein / num_meals * 1.2),  # 20% flexibility
        "Carbs(g)": (optimal_carbs / num_meals * 0.8, optimal_carbs / num_meals * 1.2),
        "Fat(g)": (optimal_fats / num_meals * 0.8, optimal_fats / num_meals * 1.2),
    }

    # Filter meals that fit within macro ranges
    filtered_df = MEAL_DF[
        (MEAL_DF["Protein(g)"] >= macro_ranges["Protein(g)"][0]) & (MEAL_DF["Protein(g)"] <= macro_ranges["Protein(g)"][1]) &
        (MEAL_DF["Carbs(g)"] >= macro_ranges["Carbs(g)"][0]) & (MEAL_DF["Carbs(g)"] <= macro_ranges["Carbs(g)"][1]) &
        (MEAL_DF["Fat(g)"] >= macro_ranges["Fat(g)"][0]) & (MEAL_DF["Fat(g)"] <= macro_ranges["Fat(g)"][1])
    ]

    # Prioritize meals based on goal
    if goal.lower() == "lose_weight":
        filtered_df = filtered_df.sort_values("Calories", ascending = True)
    elif goal.lower() in ["gain_weight", "gain_lean_muscle"]:
        filtered_df = filtered_df.sort_values("Calories", ascending = False)

    # Sample meals (or all if less than requested amount are found)
    recommended_meals = filtered_df.sample(n = min(num_meals, len(filtered_df))).to_dict(orient = "records")

    return recommended_meals

def format_meal_recommendations(meal_list):    
    if not meal_list:  # Check if list is empty
        print("No suitable meal recommendations found.")
        return
    
    # Print header
    print("{:<10} {:<35} {:<10} {:<10} {:<10} {:<10}".format(
        "Diet", "Recipe", "Protein", "Carbs", "Fat", "Calories"
    ))
    print("-" * 85)  # Separator

    # Print meal details
    for meal in meal_list:
        print("{:<10} {:<35} {:<10.1f} {:<10.1f} {:<10.1f} {:<10.1f}".format(
            meal['Diet_type'], meal['Recipe_name'], meal['Protein(g)'], meal['Carbs(g)'], meal['Fat(g)'], meal['Calories']
        ))

def __main__():
    data = [22, 1, 85, 173, 5, 67, 103]
    meals = optimise_meals("lose_weight", "any", UC.calculate_optimal_macros(data[2], 55, data[4], UC.calculate_maintenance_calories(22, 87, 185, 1, UC.calculate_exercise_level(4)), "gain lean muscle"), 5)
    print(UC.calculate_maintenance_calories(22, 85, 185, 1, UC.calculate_exercise_level(5)))
    print(UC.calculate_optimal_macros(data[2], 55, data[4], UC.calculate_maintenance_calories(22, 87, 185, 1, UC.calculate_exercise_level(4)), "lose_weight"))
    format_meal_recommendations(meals)

if __name__ == '__main__':
    __main__()