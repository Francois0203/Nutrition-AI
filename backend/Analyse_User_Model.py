import os, pickle, pandas as pd, numpy as np, matplotlib.pyplot as plt, seaborn as sb
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# Import custom libraries
import Dataframe_Functions as DF, File_Handling as FH

# Global Variables
df = DF.csv_to_dataframe(os.path.join(os.getcwd(), "backend", "Resources", "Data", 'fit_data.csv'), ",") # Create dataframe

def train_body_fat():
    global df
    global PARAM_GRID

    X = df.drop(["Body Fat(%)", "Muscle(%)"], axis = 1)
    y_fat = df["Body Fat(%)"]

    # Split data
    X_train, X_test, y_fat_train, y_fat_test = train_test_split(X, y_fat, test_size = 0.2, random_state = 42)

    # Train the model
    model_fat = RandomForestRegressor(n_estimators = 100, random_state = 42)

    model_fat.fit(X_train, y_fat_train)

    # Evaluate model performance
    y_fat_pred = model_fat.predict(X_test)
    mse_fat = mean_squared_error(y_fat_test, y_fat_pred)

    plot_results(model_fat, X_test, y_fat_test, "Body fat (%) prediction: Actual vs. predicted")

    # Save model
    with open(os.path.join(FH.get_working_directory(), "Resources", "Models", "model_fat.pkl"), "wb") as f:
        pickle.dump(model_fat, f)

    print("Model trained and saved successfully as model_fat.pkl")

def train_muscle_mass():
    global df
    global PARAM_GRID

    X = df.drop(["Body Fat(%)", "Muscle(%)"], axis = 1)
    y_muscle = df["Muscle(%)"]

    # Split data
    X_train, X_test, y_muscle_train, y_muscle_test = train_test_split(X, y_muscle, test_size = 0.2, random_state = 42)

    # Train the model
    model_muscle = RandomForestRegressor(n_estimators = 100, random_state = 42)

    model_muscle.fit(X_train, y_muscle_train)

    # Evaluate model performance
    y_muscle_pred = model_muscle.predict(X_test)
    mse_muscle = mean_squared_error(y_muscle_test, y_muscle_pred)

    plot_results(model_muscle, X_test, y_muscle_test, "Muscle mass (%) prediction: Actual vs. predicted")

    # Save model
    with open(os.path.join(FH.get_working_directory(), "Resources", "Models", "model_muscle.pkl"), "wb") as f:
        pickle.dump(model_muscle, f)

    print("Model trained and saved successfully as model_muscle.pkl")

def predict_body_fat(age, gender, weight, height, exercise_week, waist, hips):
    input = pd.DataFrame([[age, gender, weight, height, exercise_week, waist, hips]], columns = df.drop(["Body Fat(%)", "Muscle(%)"], axis = 1).columns)

    # Open the fat model file
    with open(os.path.join(FH.get_working_directory(), "Resources", "Models", "model_fat.pkl"), "rb") as f:
        loaded_model = pickle.load(f)

    return loaded_model.predict(input)[0]

def predict_muscle_mass(age, gender, weight, height, exercise_week, waist, hips):
    input = pd.DataFrame([[age, gender, weight, height, exercise_week, waist, hips]], columns = df.drop(["Body Fat(%)", "Muscle(%)"], axis = 1).columns) 

    # Open the muscle model file
    with open(os.path.join(FH.get_working_directory(), "Resources", "Models", "model_muscle.pkl"), "rb") as f:
        loaded_model = pickle.load(f)

    return loaded_model.predict(input)[0]

def plot_results(model, x_test, y_test, title):
    # Predict for the test data
    y_pred = model.predict(x_test) 

    plt.scatter(y_test, y_pred) # Plot values

    # Regression Line and Error Bands
    z = np.polyfit(y_test, y_pred, 1)  # Fit a linear regression
    p = np.poly1d(z)
    plt.plot(y_test, p(y_test), color = 'green', linestyle = '-', label = 'Regression Line')

    # Standard error of the estimate (SEE)
    residuals = y_test - p(y_test)
    std_error = np.std(residuals)

    plt.fill_between(y_test, 
                    p(y_test) - 1.96*std_error, 
                    p(y_test) + 1.96*std_error, 
                    alpha = 0.2, 
                    color = 'red', 
                    label = '95% Confidence Interval')

    plt.xlabel("Actual Values")
    plt.ylabel("Predicted Values")
    plt.title(title)
    plt.legend()
    plt.show()

def get_significant_variables():
    global df

    # Correlation Heatmap
    plt.figure(figsize = (12, 10))
    sb.heatmap(df.corr(), annot = True)
    plt.show()

def __main__():
    # Train body fat and muscle mass prediction models
    # train_body_fat()
    # train_muscle_mass()

    # Use trained models to predict body fat and muslce mass
    body_fat = predict_body_fat(22, 1, 85, 185, 2, 87, 103)
    muscle_mass = predict_muscle_mass(22, 1, 85, 185, 2, 87, 103)
    print(f"Predicted fat (%): {body_fat:.2f}, Predicted muscle (%): {muscle_mass:.2f}")

    get_significant_variables()

if __name__ == '__main__':
    __main__()