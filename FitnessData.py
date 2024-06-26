import random

class FitnessData:

    def __init__(self, age, gender, weight, muscle_mass_percentage, body_fat_percentage, 
                daily_calories, daily_protein, daily_fat, daily_carb, daily_sugar, weekly_exercise,
                waist_circumference, hip_circumference):
        self.age = age
        self.gender = gender
        self.weight = weight
        self.muscle_mass_percentage = muscle_mass_percentage
        self.body_fat_percentage = body_fat_percentage
        self.daily_calories = daily_calories
        self.daily_protein = daily_protein
        self.daily_fat = daily_fat
        self.daily_carb = daily_carb
        self.daily_sugar = daily_sugar
        self.weekly_exercise = weekly_exercise
        self.waist_circumference = waist_circumference
        self.hip_circumference = hip_circumference

    def set_weight(self):
        if self.gender == 0:
            if self.age < 5:
                return random.random(0, 20)
        else:
            return 50
        
    def __main__():
        pass

    if __name__ == "__main__()":
        __main__()