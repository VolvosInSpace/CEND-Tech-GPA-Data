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


def GetAvgGPAS():
    pass

def PlaceInList():
    pass


# Example usage:
# file_paths = ["file1.txt", "file2.txt", "file3.txt"]
# files = open_files(file_paths)
# # Perform operations on files
# close_files(files)