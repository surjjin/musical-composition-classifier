from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
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
Y = np.array([0])
cnt=1
with open("D:\\study\\major project\\scl\\src\\fLR.txt", "w") as fLR:
    for fname in os.listdir():
        with open(pth2+"\\"+fname, newline='') as csvf:
            reader = csv.DictReader(csvf)
            for row in reader:
                if float(row['song_hotttnesss']) > threshold:
                    Y_i = [1]
                else:
                    Y_i = [0]
        pitch = np.array([ [] for i in range(12) ])
        with open(fname, newline='') as csvf:
            reader = csv.DictReader(csvf)
            for row in reader:
                pitch = np.hstack([pitch, [[float(row['st{}'.format(i)])] for i in range(12)] ] )
        X_i = []
        for i in range(12):
            X_i += [np.mean(pitch[i], dtype=np.float64), np.var(pitch[i], dtype=np.float64)]
        X = np.vstack([X, X_i])
        Y = np.append(Y, Y_i)
        fLR.write("{} {} ".format(cnt, fname) + " ".join([str(vl) for vl in X_i ]) + " {}".format(Y_i) +"\n" )
        cnt+=1
        print(cnt)
    X_test=[]
    X_train=[]
    Y_train=[]
    Y_test=[]
    i=0
    for label in Y:
        if i<3500:
            Y_train.append(label)
        else:
            Y_test.append(label)
        i+=1
    i=0
    for row in X:
        if i<3500:
            X_train.append(row)
        else:
            X_test.append(row)
        i+=1
    clf = RandomForestClassifier(n_estimators=30)
    clf.fit(X_train, Y_train)
    fLR.write( "\n\naccuracy = {}".format(clf.score(X_test, Y_test)) )
