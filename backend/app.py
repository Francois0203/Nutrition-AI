import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import User_Calculations as UC, Analyse_Nutrients as AN, Analyse_User_Model as AUM, System_Functions as SF

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
        gender = data.get('gender')
        age = data.get('age')
        exercise_days = data.get('exerciseDays')
        goal = data.get('goal')
        diet = data.get('diet')
        email = data.get('email')

        # Calculations
        bmi = UC.calculate_bmi(weight, height)
        bai = UC.calculate_bai(hip, height)
        whr = UC.calculate_whr(gender, waist, hip)
        body_fat = AUM.predict_body_fat(age, gender, weight, height, exercise_days, hip, waist)
        body_mass = AUM.predict_muscle_mass(age, gender, weight, height, exercise_days, hip, waist)
        exercise_category = UC.calculate_exercise_level(exercise_days)
        main_cals = UC.calculate_maintenance_calories(age, weight, height, gender, exercise_category)
        optimal_protein, optimal_carbs, optimal_fats, total_calories = UC.calculate_optimal_macros(weight, body_mass, exercise_days, main_cals, goal)
        meals = AN.optimise_meals(goal, diet, 3, optimal_protein, optimal_carbs, optimal_fats)

        # Generate pdf
        pdf_path = r"C:\Personal Projects\Nutrition-AI\backend\Resources\Results"
        pdf_name = email + " Results"
        content = [bmi, bai, whr, body_fat, body_mass, exercise_category, main_cals, optimal_protein, optimal_fats, optimal_carbs, meals]
        SF.generate_pdf(pdf_path, pdf_name, content)

        # Send email
        #content = f"BMI: {bmi} \n BAI: {bai} \n Waist-toHip Ratio: {whr} \n\n Body Fat %: {body_fat} \n Muscle Mass %: {body_mass} \n Exercise Category: {exercise_category} \n Maintenance Calories: {main_cals} \n\n Optimal Macros: \n Protein: {optimal_protein} \n Fat: {optimal_fats} \n Carbs: {optimal_carbs} \n\n Rcommended Daily Meals: \n {meals}"
        subject = "Nutrition AI Results"
        body = "Your results from the Nutrition AI application are attached below. "
        attachment = os.path.join(pdf_path, pdf_name + '.pdf')
        SF.send_email(email, subject, body, attachment)

        # Return results to frontend
        result = {
            'bmi': bmi,
            'bai': bai,
            'whr': whr,
            'body_fat': body_fat,
            'body_mass': body_mass,
            'exercise_category': exercise_category,
            'main_calories': main_cals,
            'optimal_protein': optimal_protein,
            'optimal_carbs': optimal_carbs,
            'optimal_fats': optimal_fats,
            'total_calories': total_calories,
            'meals': meals
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
