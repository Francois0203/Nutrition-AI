import os, sys
import pandas, numpy

# Import custom libraries
import Dataframe_Functions as DF
import File_Handling as FH

# Create dataframe from the CSV file containing all the data
def create_user_df(data_location):
    df = DF.csv_to_dataframe(data_location, ",")

    return df

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

def __main__():
    # Create dataframe
    df = create_user_df(os.path.join(os.getcwd(), "Resources", "Data", 'users_new_2.csv'))
    bmi, classification = calculate_bmi(87, 185)
    #bai, classification = calculate_bai(84, 185)
    #whr, classification = calculate_whr('M', 84, 103)
    print(f"BMI: {bmi:.2f}, Classification: {classification}")

if __name__ == '__main__':
    __main__()