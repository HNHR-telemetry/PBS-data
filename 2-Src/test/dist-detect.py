#This script:
#   1. Pulls only detections from fixed-date groups
#   2. Builds a proportion of time the station was active
#   3. Corrects for the proportion of time the station is active
#   4. Shows the distance between the field tag and the stations detected at

import os
import datetime
import pandas as pd

#load in a csv of the distances between all the groups - using as casual shorthand for BS distances
dists = pd.read_csv('dist_matrix.csv', index_col=0)

tags={} #start a dictionary of tags
with open("TagIDs.csv", "r") as tagids:
    #TAG,DATE,GROUP,BIRD,SEX,STATUS,LR,UR,LL,UL,
    for line in tagids:
        tag = line.strip('\n').replace(' ','').split(',')[0] #take the tag number without any spaces
        bird = line.strip('\n').split(',')[3] #pull the bird id
        loc = line.strip('\n').split(',')[2] #pull the location of the bird
    #print(taglist) #has junk right now, like header (oops) and SOPB tags, but who cares, it does no harm
        tags[tag] = [bird, loc] #make a dictionary of tags with associated bird and home location

dates = {}
def datefill(group,date): #fills in the dates of when the BS started getting data and last datafile
    if path[-20:-18] == "17":
        if group in dates.keys():
            if date > dates[group][1]:
                dates[group][1] = date
        else:
            dates[group] = [date,date]

field = {}
def fieldfill(detect,loc): #fill in the dictionary of groups at which each field tag was detected
    if detect == "4B33524C" or detect == "55554B33": #take only full datalines with field tags
        group = tags[detect][1]
        if group in field.keys() and loc in field[group].keys():
            field[group][loc] += 1
        elif group in field.keys():
            field[group][loc] = 1
        else:
            field[group] = {}
            field[group][loc] = 1

for root, dirs, files in os.walk("C:/Users/Natasha/PycharmProjects/PBS_analysis/PBS_Data"): # target folder
    if not files: #if there's nothing in the folder, keep going
        continue
    for path in files:
        loc = path.split("_")[0]
        filename = "C:/Users/Natasha/PycharmProjects/PBS_analysis/PBS_Data/" + loc + "/" + path
        try:
            date = datetime.datetime.strptime(path.split("_")[1][1:9],"%y-%m-%d") #attempt to parse the date of the file
        except ValueError:
            pass
        datefill(loc,date)
        #if loc == "SHW": #do this only for one group (to test - have to tab out below)
        print(path) #lets us know the program is working
        if path[-20:-18] == "17" and path[-17:-15] == "05": #if the year in the filename is 2017 & month is May
            with open(filename) as data: #open each datafile
                for dataline in data: #for each line in the datafile
                #tag, time, date
                    line = dataline.strip('\n').split(',')
                    detect = line[0][0:8] #slice out only the tag digits
                    if len(dataline) == 31 and detect in tags.keys(): #only detections of actual tags
                        fieldfill(detect,loc) #fill the dictionary of field[group][BS-location] = pings


with open("field-tag_dists.csv", "w") as write: #pulling the data from just the field tags
    write.write("group,location,dist,proportion\n")
    for group in field.keys(): #for each group a field tag is at
        for loc in field[group].keys(): #for each location the field tag was detected at
            poss = (dates[loc][1]-dates[loc][0]).total_seconds() / 3.5 #rough number of possible detections if a single tag is going
            dist = round(dists.at[group,loc],1) #pull the distance between the group and the BS location
            if poss > 0: #if the BS had >1 day of data
                pings = round(field[group][loc] / poss,3)
                write.write(str(group) + ',' + str(loc) + ',' + str(dist) + ',' + str(pings) + '\n')


