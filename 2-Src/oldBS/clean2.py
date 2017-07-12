import os

# This script is run second (after clean.py)
# Its purpose is to pull out any and all sessions with bad data, so they can be ignored for analysis

def scan(data_dir):
    directories = os.listdir(data_dir)
    for directory in directories:
        files = os.listdir(data_dir + "/" + directory)
        for file in files:
            check_file(data_dir + "/" + directory + "/" + file)

open("../Data/BadFiles.txt", "w")
#opens a new version of the BadFiles.txt to allow the script to be re-run, overwriting previous version

#Making a file of sessions with >=90% "FF" connections (loose wire)
def check_file(filename):
    if("filename" not in filename and ".txt" in filename): # If it's an actual data file
        with open(filename, "r") as read:
            info = {} # Create a dictionary to store FF sessions in
            read.readline() # Read the file without the first line (column names)
            for line in read:
                pieces = line.split(",") # Split the line into columns
                key = pieces[-3] + "," + pieces[-2] + "," + pieces[-1] # Key is Session_date + Session_time + Unit
                if not key in info.keys(): # If the key doesn't already exist, create it
                    info[key] = [0,0]
                info[key][0] = info[key][0] + 1 # Tick up for every data line in the session
                if pieces[4] == "FF": # If the data line has FF connection, tick up
                    info[key][1] = info[key][1] + 1
        with open("../Data/BadFiles.txt", "a") as write:
        #Writes out all unit-sessiondate-sessiontime sets that fulfill the criteria
            for key in info.keys(): # For each unique session
                if(info[key][1] / info[key][0] >= .9): # If >= 90% of data lines have FF connection, write to the file
                    write.write(key)

scan("../Data/dataclean")