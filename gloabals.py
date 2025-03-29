import os
import pandas as pd
'''
Open Files  -   Open all given files
    Put files into data frames per name
        Make sure multiple files don't get opened twice
Close Files -   Close all given files

Convert GPA into numbers
Find average gpas (Per section, group)
Work List Bad/Good
'''

GRADE_MAP = {
    "A": 4.00,
    "A-": 3.67,
    "B+": 3.33,
    "B": 3.00,
    "B-": 2.67,
    "C+": 2.33,
    "C": 2.00,
    "C-": 1.67,
    "D+": 1.33,
    "D": 1.00,
    "D-": 0.67,
    "F": 0.00,
    "I": None,
    "W": None,
    "P": None,
    "NP": None
}

def load_files_to_dataframes():
    current_dir = os.getcwd()
    extensions = ('.run', '.grp', '.sec')
    dataframes = {}

    for file in os.listdir(current_dir):
        if file.endswith(extensions):
            file_path = os.path.join(current_dir, file)
            file_name = os.path.splitext(file)[0]  # Remove extension
            
            try:
                df = pd.read_csv(file_path, sep=",", skiprows=1, header=None)

                # Remove all quotes from every string in the DataFrame
                df = df.map(lambda x: x.replace('"', '') if isinstance(x, str) else x)

                dataframes[file_name] = df
                print(f"Loaded {file} into dataframe '{file_name}'")
            except Exception as e:
                print(f"Could not read {file}: {e}")

    return dataframes

# Loads the files into the dataframes
dataframes = load_files_to_dataframes()

# Access a dataframe by its filename
# print(dataframes["example"]) for a file named 'example.run' 
for name, df in dataframes.items():
    print(f"DataFrame for {name}:\n{df}\n{'-'*50}")

def close_files(file_objects):
    """
    Closes a list of file objects.
    
    Args:
        file_objects (list): List of file objects to close.
    """
    for file in file_objects:
        try:
            file.close()
        except IOError as e:
            print(f"Error closing file: {e}")

def grades_to_num(section):
    """
    convert grades to numbers and add to a new row in df

    Args: 
        section (df): section to convert
    """
    section['Numeric Grade'] = section.iloc[:, 2].map(GRADE_MAP)

def section_GPA(section):
    """
    finds the GPA of a section

    Args:
        section (df): section to find GPA of
    
    Returns:
        float: the GPA of that section
    """
    return section['Numeric Grade'].mean()


def PlaceInList():
    pass


# Example usage:
# file_paths = ["file1.txt", "file2.txt", "file3.txt"]
# files = open_files(file_paths)
# # Perform operations on files
# close_files(files)
