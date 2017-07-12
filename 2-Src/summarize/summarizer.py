import os
import datetime

tags={} #start a dictionary of tags
allbird = {} #start a dictionary for all the birds
with open("../Data/TagIDs.csv", "r") as tagids:
    #TAG,DATE,GROUP,BIRD,SEX,STATUS,LR,UR,LL,UL,
    for line in tagids:
        tag = line.strip('\n').replace(' ','').split(',')[0] #take the tag number without any spaces
        bird = line.strip('\n').split(',')[3] #pull the bird id
        loc = line.strip('\n').split(',')[2] #pull the location of the bird
    #print(taglist) #has junk right now, like header (oops) and SOPB tags, but who cares, it does no harm
        tags[tag] = [bird, loc] #make a dictionary of tags with associated bird and home location
        try: #build the allbird dictionary
            allbird[loc][bird] = {}
        except KeyError:
            allbird[loc] = {}
            allbird[loc][bird] = {}

expgrp = {} #start a dictionary to pull recently active tags for the experiment
#define function for filling the expgrp dict
def expfill(detect):
    #if group exists in the expgrp dictionary and if bird exists in the group subdictionary
    keys = expgrp.keys()
    if tags[detect][1] in keys and tags[detect][0] in expgrp[tags[detect][1]].keys():
        expgrp[tags[detect][1]][tags[detect][0]] += 1 #add a tick to the bird
    #else if group exists (but bird does not)
    elif tags[detect][1] in keys:
        expgrp[tags[detect][1]][tags[detect][0]] = 1 #start the bird off with 1 tick
    #else if group does not exist
    else:
        expgrp[tags[detect][1]] = {} #create the group subdictionary
        expgrp[tags[detect][1]][tags[detect][0]] = 1 #start the bird off with 1 tick

#define the filling function for the allbird set
def allfill(detect,group):
    #if group of bird exists in the expgrp dictionary and if bird exists in the group subdictionary
    loc = tags[detect][1]
    bird = tags[detect][0]
    if group in allbird[loc][bird].keys():
        allbird[loc][bird][group] += 1
    else:
        allbird[loc][bird][group] = 1

mystery = {} #start a dictionary for strange tags
def mysfill(detect):
    try: #try adding one to the detection
        mystery[detect] += 1
    except: #if you can't, make the detection
        mystery[detect] = 1

with open("../Products/summarized.csv", "w") as write: #making a summary of all the data
    write.write("birdid,homeloc,time,date,location\n")
    for root, dirs, files in os.walk("C:/Users/Natasha/PycharmProjects/PBS_analysis/PBS_Data"): # target folder
        if not files: #if there's nothing in the folder, keep going
            continue
        for path in files:
            group = path.split("_")[0]
            filename = "C:/Users/Natasha/PycharmProjects/PBS_analysis/PBS_Data/" + group + "/" + path
            #if group == "PLAN": #do this only for one group (to test - have to tab out below)
            print(path) #lets us know the program is working
            with open(filename) as data: #open each datafile
                for dataline in data: #for each line in the datafile
                    #tag, time, date
                    line = dataline.strip('\n').split(',')
                    detect = line[0][0:8] #slice out only the tag digits
                    if detect in tags.keys() and len(dataline) == 31: #take only full datalines with real tag ids
                        date = datetime.datetime.strptime(line[2],'%Y %b %d').strftime('%Y%m%d')
                        #writing bird, time, date, location
                        write.write(tags[detect][0] + "," + tags[detect][1] + ',' + line[1] + "," + date + "," + group + "\n")
                        allfill(detect,group)
                        if line[2][0:8] == "2017 May": #pull subset of detections
                            expfill(detect)
                    if detect not in tags.keys() and len(dataline) == 31: #any garbage data
                        mysfill(detect)

with open("../Products/expgrp.csv", "w") as write: #write a file of all the detections
    write.write("group,bird-id,detections\n") #write a header line
    for group in expgrp.keys():
        for bird in expgrp[group].keys():
            if expgrp[group][bird] >= 100: #drop any scattered / maybe random false detections
                write.write(group + "," + bird + "," + str(expgrp[group][bird]) + "\n") #write out the dict info

with open("../Products/mystery-tags.csv", "w") as write: #write a file of the mysteries
    write.write("tag,detections\n") #write a header line
    for tag in mystery.keys():
        if mystery[tag] >= 10000: #any tags that don't appear to be real
            write.write(tag + ',' + str(mystery[tag]) + '\n')

with open("../Products/bird-summary.csv", "w") as write: #write a file of the allbirds file
    write.write('group,bird-id,location,detections\n') #write a header line
    for group in allbird.keys():
        for bird in allbird[group].keys():
            for loc in allbird[group][bird].keys():
                write.write(group + ',' + bird + ',' + loc + ',' + str(allbird[group][bird][loc]) + '\n')
