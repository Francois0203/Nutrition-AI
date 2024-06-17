import sys, os
import tkinter as tk
from tkinter import filedialog 

# Check if a file or directory exists
def directory_exists(path):
    return os.path.exists(path)

# Get current working directory
def get_working_directory():
    script_directory = os.path.dirname(os.path.abspath(__file__))

    return script_directory

# Create a folder in a specific location if it does not yet exist
def create_folder(name, location):

    data_directory = os.path.join(location, name)

    if directory_exists == False:
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