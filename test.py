import sys, os
import pandas as pd
import csv

# Set working directory
sys.path.append(os.getcwd())

# Import custom libraries
import Dataframe_Functions as DF

# Global variables
DATA_LOCATION = os.path.join(os.getcwd(), "Resources", "Data")

# Remove a specific character from the dataset
def replace_char(data, char_remove, char_replace):
    cleaned_data = []

    for row in data:
        cleaned_row = {}

        for key, value in row.items():
            if isinstance(value, str):  # Check if the value is a string
                cleaned_row[key] = value.replace(char_remove, char_replace)
            else:  # If not a string, keep the original value
                cleaned_row[key] = value

        cleaned_data.append(cleaned_row)

    return cleaned_data

# Add the quotes around each word (string value)
def add_quotes(data):
    modified_data = []

    for row in data:
        modified_row = []

        for value in row.values():
            try:
                float(value)  # Try to convert to a number
                modified_row.append(value)  # No quotes if it's a number
            except ValueError:
                modified_row.append(f'"{value}"')  # Add quotes if it's not a number

        modified_data.append(modified_row)

    return modified_data

def __main__():
    # Variables
    global DATA_LOCATION

    data = []

    # Set data directory
    script_directory = DF.get_working_directory()
    print("Working directory: ", script_directory)

    # Prompt user if they want to change the location where the csv file is found
    print(f"\nCurrent location where data is found: {DATA_LOCATION}")
    change = input("\nDo you want to change the location where your data is found?\n1. Yes\n2. No\nYour choice (1 or 2): ")

    if change == '1':
        # Select new data location
        print("\nSelect the location where the new data is located.\n")
        data_location = DF.get_directory()
    elif change == '2':
        data_location = DATA_LOCATION
        print("\nThe data is found at: ", data_location)
    else:
        print("\nInvalid choice. Exiting...")
        data_location = DATA_LOCATION

    # Read the data from the file using the appropriate encoding.
    try:
        with open(os.path.join(data_location, 'food.csv'), "r", newline = '', encoding = 'utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            data = list(reader)
            data = replace_char(data, '""', '"') # Replace all double quotes "" "" with single quotes " "
            data = replace_char(data, ';;', '') # Replaces ';;' with an empty space
    except FileNotFoundError:
        print(f"Error: File not found at {data_location}")
        return

    #data = add_quotes(data) # Add '"' characters before the start of each word
    print(data[1])

    # Prompt user if they want to change the save location of the formatted file
    print(f"\nCurrent location where data is saved: {DATA_LOCATION}")
    change = input("\nDo you want to change the location where your data should be stored?\n1. Yes\n2. No\nYour choice (1 or 2): ")

    if change == '1':
        # Select new save location
        print("\nSelect the location where the new data should be stored.\n")
        save_location = DF.get_directory()
    elif change == '2':
        save_location = data_location
        print("\nThe data will be stored at: ", save_location)
    else:
        print("\nInvalid choice. Exiting...")
        save_location = data_location

    # Get the fieldnames from the first non-empty dictionary
    for row in data:
        if row:  # Find the first non-empty dictionary
            fieldnames = list(row.keys())
            break
    else:
        raise ValueError("Data contains only empty dictionaries.")

    # Write data to the new csv file
    with open(os.path.join(save_location, 'food_formatted.csv'), "w", newline = "") as csvfile:
        # fieldnames = data[0].keys() # Get the fieldnames from the first dictionary in the data
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames) # Create a DictWriter object
        writer.writeheader() # Write the header row
        writer.writerows(data)# Write the data rows
    
        print(f"CSV file saved to: {save_location}")

if __name__ == '__main__':
    __main__()