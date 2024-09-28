import os

def load_csv_files(directory, file_prefix="ctg_tick", file_extension=".csv"):
    """
    Reads CSV files from the specified directory. Cleans them (converts strings to numercics as needed, 
    changes any empty values or abstract values) and stores each line in a list within a giant 2D list. 
    Contains error handling for inabiity to find the file or trouble reading the file.
    
    Args:
    - directory (str): The directory where CSV files are located.
    - file_prefix (str): The prefix for the CSV file names (default is "ctg_tick").
    - file_extension (str): The extension of the file (default is ".csv").
    
    Returns:
    - data (list): A list of data read from all the CSV files.

    Assumptions:
    - I assume that tick data will remain in the hundreds. While I understand this is not always 
    generalizable code, it works for the particular instance and could easily be edited for other general values. 

    Four data errors it catches: 
    1. Empty price values
    2. Negative price values
    3. Incorrect price values (clearly off)
    4. 
    """
    
    data = []
    file_list = os.listdir(directory)
    err = False
    
    for file_name in file_list:
        if file_name.startswith(file_prefix) and file_name.endswith(file_extension):
            try:
                
                file_path = os.path.join(directory, file_name)
                
                with open(file_path, 'r') as file:

                    file_data = [line.rstrip('\n') for line in file.readlines()[1:]] #  read file while getting rid of the unneeded '\n' at the end of lines and skip the first line (header) of the file
                    file_data = [line.split(',') for line in file_data] # create a list for each line where each feature is its own element

                    ## convert price and size to floats
                    ## check if either value is empty or a weird value, if it is, convert it to the value in the line before it (line after if it is first line)
                    for line in range(0, len(file_data)):
                        ## if empty
                        if (file_data[line][1] == ''):
                            if line != 0:
                                file_data[line][1] = file_data[line-1][1]
                            else:
                                # iterate through the rest of the lines until you find a non empty one to replace it with
                                for n in range(1, len(file_data)):
                                    if file_data[line+n][1] != '':
                                        file_data[line][1] = file_data[line+n][1] 

                        # if negative
                        if ('-' in file_data[line][1]):
                            # remove '-' from string
                            file_data[line][1] = file_data[line][1][1:]
                        # if decimal in wrong spot
                        if (file_data[line][1][3] != '.'): 
                            # switch . with number 
                            file_data[line][1][2], file_data[line][1][3] = file_data[line][1][3], file_data[line][1][2]
                            

                        ## convert price and volume to float and int respectively
                        file_data[line][1] = float(file_data[line][1])
                        file_data[line][2] = int(file_data[line][2])


                    data.extend(file_data)

            except FileNotFoundError:
                print(f"File {file_name} not found. Skipping...")
            except Exception as e:
                print(f"An error occurred while reading {file_name}: {e}")
    
    return data

# Example usage:
directory_path = "data"
loaded_data = load_csv_files("data")
print(loaded_data)

#TODO implement validation checks for data loading
#TODO data interface development
