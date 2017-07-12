#the purpose of this script is to determine which locations get more detections
#there might be an altitudinal issue or something like that?

import os
import datetime

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
def datefill(group,date):
    if path[-20:-18] == "17":
        if group in dates.keys():
            if date > dates[group][1]:
                dates[group][1] = date
        else:
            dates[group] = [date,date]

summary = {}
def sumfill(group,detect):
    if group in summary.keys():
        if detect in tags.keys() and tags[detect][1] != "Field Tag":
            summary[group][0] += 1
        else:
            summary[group][1] += 1
    else:
        if detect in tags.keys() and tags[detect][1] != "Field Tag":
            summary[group] = [1,0]
        else:
            summary[group] = [0,1]

with open("summarized_loc.csv", "w") as write: #making a summary of all the data
    write.write("loc,good-prop,bab-prop\n") #header line
    for root, dirs, files in os.walk("C:/Users/Natasha/PycharmProjects/PBS_analysis/PBS_Data"): # target folder
        if not files: #if there's nothing in the folder, keep going
            continue
        for path in files:
            group = path.split("_")[0]
            filename = "C:/Users/Natasha/PycharmProjects/PBS_analysis/PBS_Data/" + group + "/" + path
            try:
                date = datetime.datetime.strptime(path.split("_")[1][1:9],"%y-%m-%d") #attempt to parse the date of the file
            except ValueError:
                pass
            datefill(group,date)
            #if group == "PLAN": #do this only for one group (to test - have to tab out below)
            print(path) #lets us know the program is working
            if path[-20:-18] == "17": #if the year in the filename is 2017
                with open(filename) as data: #open each datafile
                    for dataline in data: #for each line in the datafile
                    #tag, time, date
                        line = dataline.strip('\n').split(',')
                        detect = line[0][0:8] #slice out only the tag digits
                        if len(dataline) == 31: #take only full datalines
                            sumfill(group,detect)
    for loc in summary.keys():
        poss = (dates[loc][1]-dates[loc][0]).total_seconds() / 3.5 #number of possible detections if a single tag is going
        if poss > 0:
            good = round(summary[loc][0] / poss,3)
            bad = round(summary[loc][1] / poss,3)
            write.write(loc + ',' + str(good) + ',' + str(bad) + '\n')

