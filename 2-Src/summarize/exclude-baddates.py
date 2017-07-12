import pandas as pd

def lookup(s):
    """
    This is an extremely fast approach to datetime parsing.
    For large data, the same dates are often repeated. Rather than
    re-parse these, we store all unique dates, parse them, and
    use a lookup to convert all dates.
    """
    dates = {date:pd.to_datetime(date, format='%Y%m%d') for date in s.unique()}
    return s.map(dates)

#This process eats too much memory - read in chunks
chunksize = 150000
data = []
i = 0
for chunk in pd.read_csv('../Products/summarized.csv',dtype=str,chunksize=chunksize):
    i+=1
    print("chunk #",i)
    data.append(chunk)

    print("concatenate...")
    data = pd.concat(data)
    print("concatenation complete")


##THIS WAS THE ORIGINAL ATTEMPT
#data = pd.read_csv('summarized.csv',dtype=str)
#date in format YYYYMMDD
#file has line as such: "birdid,homeloc,time,date,location\n"

#drop the mistake last column -- take this out if you rerun summarizer after 3 Jun 2017
#print("removing empty column...")
#data = data.drop(data.columns[5], axis=1)
#print("empty column drop complete")

    #change the date column to datetime format
    print("reading datetimes...")
    data['date'] = lookup(data['date'])
    print("datetime read complete")

    #filter out all the bad dates (Year != 2017)
    print("filtering out bad dates...")
    data = data[data['date'].apply(lambda x: x.year == 2017)]
    print("bad dates drop complete")

    #write out this fixed data
    print("filling csv...")
    data.to_csv('../Products/summarized_2017.csv',mode='a',header=False,index=False)
    print("csv fill complete")

    data = [] #make the dataframe blank again