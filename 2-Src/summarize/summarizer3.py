#The purpose of this script is to summarize the data using a 15-minute frame - each file.
#In order for a detection to be accepted, it must exist at >90% of the file

import os

tags={} #start a dictionary of tags
birdinfo={} #bird - group dictionary
allbird = {} #start a dictionary for all the birds
with open("TagIDs.csv", "r") as tagids:
    #TAG,DATE,GROUP,BIRD,SEX,STATUS,LR,UR,LL,UL,
    for line in tagids:
        tag = line.strip('\n').replace(' ','').split(',')[0] #take the tag number without any spaces
        bird = line.strip('\n').split(',')[3] #pull the bird id
        loc = line.strip('\n').split(',')[2] #pull the location of the bird
    #print(taglist) #has junk right now, like header (oops) and SOPB tags, but who cares, it does no harm
        tags[tag] = [bird, loc] #make a dictionary of tags with associated bird and home location
        birdinfo[bird] = loc
        try: #build the allbird dictionary
            allbird[loc][bird] = {}
        except KeyError:
            allbird[loc] = {}
            allbird[loc][bird] = {}

#define the filling function for the allbird set
def allfill(bird,group):
    #if group of bird exists in the expgrp dictionary and if bird exists in the group subdictionary
    loc = birdinfo[bird]
    if group in allbird[loc][bird].keys():
        allbird[loc][bird][group] += 1
    else:
        allbird[loc][bird][group] = 1

with open("summarized_15min.csv", "w") as write: #making a summary of all the data
    write.write("bird-id,home-grp,loc,15minblocks\n")
    for root, dirs, files in os.walk("C:/Users/Natasha/PycharmProjects/PBS_analysis/PBS_Data"): # target folder
        if not files: #if there's nothing in the folder, keep going
            continue
        for path in files:
            group = path.split("_")[0]
            filename = "C:/Users/Natasha/PycharmProjects/PBS_analysis/PBS_Data/" + group + "/" + path
            #if group == "PLAN": #do this only for one group (to test - have to tab out below)
            print(path) #lets us know the program is working
            with open(filename) as data: #open each datafile
                summary = {}
                for dataline in data: #for each line of the data
                    #tag, time, date <- the order of the line
                    line = dataline.strip('\n').split(',')
                    detect = line[0][0:8] #slice out only the tag digits
                    if detect in tags.keys() and len(dataline) == 31: #take only full datalines with real tag ids
                        if tags[detect][0] in summary.keys():
                            summary[tags[detect][0]] +=1
                        else:
                            summary[tags[detect][0]] = 1
                for bird in summary.keys():
                    if summary[bird] >= 405: #if the number of detections in the 15 minutes is 90% of the possible
                        allfill(bird,group)
    for home in allbird.keys():
        for bird in allbird[home].keys():
            for loc in allbird[home][bird].keys():
                write.write(bird + ',' + home + ',' + loc + ',' + str(allbird[home][bird][loc]) + '\n')


