from collections import defaultdict

#dictionary is base station id > date > num detections
bs = {}
def bsfill(birdid,bsid,date):
    if len(birdid) == 4:
        if bsid not in bs.keys():
            bs[bsid] = defaultdict(int)
            bs[bsid][date] += 1
        else:
            bs[bsid][date] += 1

#dictionary is bird id > date > num detections
bird = {}
def birdfill(birdid,date):
    if len(birdid) == 4:
        if birdid not in bird.keys():
            bird[birdid] = defaultdict(int)
            bird[birdid][date] += 1
        else:
            bird[birdid][date] += 1

i = 0

#this script uses the summarized data with only real detections
with open('../Products/summarized_2017.csv','r') as file:
    with open('../Products/hot_station_birdreport.csv', 'w') as write:
        with open('../Products/hot_station_summaryreport.csv', 'w') as write2:
            file.readline()
            for line in file:
                #line looks like 'FieldTag1,1500,09:07:10,2017-04-11,MLF2\n'
                data = line.strip('\n').split(',')
                i += 1
                datebits = data[3].split('-')
                    #if the date is between April 21 - 30
                if datebits[1] == '05' and int(datebits[2]) > 20:
                    bsfill(data[0],data[4],data[3])
                    birdfill(data[0],data[3])
                    if i % 500 == 0:
                        print(data)
            #for bsid in bs.keys():
            #    for date in bs[bsid].keys():
            #        write.write(bsid + ',' + date + ',' + str(bs[bsid][date]) + '\n')
            for birdid in bird.keys():
                count = 0
                for date in bird[birdid].keys():
                    count += bird[birdid][date]
                write.write(birdid + ',' + str(count) + '\n')
            for bsid in bs.keys():
                count = 0
                for date in bs[bsid].keys():
                    count += bs[bsid][date]
                daily = count / len(bs[bsid])
                write2.write(bsid + ',' + str(daily) + '\n')

