import tkinter as tk
from tkinter import ttk  # Import ttk for more modern widgets

# Create the main window
root = tk.Tk()
root.title("Nutrition App")

# Title label (using grid)
title_label = tk.Label(root, text="Nutrition AI", font=("Arial", 24, "bold"), bg="#333333", fg="white")
title_label.grid(row=0, column=0, columnspan=2, pady=20)  # Span across columns for centering

# Weight Label
weight_label = tk.Label(root, text="Weight:", bg="#333333", fg="white", font=("Arial", 12, "bold"))
weight_label.grid(row=1, column=0, sticky="e", padx=(10, 0), pady=10) 

# Dropdown box (using ttk.Combobox)
weight_options = [str(i) + " kg" for i in range(1, 101)]
weight_combobox = ttk.Combobox(root, values=weight_options, state="readonly")
weight_combobox.set("50 kg")
weight_combobox.grid(row=1, column=1, sticky="w", padx=(0, 10), pady=10) 

# Height Label
height_label = tk.Label(root, text="Height:", bg="#333333", fg="white", font=("Arial", 12, "bold"))
height_label.grid(row=2, column=0, sticky="e", padx=(10, 0), pady=10)  

# Dropdown box (using ttk.Combobox)
height_options = [str(i) + " cm" for i in range(50, 251)]  # Height options from 50cm to 250cm
height_combobox = ttk.Combobox(root, values=height_options, state="readonly")
height_combobox.set("170 cm")  # Default selection (adjust as needed)
height_combobox.grid(row=2, column=1, sticky="w", padx=(0, 10), pady=10) 

# Set window size
root.geometry("600x400")  # Adjust as needed

# Dark gray background color
root.configure(bg = "#333333") 

# Rounded edges (Tkinter doesn't have built-in rounded corners)
# You'll need a workaround or consider a different toolkit like PyQt 
# for this specific styling.

# Run the application
root.mainloop()
