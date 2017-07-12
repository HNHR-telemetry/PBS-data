# This script uses reservoir sampling to make a test dataset from the actual data
import random

with open("../Data/cons_data.txt", "r") as infile:
    with open("../Data/test_data.txt", "w") as outfile:
        outfile.write("Detection_date,Detection_time,Tag_ID,Signal_strength,Connection,Unit,Session_date,Session_time,"
                      "Session_loc,Bird_ID,Home_Location,Sex,Status\n") # Write the column headings
        infile.readline() # Skip the column headings
        chances_selected = .005 # Take .5% of the lines
        for line in infile:
            chance = random.random() # Create a pseudorandom number between 0 and 1
            if chance < chances_selected: # If the pseudorandom number is under the chosen chance level, write it
                outfile.write(line)