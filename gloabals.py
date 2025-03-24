import os
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

def get_files_in_dir(directory):
    """
    Get all files in a directory.
    
    Args:
        directory (str): Directory to get files from.
        
    Returns:
        list: List of file paths in the directory.
    """
    return [os.path.join(directory, file) for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]

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
