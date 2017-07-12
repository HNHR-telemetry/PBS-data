import pandas
import scipy.spatial

df = pandas.read_csv("../Data/terr_locs.txt")
frames = [df["EASTING"],df["NORTHING"]]
names = df["GCODE"]
a = pandas.concat(frames, axis=1)
b = a

dist = scipy.spatial.distance.cdist(a,b)
df = pandas.DataFrame(dist, index=names, columns=names)

df.to_csv('../Data/dist_matrix.csv', index=True, header=True, sep=',')