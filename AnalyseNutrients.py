# System libraries
import sys, os

# Set working directory
sys.path.append(os.getcwd())

# Import my own libraries
import DataframeFunctions

# Read csv file into a dataframe
df = DataframeFunctions.create_dataframe("food.csv")
print(df)

# Create a subset to extract only fields required from dataset
vars_in_dataframe = ["Category", "Description", "Carbohydrate", "Cholesterol", "Fiber", "Kilocalories", "Protein", "Sugar Total", "Water", "Monosaturated Fat", "Polysaturated Fat", "Saturated Fat"]
df = DataframeFunctions.create_subset(df, vars_in_dataframe)
print(df)

# Extract all distinct food categories
categories = df["Category"].unique()
