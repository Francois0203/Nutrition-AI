# System libraries
import sys, os

# GUI libraries
import customtkinter as ctk 
import tkinter.messagebox as tkmb 

# Set working directory
sys.path.append(os.getcwd())

# Import custom python scripts
import DataframeFunctions

# GUI main theme
ctk.set_appearance_mode("system") 
ctk.set_default_color_theme("green") # Secondary color theme

# Create main nutrition form
main_form = ctk.CTk() 
main_form.minsize(800, 600) 
main_form.title("Smart Nutrition App") 

# Start GUI loop
main_form.mainloop()