import os, sys, random
import pandas as pd, numpy as np, tabulate as tb
from pulp import *

# Import custom libraries
import Dataframe_Functions as DF, File_Handling as FH, User_Calculations as UC

# Create nutrient dataframe
def create_nutrient_file(data_location, name):
    # Variables
    variables = ["Category", "Description", "Carbohydrate", "Cholesterol", "Choline", "Fiber", "Kilocalories", "Protein", "Sugar Total", "Water", "Monosaturated Fat", "Polysaturated Fat", "Saturated Fat", "Total Lipid", "1st Household Weight", "1st Household Weight Description"]

    # Create dataframe containing unfiltered data from csv file
    df_raw = DF.csv_to_dataframe(os.path.join(data_location, name), delim = ";")

    # Extract variables that are important and drop rest
    df = DF.create_subset(df = df_raw, vars = variables)

    FH.dataframe_to_csv(df, data_location, "food_subset")

# Create a new dataset only containing the healthiest items with the least amount of saturated fat, cholesterol, and sugar
def extract_healthy_items(df, data_location):
    # Sort and drop duplicates as before
    df_sorted = df.sort_values(['Category', 'Saturated Fat', 'Cholesterol', 'Sugar Total'])
    df_final = df_sorted.drop_duplicates(subset = ['Category'], keep = 'first')

    FH.dataframe_to_csv(df_final, data_location, "healthy_food")

def generate_food_items(food_data, protein_goal, calorie_goal, fat_goal, carb_goal, num_meals = 3):
    # Filter out unsuitable items (too high in a single nutrient, extremely small portions)
    filtered_data = food_data[
        (food_data["Protein"] < protein_goal * 0.7)
        & (food_data["Kilocalories"] < calorie_goal * 0.7)
        & (food_data["Total Lipid"] < fat_goal * 0.7)
        & (food_data["Carbohydrate"] < carb_goal * 0.7)
        & (food_data["1st Household Weight"] > 10)  # Ensure a minimum serving size
    ].copy()  # Create a copy to avoid modifying the original DataFrame

    # Add a new column for portion size in grams
    filtered_data["Portion_Grams"] = filtered_data["1st Household Weight"] * 100

    meals = []
    for _ in range(num_meals):
        meal = {}
        remaining_nutrients = {
            "Protein": protein_goal,
            "Kilocalories": calorie_goal,
            "Total Lipid": fat_goal,
            "Carbohydrate": carb_goal,
        }

        while any(val > 0 for val in remaining_nutrients.values()):
            # Prioritize items that contribute most to remaining nutrients
            filtered_data["Priority"] = filtered_data.apply(
                lambda row: sum(
                    remaining_nutrients[nutrient] / max(1, row[nutrient])  # Avoid division by zero
                    for nutrient in remaining_nutrients
                ),
                axis=1,
            )
            food_item = filtered_data.nlargest(1, "Priority").iloc[0]

            # Adjust quantity based on remaining nutrients, portion size, and food item's nutritional content
            max_quantity = min(
                (remaining_nutrients[nutrient] / max(1, food_item[nutrient]))  # Avoid division by zero
                * food_item["Portion_Grams"]
                for nutrient in remaining_nutrients
            )

            # Ensure we add at least one serving and round to nearest serving size
            quantity = max(food_item["Portion_Grams"], max_quantity)
            servings = round(quantity / food_item["Portion_Grams"])

            # Add the food item and quantity to the meal
            meal[food_item["Description"]] = servings

            # Update remaining nutrients
            for nutrient in remaining_nutrients:
                remaining_nutrients[nutrient] -= food_item[nutrient] * servings

            # Remove the used item to avoid repetition
            filtered_data = filtered_data.drop(food_item.name)

        meals.append(meal)
    return meals

def display_food_items(meals, food_data):
    for i, meal in enumerate(meals, start = 1):
        print(f"\nMeal {i}:")
        meal_data = []

        total_nutrients = {
            "Protein": 0,
            "Kilocalories": 0,
            "Total Lipid": 0,
            "Carbohydrate": 0,
        }

        for food, quantity in meal.items():
            food_info = food_data[food_data["Description"] == food].iloc[0]  # Get info from original data

            meal_data.append([
                food,
                f"{quantity:.2f} {food_info['1st Household Weight Description']}",
                f"{food_info['Kilocalories'] * quantity:.0f} kcal",
                f"{food_info['Protein'] * quantity:.1f} g",
                f"{food_info['Total Lipid'] * quantity:.1f} g",
                f"{food_info['Carbohydrate'] * quantity:.1f} g",
            ])

            # Accumulate total nutrients for the meal
            for nutrient in total_nutrients:
                total_nutrients[nutrient] += food_info[nutrient] * quantity

        # Display the meal table
        print(tb.tabulate(meal_data, headers = ["Food", "Quantity", "Calories", "Protein", "Fat", "Carbs"]))

        # Display total meal nutrients
        print("\nTotal Nutrients:")
        print(f"  Calories: {total_nutrients['Kilocalories']:.0f} kcal")
        print(f"  Protein: {total_nutrients['Protein']:.1f} g")
        print(f"  Fat: {total_nutrients['Total Lipid']:.1f} g")
        print(f"  Carbs: {total_nutrients['Carbohydrate']:.1f} g")

def process_meal_calories(file_path):
    df = DF.csv_to_dataframe(file_path, ',')

    # Caloric values per gram
    PROTEIN_CALORIES_PER_GRAM = 4
    FAT_CALORIES_PER_GRAM = 9
    CARB_CALORIES_PER_GRAM = 4

    # Calculate calories per meal
    df["Calories"] = df["Protein(g)"]*PROTEIN_CALORIES_PER_GRAM + df["Carbs(g)"]*FAT_CALORIES_PER_GRAM + df["Fat(g)"]*CARB_CALORIES_PER_GRAM
    df.to_csv(file_path, index = False)  # index = False to avoid adding an index colum

def optimise_meals(df, goal, diet_type, macros, num_meals):
    # Filter by diet type (if specified)
    if diet_type.lower() != "any":
        df = df[df["Diet_type"].str.lower() == diet_type.lower()]

    # Calculate macro ranges for each meal 
    macro_ranges = {
        "Protein(g)": (macros["protein grams"] / num_meals * 0.8, macros["protein grams"] / num_meals * 1.2),  # 20% flexibility
        "Carbs(g)": (macros["carb grams"] / num_meals * 0.8, macros["carb grams"] / num_meals * 1.2),
        "Fat(g)": (macros["fat grams"] / num_meals * 0.8, macros["fat grams"] / num_meals * 1.2),
    }

    # Filter meals that fit within macro ranges
    filtered_df = df[
        (df["Protein(g)"] >= macro_ranges["Protein(g)"][0]) & (df["Protein(g)"] <= macro_ranges["Protein(g)"][1]) &
        (df["Carbs(g)"] >= macro_ranges["Carbs(g)"][0]) & (df["Carbs(g)"] <= macro_ranges["Carbs(g)"][1]) &
        (df["Fat(g)"] >= macro_ranges["Fat(g)"][0]) & (df["Fat(g)"] <= macro_ranges["Fat(g)"][1])
    ]

    # Prioritize meals based on goal
    if goal.lower() == "lose weight":
        filtered_df = filtered_df.sort_values("Calories", ascending = True)
    elif goal.lower() in ["gain weight", "gain lean muscle"]:
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
    #create_nutrient_file(os.path.join(os.getcwd(), "Resources", "Data"), "food.csv")
    #df = DF.csv_to_dataframe(os.path.join(os.getcwd(), "Resources", "Data", "food_subset.csv"), ',')

    #extract_healthy_items(df, os.path.join(os.getcwd(), "Resources", "Data"))
    #healthy_df = DF.csv_to_dataframe(os.path.join(os.getcwd(), "Resources", "Data", "healthy_food.csv"), ',')

    #food_items = generate_food_items(healthy_df, 100, 2000, 70, 250)
    #display_food_items(food_items, healthy_df)

    meal_df = DF.csv_to_dataframe(os.path.join(os.getcwd(), "Resources", "Data", "all_diets.csv"), ',')
    data = [22, 1, 85, 173, 5, 67, 103]
    meals = optimise_meals(meal_df, "lose weight", "any", UC.calculate_optimal_macros(data[2], 55, data[4], UC.calculate_maintenance_calories(22, 87, 185, 1, UC.calculate_exercise_level(4)), "gain lean muscle"), 5)
    print(UC.calculate_maintenance_calories(22, 85, 185, 1, UC.calculate_exercise_level(5)))
    print(UC.calculate_optimal_macros(data[2], 55, data[4], UC.calculate_maintenance_calories(22, 87, 185, 1, UC.calculate_exercise_level(4)), "lose weight"))
    format_meal_recommendations(meals)

if __name__ == '__main__':
    __main__()