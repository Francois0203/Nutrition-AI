import os, sys
import pandas as pd, numpy as np, excel_solver as solver

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

    return df

def optimise_macros(goal):
    if goal == "weight loss": # High fiber and less calories than recommended amount
        pass
    elif goal == "weight gain": # More calories in carbohydrates, protein and fat
        pass
    elif goal == "lean muscle gain":  # Higher fiber and protein
        pass
    elif goal == "muscle and weight gain": # Higher calories and protein
        pass
    elif goal == "maintain weight": # Keep calories same as recommended amount
        pass

def __main__():
    # Create dataframe
    df = create_nutrient_df(os.path.join(os.getcwd(), "Resources", "Data"))

if __name__ == '__main__':
    __main__()