import os, pickle, pandas as pd, numpy as np, matplotlib.pyplot as plt, seaborn as sb
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import Dataframe_Functions as DF, File_Handling as FH

# Global Variables
df = DF.csv_to_dataframe(os.path.join(os.getcwd(), "backend", "Resources", "Data", 'fit_data.csv'), ",")

# Parameter grid for tuning Random Forest
PARAM_GRID = {
    'n_estimators': [100, 200, 300],  # Number of trees in the forest
    'max_depth': [None, 10, 20, 30],  # Maximum depth of the trees
    'min_samples_split': [2, 5, 10],  # Minimum samples required to split a node
}

def train_model(X_train, y_train, X_test, y_test, target_name, param_grid):
    # Initialize RandomForestRegressor
    rf = RandomForestRegressor(random_state=42)

    # Hyperparameter tuning using GridSearchCV
    grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=3, n_jobs=-1, verbose=2)
    
    # Train the model using the training data
    grid_search.fit(X_train, y_train)

    # Best parameters
    print(f"Best parameters for {target_name} prediction: {grid_search.best_params_}")

    # Train model using best parameters
    best_rf = grid_search.best_estimator_
    
    # Predict the test data
    y_pred = best_rf.predict(X_test)
    
    # Calculate Mean Squared Error
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error for {target_name} prediction: {mse:.4f}")

    # Plot results
    plot_results(best_rf, X_test, y_test, f"{target_name} prediction: Actual vs. Predicted")
    
    return best_rf

def train_body_fat():
    global df
    global PARAM_GRID

    X = df.drop(["Body Fat(%)", "Muscle(%)"], axis=1)
    y_fat = df["Body Fat(%)"]

    # Split data
    X_train, X_test, y_fat_train, y_fat_test = train_test_split(X, y_fat, test_size=0.2, random_state=42)

    # Train and save the best model for body fat prediction
    model_fat = train_model(X_train, y_fat_train, X_test, y_fat_test, "Body Fat", PARAM_GRID)

    # Save the model
    with open(os.path.join(FH.get_working_directory(), "Resources", "Models", "model_fat.pkl"), "wb") as f:
        pickle.dump(model_fat, f)

    print("Body Fat model trained and saved successfully.")

def train_muscle_mass():
    global df
    global PARAM_GRID

    X = df.drop(["Body Fat(%)", "Muscle(%)"], axis=1)
    y_muscle = df["Muscle(%)"]

    # Split data
    X_train, X_test, y_muscle_train, y_muscle_test = train_test_split(X, y_muscle, test_size=0.2, random_state=42)

    # Train and save the best model for muscle mass prediction
    model_muscle = train_model(X_train, y_muscle_train, X_test, y_muscle_test, "Muscle Mass", PARAM_GRID)

    # Save the model
    with open(os.path.join(FH.get_working_directory(), "Resources", "Models", "model_muscle.pkl"), "wb") as f:
        pickle.dump(model_muscle, f)

    print("Muscle Mass model trained and saved successfully.")

def predict_body_fat(age, gender, weight, height, exercise_week, waist, hips):
    input_data = pd.DataFrame([[age, gender, weight, height, exercise_week, waist, hips]], 
                              columns=df.drop(["Body Fat(%)", "Muscle(%)"], axis=1).columns)

    # Load the fat model
    with open(os.path.join(FH.get_working_directory(), "Resources", "Models", "model_fat.pkl"), "rb") as f:
        loaded_model = pickle.load(f)

    return loaded_model.predict(input_data)[0]

def predict_muscle_mass(age, gender, weight, height, exercise_week, waist, hips):
    input_data = pd.DataFrame([[age, gender, weight, height, exercise_week, waist, hips]], 
                              columns=df.drop(["Body Fat(%)", "Muscle(%)"], axis=1).columns)

    # Load the muscle model
    with open(os.path.join(FH.get_working_directory(), "Resources", "Models", "model_muscle.pkl"), "rb") as f:
        loaded_model = pickle.load(f)

    return loaded_model.predict(input_data)[0]

def plot_results(model, X_test, y_test, title):
    # Predict for the test data
    y_pred = model.predict(X_test) 

    plt.scatter(y_test, y_pred)

    # Regression Line and Error Bands
    z = np.polyfit(y_test, y_pred, 1)  # Linear regression fit
    p = np.poly1d(z)
    plt.plot(y_test, p(y_test), color='green', linestyle='-', label='Regression Line')

    # Standard error of the estimate (SEE)
    residuals = y_test - p(y_test)
    std_error = np.std(residuals)

    plt.fill_between(y_test, 
                     p(y_test) - 1.96 * std_error, 
                     p(y_test) + 1.96 * std_error, 
                     alpha=0.2, 
                     color='red', 
                     label='95% Confidence Interval')

    plt.xlabel("Actual Values")
    plt.ylabel("Predicted Values")
    plt.title(title)
    plt.legend()
    plt.show()

def get_significant_variables():
    global df
    plt.figure(figsize=(12, 10))
    sb.heatmap(df.corr(), annot=True)
    plt.show()

def __main__():
    # Train body fat and muscle mass models
    train_body_fat()
    train_muscle_mass()

    # Make predictions using the trained models
    body_fat = predict_body_fat(22, 1, 85, 185, 2, 87, 103)
    muscle_mass = predict_muscle_mass(22, 1, 85, 185, 2, 87, 103)
    print(f"Predicted Body Fat (%): {body_fat:.2f}, Predicted Muscle Mass (%): {muscle_mass:.2f}")

    # Visualize correlations in the dataset
    get_significant_variables()

if __name__ == '__main__':
    __main__()