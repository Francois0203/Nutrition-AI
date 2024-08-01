from flask import Flask, request, jsonify
from flask_cors import CORS

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
        age = data.get('age')
        exercise_days = data.get('exerciseDays')
        goal = data.get('goal')
        diet = data.get('diet')
        email = data.get('email')

        # Perform calculations here
        result = {
            'weight': weight,
            'height': height,
            'hip': hip,
            'waist': waist,
            'age': age,
            'exerciseDays': exercise_days,
            'goal': goal,
            'diet': diet,
            'email': email,
            'message': 'Calculations done'  # Example result
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
