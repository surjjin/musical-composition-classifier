# to find third quartile for song_hotttnesss in msd

import os
import pandas
import sys
import numpy 
import csv

pth= 'D:\\study\\major project\\scl\\preprocessed\\metadata'
pth1 = 'D:\\study\\major project\\scl\\preprocessed\\pitchdata'

os.chdir(pth)
x = numpy.array([])
ct, remove = 0, []
for fname in os.listdir():
    ct+=1
    with open(fname, newline='') as csvf:
        reader = csv.DictReader(csvf)
        for row in reader:
            tmp = row['song_hotttnesss']
            if tmp=='nan':
                remove += [fname]
            else:
                x = numpy.append(x, [float(tmp)])

#print(remove)
for fname in remove:
    os.remove(pth+"\\"+fname)
    os.remove(pth1+'\\'+fname)
x=numpy.nan_to_num(x)

q3 = numpy.percentile(x, 75)
print(q3)

# Q3 = 0.586366150792