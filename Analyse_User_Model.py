import os, sys, pandas as pd, numpy as np, matplotlib.pyplot as plt, seaborn as sb
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.svm import SVR

# Import custom libraries
import Dataframe_Functions as DF, File_Handling as FH

df = DF.csv_to_dataframe(os.path.join(os.getcwd(), "Resources", "Data", 'fitness_data.csv'), ",") # Create dataframe

# Train fat and muscle percentage prediction models with user dataset
def predict_composition(input):
    global df

    # Define features and target variables
    X = df.drop(["Body Fat(%)", "Muscle(%)", "Daily Average Calorie Intake", "Daily Average Protein Intake(g)", "Daily Average Fat Intake(g)" , "Daily Average Carb Intake(g)", "Daily Average Sugar Intake(g)"], axis = 1)
    y_fat = df["Body Fat(%)"]
    y_muscle = df["Muscle(%)"]

    # Split data
    X_train, X_test, y_fat_train, y_fat_test, y_muscle_train, y_muscle_test = train_test_split(
        X, y_fat, y_muscle, test_size = 0.2, random_state = 42
    )

    # Hyperparameter tuning for Random Forest
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [None, 10, 20]
    }

    # Choose and train the models
    #model_fat = GridSearchCV(RandomForestRegressor(random_state = 42), param_grid, cv = 5)
    model_fat = RandomForestRegressor(n_estimators = 100, random_state = 42)
    #model_fat = GradientBoostingRegressor(random_state = 42)
    #model_fat = LinearRegression()
    #model_fat = Ridge(alpha = 1)
    #model_fat = Lasso(alpha = 1)
    #model_fat = SVR(kernel = 'linear') # kernal = linear/rbf/poly
    model_fat.fit(X_train, y_fat_train)

    #model_muscle = GridSearchCV(RandomForestRegressor(random_state = 42), param_grid, cv = 5)
    model_muscle = RandomForestRegressor(n_estimators = 100, random_state = 42)
    #model_muscle = GradientBoostingRegressor(random_state = 42)
    #model_muscle = LinearRegression()
    #model_muscle = Ridge(alpha = 1)
    #model_muscle = Lasso(alpha = 1)
    #model_muscle = SVR(kernel = 'linear')
    model_muscle.fit(X_train, y_muscle_train)

    # Evaluate model performance
    y_fat_pred = model_fat.predict(X_test)
    y_muscle_pred = model_muscle.predict(X_test)
    mse_fat = mean_squared_error(y_fat_test, y_fat_pred)
    mse_muscle = mean_squared_error(y_muscle_test, y_muscle_pred)

    # Use models to predict fat and muscle percentage from user data
    predicted_fat = model_fat.predict(input)[0]
    predicted_muscle = model_muscle.predict(input)[0]

    # Plot results to see how the models perform
    plot_results(model_fat, X_test, y_fat_test, "Body fat (%) prediction: Actual vs. predicted")
    plot_results(model_muscle, X_test, y_muscle_test, "Muscle mass (%) prediction: Actual vs. predicted")

    return predicted_fat, predicted_muscle

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
    # data = pd.DataFrame([[22, 1, 87, 185, 4, 85, 103]], columns = df.drop(["Body Fat(%)", "Muscle(%)", "Daily Average Calorie Intake", "Daily Average Protein Intake(g)", "Daily Average Fat Intake(g)" , "Daily Average Carb Intake(g)", "Daily Average Sugar Intake(g)"], axis = 1).columns) # Francois
    
    # # Predict body fat and muscle % using trained models
    # predicted_fat, predicted_muscle = predict_composition(df, data)
    # print(f"Predicted fat (%): {predicted_fat:.2f}, Predicted muscle (%): {predicted_muscle:.2f}")

    get_significant_variables()

if __name__ == '__main__':
    __main__()