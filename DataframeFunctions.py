# System libraries
import sys, os

# Dataframe and array libraries
import pandas as pd
import numpy as np

# Import libraries that make data easier to read
import seaborn as sns
import matplotlib.pyplot as plt

# Set working directory
sys.path.append(os.getcwd())

# Read csv file into a dataframe
def create_dataframe(file):
    df = pd.DataFrame(pd.read_csv(file, header = 0))

    return df

# Create subset of columns from dataset
def create_subset(df, vars):
    if vars:
        try:
            df = df[vars]
        except KeyError:
            print(f"Warning: Some requested columns ({', '.join(vars)}) are missing in the dataframe.")

    return df

# Get specific record from dataframe
def get_record(df, field, value): 
    selected_rows = df.loc[df[field] == value]

    return selected_rows

# Extract specific field value from a record
def get_field(df, field):
    selected_field = df[[field]]

    return selected_field

# Create correlation matrix of specific variables
def corr_mat(df, variables):
    correlation_matrix = df[variables].corr()

    return correlation_matrix

# Draw heatmap of correlation matrix to easily view weak vs strong correlations
def draw_matrix_heatmap(corr_mat, name):
    sns.set(font_scale = 1)  # Adjust font size for readability
    plt.figure(figsize = (6, 4))  # Set the figure size

    # Create the heatmap
    sns.heatmap(corr_mat, annot = True, cmap = "coolwarm", 
                linewidths = 0.5, square = True, 
                annot_kws = {"fontsize": 8})

    # Customize the plot (optional)
    plt.title("Correlation Heatmap")
    plt.subplots_adjust(bottom = 0.30)

    # Create file path of where the image of the plot should be saved
    folder_path = os.path.join(os.getcwd(), "Resources", "Images")
    file_path = os.path.join(folder_path, name + " Correlation Heatmap.png")

    # Check if image of plot already exists
    if os.path.exists(file_path):
        # If it exists, remove it to ensure a clean overwrite
        os.remove(file_path)

    # Save new plot
    plt.savefig(file_path, dpi = 600)