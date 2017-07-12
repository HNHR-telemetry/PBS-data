import os
import string
import re

# This script is used for the basic cleaning of all the files, to produce readable datafiles.
# It only changes the format of the files, does not remove bad data.

# Define 'scan' as reading through the data directory, parsing into files, and giving the name of the new directory
def scan(data_dir, clean_data_dir):
    directories = os.listdir(data_dir)
    for directory in directories:
        files = os.listdir(data_dir + "/" + directory)
        for file in files:
            print(clean_data_dir + "/" + directory)
            parse(data_dir + "/" + directory + "/" + file, clean_data_dir + "/" + directory, file)

#The arguments for this are stupid, but oh well.
def parse(filename, dest, file_suffix):
    if not os.path.exists(dest):
        os.makedirs(dest)
    # Clear out junk files (all data files are .txt)
    if "txt" not in filename:
        print("Invalid file type: " + filename)
        return
    with open(filename, "r") as read:
        with open(dest + "/" + file_suffix, "w") as write:
            # Write the first line of the file as column names
            write.write("Detection_date,Detection_time,Tag_ID,Signal_strength,Connection,Unit,Session_date,Session_time\n")
            # Make a variable for the session information
            session_info = ""
            for line in read: # For each line of the file
                if line[0] == "$": # If the line is a session line
                    # Split the line by commas and by T, take the date - time
                    session_info = re.split(',|T', line)[3] + "," + re.split(',|T', line)[4]

                elif not (re.match(r'[0-9]+.*', line)): # Pass by any non-session non-data lines
                    pass
                else:
                # Lazy way activated - use line length to determine data lines. Takes a while to load
                    if len(line) == 42 or len(line) == 41: # Hard-coded line lengths of data lines
                        line = remove_non_ascii(line[0:-1]) # Remove the weird non-ASCII characters
                        lines = re.split(',|T', line) # Split the line by , and T
                        for cell in lines:
                            if " " not in cell: # If the cell does not contain a space (date or time)
                                write.write(cell + ",")
                            else: # Hard-coded line splits for tag ID, signal strength, and connection
                                #print(line)
                                #print(cell)
                                write.write(cell[0:9] + ",")
                                write.write(cell[10:12] + ",")
                                write.write(cell[12:14] + ",")
                        write.write(file_suffix[0:5] + ",") # Tack on the Unit #
                        write.write(session_info + "\n")

def remove_non_ascii(s): # Definition of function to remove non-ASCII characters
    return s.encode('ascii',errors='ignore').decode()




scan("../Data/RawDetections", "../Data/dataclean")


