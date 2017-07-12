#This script will:
#   1. summarize each minute, so that we have # detections per minute by location
#   2. compare minutes for each birdid
#   3. assign the birdid to a location based on what had the most detections for 2+ locations detected
#   4. render no assignment for birds detected at one location at <80% detected

import pandas as pd

#Read in the field tag data, then label the columns
#file has line as such: "birdid,homeloc,time,date,location\n"
data = pd.read_csv("fieldtag-data.csv",header=None)
data.columns = ['id','group','time','date','loc']

#Make a column of just the minutes and hour
data['min'] = data['time'].apply(lambda x: x[3:5])
data['hour'] = data['time'].apply(lambda x: x[0:2])

#count the number of detections for each tag, by location and datetime
grouped = data.groupby(['group','id','date','hour','min','loc']).count()
#this turns the column 'time' into the count of time

#turn the groupby object back into a dataframe
grouped = grouped.reset_index()

#drop any row with <25 detections
grouped = grouped[grouped['time'].apply(lambda x: x >= 25)]

#group by everything but loc & time
groupy = grouped.groupby(['group','id','date','hour','min'])

#pull the index of the maximum value rows for each group-id-date-min combination
idx = groupy.apply(lambda x: x['time'].idxmax())
idx = idx.reset_index()[0]

#pull the rows of maximums
maxes = grouped.ix[idx]

###Now we have to do a second filter - we will clear out any locations not assigned
###for more than 15 minutes per hour

#look at this by hour now
hours = maxes.groupby(['group','date','hour','loc']).count()
hourly = hours[hours['id'].apply(lambda x: x>=15)]

print(hourly)

#count the number of minutes assigned to each location each day
maxes = maxes.groupby(['group','date','loc']).count()
#remove any locations not detected for an hour each day
daily = maxes[maxes['id'].apply(lambda x: x >= 60)]


###STACK EXCHANGE CODE. DOES NOT WORK CORRECTLY AS FAR AS I CAN TELL
#pull the maximum value for each minute
#idx = grouped.groupby(['loc'])['time'].transform(max) == grouped['time']
#maxes = grouped[idx]
#maxes = maxes[maxes['time'] > 200]
#print(maxes)









