# System libraries
import sys, os

# Set working directory
sys.path.append(os.getcwd())

# Import my own libraries
import DataframeFunctions

# Read csv file into a dataframe
df = DataframeFunctions.create_dataframe("Users.csv")
print(df)

# Numerical variables in dataframe
vars = ["Age", "Weight (kg)", "Length (cm)", "Muscle (%)", "Fat (%)", "Daily Average Calories", "Daily Average Protein (g)", "Daily Average Fat (g)", "Daily Average Sugar (g)"]

# Create another dataframe with just the numerical values
num_df = DataframeFunctions.create_subset(df, vars)