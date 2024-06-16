import os, sys
import pandas

# Set working directory
sys.path.append(os.getcwd())

# Import custom libraries
import Dataframe_Functions as DF

def __main__():
    # Variables
    script_directory = DF.get_working_directory() # Get working directory
    data_location = os.path.join(os.getcwd(), "Resources", "Data") # Get folder where data is stored and found
    variables = ["Category", "Description", "Carbohydrate", "Cholesterol", "Choline", "Fiber", "Kilocalories", "Protein", "Sugar Total", "Water", "Monosaturated Fat", "Polysaturated Fat", "Saturated Fat", "Total Lipid"]

    # Change data directory
    change = 0

    while (change != '1' or change != '2' or change != 'q'):
        change = input("Do you want to change the directory where your data is located?:\n1. Yes\n2. No\nYour choice (1 or 2): ")

        if change == '1':
            data_location = DF.get_directory()
            print("\nYour data will be stored at: ", data_location)
            break
        elif change == '2':
            print("\nYour data will then be located at: ", data_location)
            break
        elif change == 'q':
            break
        else:
            print("\nInvalid choice!\n")

    # Create dataframe from csv file
    df_raw = DF.csv_to_dataframe(os.path.join(data_location, 'food_cleaned.csv'), delim = ";")
    df = DF.create_subset(df = df_raw, vars = variables)
    print(df.head())

if __name__ == '__main__':
    __main__()