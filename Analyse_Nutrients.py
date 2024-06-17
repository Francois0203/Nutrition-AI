import os, sys
import pandas

# Import custom libraries
import Dataframe_Functions as DF
import File_Handling as FH

# Create nutrient dataframe
def create_nutrient_df(data_location):
    # Variables
    variables = ["Category", "Description", "Carbohydrate", "Cholesterol", "Choline", "Fiber", "Kilocalories", "Protein", "Sugar Total", "Water", "Monosaturated Fat", "Polysaturated Fat", "Saturated Fat", "Total Lipid"]

    # Create dataframe containing unfiltered data from csv file
    df_raw = DF.csv_to_dataframe(os.path.join(data_location, 'food_cleaned.csv'), delim = ";")

    # Extract variables that are important and drop rest
    df = DF.create_subset(df = df_raw, vars = variables)

    # Save subset dataframe to a CSV file
    if os.path.isfile(os.path.join(data_location, 'food_cleaned_subset.csv')):
        print(os.path.join(data_location, 'food_cleaned_subset.csv'), " already exists.")
    else:
        df.to_csv(os.path.join(data_location, 'food_cleaned_subset.csv'), sep = ',')
        print(os.path.join(data_location, 'food_cleaned_subset.csv'), " has successfully been created and saved.") 

    return df

def __main__():
    # Create dataframe
    df = create_nutrient_df(os.path.join(os.getcwd(), "Resources", "Data"))

if __name__ == '__main__':
    __main__()