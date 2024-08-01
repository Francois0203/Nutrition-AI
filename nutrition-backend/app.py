import os, sys
from flask import Flask, request, jsonify
from flask_cors import CORS

# Import custom libraries
import Dataframe_Functions as DF, File_Handling as FH, User_Calculations as UC, Analyse_Nutrients as AN, Analyse_User_Model as AUM

app = Flask(__name__)

CORS(app)

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json
        # Extract input data
        weight = data.get('weight')
        height = data.get('height')
        hip = data.get('hip')
        waist = data.get('waist')
        gender = 1 # data.get('gender')
        age = data.get('age')
        exercise_days = data.get('exerciseDays')
        goal = data.get('goal')
        diet = data.get('diet')
        email = data.get('email')

        # Calculations
        meal_df = DF.csv_to_dataframe(os.path.join(os.getcwd(), "Resources", "Data", "all_diets.csv"), ',')
        bmi = UC.calculate_bmi(weight, height)
        bai = UC.calculate_bai(hip, height)
        whr = UC.calculate_whr(gender, waist, hip)
        body_fat = 20
        body_mass = 60
        exercise_category = UC.calculate_exercise_level(exercise_days)
        main_cals = UC.calculate_maintenance_calories(age, weight, height, gender, exercise_category)
        optimal_macros = UC.calculate_optimal_macros(weight, body_mass, exercise_days, main_cals, goal)
        meals = AN.optimise_meals(meal_df, goal, diet, optimal_macros, 2)

        # Return results
        result = {
            'bmi': bmi,
            'bai': bai,
            'whr': whr,
            'body_fat': body_fat,
            'body_mass': body_mass,
            'exercise_category': exercise_category,
            'main_calories': main_cals,
            'optimal_macros': optimal_macros,
            'meals': meals
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
