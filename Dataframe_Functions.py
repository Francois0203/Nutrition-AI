import sys, os

import pandas as pd
import numpy as np

import tkinter as tk
from tkinter import filedialog 

# Global variables
DATA_LOCATION = os.path.join(os.getcwd(), "Resources", "Data")

# Create a dataframe from a csv file
def csv_to_dataframe(file, delim):
    try:
        df = pd.read_csv(file, delimiter = delim)
        return df
    except FileNotFoundError:
        print(f"Error: File not found at '{file}'")
        return None
    except pd.errors.EmptyDataError:
        print(f"Error: CSV file at '{file}' is empty")
        return None
    except pd.errors.ParserError:
        print(f"Error: Parsing error while reading '{file}'")
        return None

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

# Get current working directory
def get_working_directory():
    script_directory = os.path.dirname(os.path.abspath(__file__))

    return script_directory

# Create a folder in a specific location if it does not yet exist
def create_folder(name, location):
    data_directory = os.path.join(location, name)
    os.makedirs(data_directory, exist_ok = True)

    return data_directory

# Select a save location
def get_directory():
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window

    # Ask if the user wants to browse or enter manually
    choice = input("Choose how to provide the directory path:\n1. Browse\n2. Enter manually\nYour choice (1 or 2): ")

    if choice == '1':
        directory = filedialog.askdirectory(title = "Select a directory")
    elif choice == '2':
        directory = input("Enter the directory path: ")
    else:
        print("Invalid choice. Exiting...")
        return None

    # Basic validation to ensure it's a valid path
    if not os.path.isdir(directory):
        print("Invalid directory. Exiting...")
        return None

    return directory

def __main__():
    # Variables
    global DATA_LOCATION

    # Get working directory
    script_directory = get_working_directory()
    print("Working directory: ", script_directory)

    # Change data directory
    change = input("Do you want to change the directory where your data is stored?:\n1. Yes\n2. No\nYour choice (1 or 2): ")

    if change == '1':
        print("\nSelect the location where the data is stored.\n")
        data_loc = get_directory()
    elif change == '2':
        data_loc = DATA_LOCATION
        print("Data is found at: ", data_loc)
    else:
        print("Invalid choice. Exiting...")
        data_loc = DATA_LOCATION

if __name__ == '__main__':
    __main__()