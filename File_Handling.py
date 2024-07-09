import sys, os, csv
from pathlib import Path
import tkinter as tk
from tkinter import filedialog 

# Check if a file or directory exists
def directory_exists(path):
    return os.path.exists(path)

def file_exists(file_path):
    return Path(file_path)

def dataframe_to_csv(df, data_location, name):
    # Save subset dataframe to a CSV file
    if os.path.isfile(os.path.join(data_location, name + '.csv')):
        print(os.path.join(data_location, name + '.csv'), " already exists.")
    else:
        df.to_csv(os.path.join(data_location, name + '.csv'), sep = ',', index = False)
        print(os.path.join(data_location, name + '.csv'), " has successfully been created and saved.") 

# Get current working directory
def get_working_directory():
    return os.path.dirname(os.path.abspath(__file__))

# Create a folder in a specific location if it does not yet exist
def create_folder(name, location):
    if directory_exists == False:
        os.makedirs(os.path.join(location, name), exist_ok = True)

    return os.path.join(location, name)

def append_to_csv(file_path, item):
    try:
        with open(file_path, mode = 'a', newline = '', encoding = 'utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([item]) 
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def append_value_to_rows(file_path, text_to_append):
    temp_file_path = file_path + ".tmp"

    try:
        with open(file_path, 'r', encoding = 'utf-8') as csvfile, \
            open(temp_file_path, 'w', newline = '', encoding = 'utf-8') as temp_csvfile:
            reader = csv.reader(csvfile)
            writer = csv.writer(temp_csvfile)

            for row in reader:
                writer.writerow(row + [text_to_append])  # Append to the row

        # Replace original file with modified file
        import os
        os.remove(file_path)
        os.rename(temp_file_path, file_path)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

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
    
    file_path = os.path.join(os.getcwd(), "Resources", "Data", "all_diets_copy.csv") 
    text_to_append = "new_value"

    append_value_to_rows(file_path, text_to_append)

if __name__ == "__main__":
    __main__()