
with open("summarize_1min.csv") as data:
    with open("slim_1min.csv", "w") as write:
        data.readline()
        for dataline in data:
            line = dataline.strip('\n').split(',')
            if int(line[3]) > 15: #clears out any locations where the tag was not detected for 15 1 min periods
                write.write(dataline)