import os, sys
import pandas as pd, numpy as np
from pulp import *

# Import custom libraries
import Dataframe_Functions as DF, File_Handling as FH

# Create nutrient dataframe
def create_nutrient_df(data_location):
    # Variables
    variables = ["Category", "Description", "Carbohydrate", "Cholesterol", "Choline", "Fiber", "Kilocalories", "Protein", "Sugar Total", "Water", "Monosaturated Fat", "Polysaturated Fat", "Saturated Fat", "Total Lipid"]

    # Create dataframe containing unfiltered data from csv file
    df_raw = DF.csv_to_dataframe(os.path.join(data_location, 'food_cleaned.csv'), delim = ";")

    # Extract variables that are important and drop rest
    df = DF.create_subset(df = df_raw, vars = variables)

    FH.dataframe_to_csv(df, data_location, "food_cleaned_subset")

# Create a new dataset only containing the healthiest items with the least amount of saturated fat, cholesterol, and sugar
def extract_healthy_items(df, data_location):
    # Sort and drop duplicates as before
    df_sorted = df.sort_values(['Category', 'Saturated Fat', 'Cholesterol', 'Sugar Total'])
    df_final = df_sorted.drop_duplicates(subset = ['Category'], keep = 'first')

    FH.dataframe_to_csv(df_final, data_location, "healthy_food")

def optimize_macros(df, goal, target_calories, target_protein, target_fat, target_carbs):
    # Define target_macros dictionary
    target_macros = {
        "Kilocalories": target_calories,
        "Protein": target_protein,
        "Total Lipid": target_fat,
        "Carbohydrate": target_carbs,
    }

    # Filtering based on goal
    if goal == "weight loss":
        df_filtered = df[df["Kilocalories"] < target_calories] 
        df_filtered = df_filtered.sort_values(by = ["Fiber", "Protein"], ascending = [False, False]) 
    elif goal == "weight gain":
        df_filtered = df[df["Kilocalories"] > target_calories]
        df_filtered = df_filtered.sort_values(by = ["Kilocalories"], ascending = [False])
    elif goal == "lean muscle gain":
        df_filtered = df.sort_values(by=["Fiber", "Protein"], ascending=[False, False])
    elif goal == "muscle and weight gain":
        df_filtered = df[df["Kilocalories"] > target_calories]
        df_filtered = df_filtered.sort_values(by = ["Kilocalories", "Protein"], ascending= [False, False])
    elif goal == "maintain weight":
        df_filtered = df[df["Kilocalories"] == target_calories]
    else:
        return pd.DataFrame()  # Return an empty DataFrame if goal is invalid

    # Combining foods to reach targets
    selected_foods = []
    current_macros = {"Kilocalories": 0, "Protein": 0, "Total Lipid": 0, "Carbohydrate": 0}
    
    for index, row in df_filtered.iterrows():
        new_macros = {
            "Kilocalories": current_macros["Kilocalories"] + row["Kilocalories"],
            "Protein": current_macros["Protein"] + row["Protein"],
            "Total Lipid": current_macros["Total Lipid"] + row["Total Lipid"],
            "Carbohydrate": current_macros["Carbohydrate"] + row["Carbohydrate"],
        }
        
        # Check if the new food gets us closer to the target. If overshoot, skip the food.
        if all(new_macros[macro] <= target_macros[macro] for macro in current_macros):
            selected_foods.append(row)
            current_macros = new_macros

            # If targets are met, exit the loop
            if all(current_macros[macro] >= target_macros[macro] for macro in current_macros):
                break

    return pd.DataFrame(selected_foods)

def __main__():
    create_nutrient_df(os.path.join(os.getcwd(), "Resources", "Data"))
    df = DF.csv_to_dataframe(os.path.join(os.getcwd(), "Resources", "Data", "food_cleaned_subset"), ',')
    extract_healthy_items(df, os.path.join(os.getcwd(), "Resources", "Data"))
    healthy_df = DF.csv_to_dataframe(os.path.join(os.getcwd(), "Resources", "Data", "healthy_food.csv"), ',')

if __name__ == '__main__':
    __main__()