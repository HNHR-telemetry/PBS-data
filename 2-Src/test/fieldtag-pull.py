i = 0

with open("summarized_2017.csv") as file:
    with open("fieldtag-data.csv", 'w') as write:
        for line in file:
            #line looks like 'Walk Tag,09:07:10,2017 Apr 11,1500\n'
            data = line.strip('\n').split(',')
            i += 1
            if data[0][0:5] == 'Field':
                write.write(line)
                if i % 500 == 0:
                    print(data)