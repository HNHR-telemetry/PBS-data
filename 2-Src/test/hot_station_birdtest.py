#The purpose of this script is to use real data from a low-lying group (LOLF)
# in order to see if detections are proportionate according to expected proportions,
# or if high-altitude stations are hotter than expected.

from collections import defaultdict

#dictionary is base station id > date > num detections
bs = {}
def bsfill(birdid,bsid,date):
    if birdid == "4889" or birdid == "5679":
        if bsid not in bs.keys():
            bs[bsid] = defaultdict(int)
            bs[bsid][date] += 1
        else:
            bs[bsid][date] += 1

#Use the already cleaned data with real detections
i = 0
with open('../Products/summarized_2017.csv','r') as file:
    with open('../Products/hot_station_LOLFreport.csv', 'w') as write:
        for line in file:
            #line looks like 'FieldTag1,1500,09:07:10,2017-04-11,MLF2\n'
            data = line.strip('\n').split(',')
            i += 1
            datebits = data[3].split('-')
                #if the date is between May 11 - 20
            if datebits[1] == '05' and 10 < int(datebits[2]) < 21:
                bsfill(data[0],data[4],data[3])
            if i % 1000 == 0: #lets us know the code is running by printing the dataline every 1000 lines
                print(data)
        for bsid in bs.keys():
            count = 0
            for date in bs[bsid].keys():
                count += bs[bsid][date]
            daily = count / len(bs[bsid])
            write.write(bsid + ',' + str(daily) + '\n')

