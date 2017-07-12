#This script copies renames the PBS files to include their location in the title.
#Only dataloc (the data source) and newroot (the renamed data location) should be changed.

import os
from shutil import copyfile

#copyfile(src, dst) is used to make a copy of the file

dataloc = "G:/PBS_Data" #data source
newroot = "C:/Users/Natasha/PycharmProjects/PBS_analysis/PBS_Data" #new location

i=0
for root, dirs, files in os.walk(dataloc): #pulls the file names from the entire data source folder
    if not files:
        continue
    #pulls the folder name of the data - this is group name
    prefix = os.path.basename(root)
    #runs through the list of files produced above, and copies them with a new name to the data location
    for f in files:
        i+=1
        loc = newroot + "/" + prefix
        try:
            copyfile(os.path.join(root, f), os.path.join(loc, "{}_{}".format(prefix, f)))
            if i % 100 == 0: #when i is divisible by 100, aka every 100 files
                print(os.path.join(loc, "{}_{}".format(prefix, f)))
        except FileNotFoundError:
            print(os.path.join(root,f) + " does not exist")


