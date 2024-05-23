import os, sys
import pandas as pd

# Set working directory
sys.path.append(os.getcwd())

# Import custom libraries
import Dataframe_Functions as DF

# Global variables
DATA_LOCATION = os.path.join(os.getcwd(), "Resources", "Data")

def __main__():
    # Variables
    global DATA_LOCATION

    variables = ["Category", "Description", "Carbohydrate", "Cholesterol", "Choline", "Fiber", "Kilocalories", "Protein", "Sugar Total", "Water", "Monosaturated Fat", "Polysaturated Fat", "Saturated Fat", "Total Lipid"]

    # Create a dataframe from the food.csv file
    df = pd.read_csv(os.path.join(DATA_LOCATION, 'food.csv'), 
                        sep = ';;', # Specify delimiter as ';;'
                        engine = 'python', 
                        header = None,
                        quotechar = '"') 

    # Remove double quotes from all columns
    for col in df.columns:
        df[col] = df[col].astype(str).str.replace('"', '', regex = False)

    # Format the dataframe in the correct form
    df = df[0].str.split(',', expand = True)
    df.dropna(axis = 1, inplace = True) # Drop columns with NaN values
    new_header = df.iloc[0]
    df = df[1:]
    df.columns = new_header
    
    # Display the dataframe and its details after formatting correctly
    print("\nCorrect Form:\n")
    print(df.head())
    print(f"\nColumns: {df.shape[1]}, Rows: {df.shape[0]}, Variables: \n")
    print(new_header)

    # Save the dataframe to a csv file
    df.to_csv(os.path.join(os.getcwd(), 'Resources', 'Data', 'food_cleaned.csv'), index = False)
    print("File saved to: ", os.path.join(os.getcwd(), 'Resources', 'Data', 'food_cleaned.csv'))

if __name__ == '__main__':
    __main__()