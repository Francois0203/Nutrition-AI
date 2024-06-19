import os, sys
import pandas as pd, numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# Import custom libraries
import Dataframe_Functions as DF
import File_Handling as FH

# Calculate body mass index and classify accordingly
def calculate_bmi(weight, height):
    height = height / 100 # Convert height from cm to m
    bmi = weight / (height ** 2) # Calculate bmi
    classification = ""

    if bmi < 18.5: classification = "Underweight"
    elif 18.5 <= bmi < 25: classification = "Normal Weight"
    elif 25 <= bmi < 30: classification = "Overweight"
    else: classification = "Obese"

    return bmi, classification

# Calculate body adiposity index and classify accordingly
def calculate_bai(hip_circumference, height):
    height = height / 100
    bai = (hip_circumference / (height ** 1.5)) - 18
    classification = ""

    if bai <= 20: classification = "Underweight"
    elif 20 < bai <= 25: classification = "Normal Weight"
    elif 25 < bai <= 30: classification = "Overweight"
    else: classification = "Obese"

    return bai, classification

# Calculate waist-to-hip ratio and classify accordingly
def calculate_whr(gender, waist, hip):
    whr = waist / hip
    classification = ""

    if gender == 'M':
        if whr <= 0.95: classification = "Normal Weight"
        elif 0.95 < whr <= 1: classification = "Overweight"
        else: classification = "Obese"
    elif gender == 'F':
        if whr <= 0.8: classification = "Normal Weight"
        elif 0.8 < whr <= 0.84: classification = "Overweight"
        else: classification = "Obese"

    return whr, classification

# Train fat and muscle percentage prediction models with user dataset
def train_models(df):
    # Define features and target variables
    X = df.drop(["Body Fat(%)", "Muscle(%)"], axis = 1)
    y_fat = df["Body Fat(%)"]
    y_muscle = df["Muscle(%)"]

    # Split data
    X_train, X_test, y_fat_train, y_fat_test, y_muscle_train, y_muscle_test = train_test_split(
        X, y_fat, y_muscle, test_size = 0.2, random_state = 42
    )

    # Choose and train a model (example: Random Forest)
    model_fat = RandomForestRegressor(n_estimators = 100, random_state = 42)
    fat_history = model_fat.fit(X_train, y_fat_train)

    model_muscle = RandomForestRegressor(n_estimators = 100, random_state = 42)
    muscle_history = model_muscle.fit(X_train, y_muscle_train)

    # Evaluate model performance
    y_fat_pred = model_fat.predict(X_test)
    y_muscle_pred = model_muscle.predict(X_test)
    mse_fat = mean_squared_error(y_fat_test, y_fat_pred)
    mse_muscle = mean_squared_error(y_muscle_test, y_muscle_pred)

    print("Mean Squared Error (Fat):", mse_fat)
    print("Mean Squared Error (Muscle):", mse_muscle)

    return model_fat, model_muscle

# Use models to predict fat and muscle percentage from user data
def predict_composition(input, model_fat, model_muscle):
    predicted_fat = model_fat.predict(input)[0]
    predicted_muscle = model_muscle.predict(input)[0]

    return predicted_fat, predicted_muscle

def __main__():
    df = DF.csv_to_dataframe(os.path.join(os.getcwd(), "Resources", "Data", 'users_new.csv'), ",") # Create dataframe

    # Train fat and muscle prediction models 
    fat_modl, muscle_modl = train_models(df)

    # Get user input
    age = int(input("Enter age: "))
    gender = float(input("Enter gender (1 = Male or 0 = Female): "))
    weight = float(input("Enter weight (kg): "))
    height = float(input("Enter height (cm): "))
    calories = float(input("Enter daily average calories intake: "))
    protein = float(input("Enter daily average protein intake (g): "))
    fat = float(input("Enter daily average fat intake (g): "))
    carbs = float(input("Enter daily average carbs intake (g): "))
    sugar = float(input("Enter daily average sugar intake (g): "))
    exercise = float(input("Enter how many times you exercise per week (1 - 7): "))
    waist = float(input("Enter waist circumference (cm): "))
    hip = float(input("Enter hip circumference (cm): "))
    data = pd.DataFrame([[age, gender, weight, height, calories, protein, fat, carbs, sugar, exercise, waist, hip]], columns = df.drop(["Body Fat(%)", "Muscle(%)"], axis = 1).columns)

    # Predict body fat and muscle % using trained models
    predicted_fat, predicted_muscle = predict_composition(data, fat_modl, muscle_modl)
    print(f"Predicted fat (%): {predicted_fat:.2f}, Predicted muscle (%): {predicted_muscle:.2f}")

if __name__ == '__main__':
    __main__()