#The purpose of this code is to do minute-by-minute summations of the data.

import os
import datetime

tags={} #start a dictionary of tags
allbird={}
birdinfo={}
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

print(allbird["NA"])

def summarize(detect):
    if tags[detect][0] in summary.keys():
        summary[tags[detect][0]] +=1
    else:
        summary[tags[detect][0]] = 1

#define the filling function for the allbird set
def allfill(bird,group):
    #if group of bird exists in the expgrp dictionary and if bird exists in the group subdictionary
    loc = birdinfo[bird]
    if group in allbird[loc][bird].keys():
        allbird[loc][bird][group] += 1
    else:
        allbird[loc][bird][group] = 1

with open("summarize_1min.csv", "w") as write: #making a summary of all the data
    minute = datetime.timedelta(seconds = 60)
    write.write("bird-id,home-grp,loc,minutes\n")
    for root, dirs, files in os.walk("C:/Users/Natasha/PycharmProjects/PBS_analysis/PBS_Data"): # target folder
        if not files: #if there's nothing in the folder, keep going
            continue
        for path in files:
            group = path.split("_")[0]
            filename = "C:/Users/Natasha/PycharmProjects/PBS_analysis/PBS_Data/" + group + "/" + path
            #if group == "PLAN": #do this only for one group (to test - have to tab out below)
            print(path) #lets us know the program is working
            with open(filename) as data: #open each datafile
                tick = 0
                starttime = 0
                endtime = 0
                summary = {}
                for dataline in data: #for each line in the datafile
                    #tag, time, date
                    line = dataline.strip('\n').split(',')
                    detect = line[0][0:8] #slice out only the tag digits
                    if detect in tags.keys() and len(dataline) == 31: #take only full datalines with real tag ids
                        time = datetime.datetime.strptime(line[1], '%H:%M:%S').time()
                        if tick == 0:
                            starttime = time
                            endtime = (datetime.datetime.combine(datetime.date.today(), starttime) + minute).time()
                            summarize(detect)
                            tick = 1
                        elif endtime >= time:
                            summarize(detect)
                        elif endtime < time:
                            starttime = time
                            endtime = (datetime.datetime.combine(datetime.date.today(), starttime) + minute).time()
                            for bird in summary.keys():
                                if summary[bird] == 30: #if the bird is detected for a full minute
                                    allfill(bird,group)
                            summary = {}
    for home in allbird.keys():
        for bird in allbird[home].keys():
            for loc in allbird[home][bird].keys():
                write.write(bird + ',' + home + ',' + loc + ',' + str(allbird[home][bird][loc]) + '\n')



