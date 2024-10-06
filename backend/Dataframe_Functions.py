import os, pandas as pd

# Global variables
DATA_LOCATION = os.path.join(os.getcwd(), "Resources", "Data")

# Create a dataframe from a csv file
def csv_to_dataframe(file, delim):
    try:
        df = pd.read_csv(file, delimiter = delim)
        return df
    except FileNotFoundError:
        print(f"Error: File not found at '{file}'")
        return None
    except pd.errors.EmptyDataError:
        print(f"Error: CSV file at '{file}' is empty")
        return None
    except pd.errors.ParserError:
        print(f"Error: Parsing error while reading '{file}'")
        return None

# Create subset of columns from dataset
def create_subset(df, vars):
    if vars:
        try:
            df = df[vars]
        except KeyError:
            print(f"Warning: Some requested columns ({', '.join(vars)}) are missing in the dataframe.")

    return df

# Get specific record from dataframe that has a certain variable value
def get_record(df, field, value): 
    selected_rows = df.loc[df[field] == value]

    return selected_rows

# Extract specific field value from a record
def get_field(df, field):
    selected_field = df[[field]]

    return selected_field

def __main__():
    pass

if __name__ == '__main__':
    __main__()