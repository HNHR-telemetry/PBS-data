import pandas
import os

def scan(data_dir):
    directories = os.listdir(data_dir)
    # Make a dataframe to hold all the data
    df = pandas.DataFrame()
    # Go through all the directories + files in the scanned directory (dataclean2)
    for directory in directories:
        files = os.listdir(data_dir + "/" + directory)
        for file in files:
            if(".txt" in file):
                # Print the name of the file as you run through it, to show progress
                print(data_dir + "/" + directory + "/" + file)
                # Read in date values & bird IDs as strings to keep from reading in as floats
                df = df.append(pandas.read_csv(data_dir + "/" + directory + "/" + file, dtype={"Detection_date": str,
                                                                                               "Session_date": str,
                                                                                               "Bird_ID": str}))
    # Write the full dataset (including duplicates) to a .csv, excluding the row numbers (index)
    df.to_csv("../Data/all_data.txt", index=False)
    # Use pandas to drop duplicate rows - this keeps the first occurrence of every row
    cons_df = df.drop_duplicates()
    # Write the consolidated dataset to a .csv, excluding the row numbers (index)
    cons_df.to_csv("../Data/cons_data.txt", index=False)

scan("../Data/dataclean2")


