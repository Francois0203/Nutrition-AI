import sys, os
import pandas as pd

# Set working directory
sys.path.append(os.getcwd())

# Import custom libraries
import Dataframe_Functions as DF

# Set data directory
script_directory = DF.get_working_directory()
print("Working directory: ", script_directory)

# Create dataframe from data stored in specific 'Data' directory
print("\nSelect the location where the data is stored.\n")
data_location = DF.get_directory()

# Read the data from the file using the appropriate encoding.
with open('food.csv', 'r', encoding = 'utf-8') as file:
    data = file.read()

# Remove extra double quotes.
data = data.replace('""', '"')

# Split the data into rows using ';;' as the delimiter.
rows = data.strip().split(';;')

# Extract column names from the first row.
column_names = rows[0].split(',')

# Split the remaining rows into values.
values = [row.split(',') for row in rows[1:]]

# Find the maximum number of values in any row.
max_values = max(len(row) for row in values)

# Fill missing values with None.
values = [row + [None] * (max_values - len(row)) for row in values]

# Create a dictionary from the data.
data_dict = {col: [row[i] for row in values] for i, col in enumerate(column_names)}

# Create the DataFrame.
df = pd.DataFrame(data_dict)

# Save the DataFrame to a new CSV file with proper formatting.
df.to_csv('Resources/Data/formatted_food_data.csv', index = False)
