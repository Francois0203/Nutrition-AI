import os, csv, random
import numpy as np, matplotlib.pyplot as plt, pandas as pd, tabulate as tb
from scipy.stats import norm, truncnorm
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

def __main__():
    # Generate data entries 
    num_entries = 20000
    data_2 = generate_data_distributions(num_entries)

    #create_nutrient_file(os.path.join(os.getcwd(), "Resources", "Data"), "food.csv")
    #df = DF.csv_to_dataframe(os.path.join(os.getcwd(), "Resources", "Data", "food_subset.csv"), ',')

    #extract_healthy_items(df, os.path.join(os.getcwd(), "Resources", "Data"))
    #healthy_df = DF.csv_to_dataframe(os.path.join(os.getcwd(), "Resources", "Data", "healthy_food.csv"), ',')

    #food_items = generate_food_items(healthy_df, 100, 2000, 70, 250)
    #display_food_items(food_items, healthy_df)

if __name__ == '__main__':
    __main__()