from sklearn.linear_model import LinearRegression
import pandas
import csv
import numpy as np 
import os
from math import floor 

threshold = 0.586366150792

pth1= 'D:\\study\\major project\\scl\\preprocessed\\pitchdata'
pth2 = 'D:\\study\\major project\\scl\\preprocessed\\metadata'
os.chdir(pth1)
X = np.array([0]*24)
Y = np.array([0.0])
cnt=1
with open("D:\\study\\major project\\scl\\src\\statistics.csv", "w", newline='') as mcsv:
    with open("D:\\study\\major project\\scl\\src\\fLR.txt", "w") as fLR:
        for fname in os.listdir():
            with open(pth2+"\\"+fname, newline='') as csvf:
                reader = csv.DictReader(csvf)
                for row in reader:
                    #Y_i =  floor(float(row['song_hotttnesss'])*10)/10
                    Y_i = float(row['song_hotttnesss'])
            pitch = np.array([ [] for i in range(12) ])
            with open(fname, newline='') as csvf:
                reader = csv.DictReader(csvf)
                for row in reader:
                    pitch = np.hstack([pitch, [[float(row['st{}'.format(i)])] for i in range(12)] ] )
            X_i = []
            for i in range(12):
                X_i += [np.mean(pitch[i], dtype=np.float64), np.var(pitch[i], dtype=np.float64)]
            writer = csv.writer(mcsv, delimiter = ",")
            tmp = X_i + [1 if Y_i>threshold else 0]
            writer.writerow(tmp)

            #X = np.vstack([X, X_i])
            #Y = np.append(Y, Y_i)
            #fLR.write("{} {} ".format(cnt, fname) + " ".join([str(vl) for vl in X_i ]) + " {}".format(Y_i) +"\n" )
            #cnt+=1
        

    #clf = LinearRegression()
    #clf.fit(X, Y)
    #fLR.write( "\n\naccuracy = {}".format(clf.score(X, Y)) )
