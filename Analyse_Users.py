import os, sys
import pandas, numpy

# Import custom libraries
import Dataframe_Functions as DF
import File_Handling as FH

# Create dataframe from the CSV file containing all the data
def create_user_df(data_location):
    df = DF.csv_to_dataframe(data_location, ",")

    return df

def __main__():
    # Create dataframe
    df = create_user_df(os.path.join(os.getcwd(), "Resources", "Data", 'Users.csv'))

if __name__ == '__main__':
    __main__()