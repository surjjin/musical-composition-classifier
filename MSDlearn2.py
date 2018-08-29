from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
import pandas
import csv
import numpy as np 
import os
from math import floor

threshold = 0.586366150792

pth1= 'D:\\study\\major project\\scl\\preprocessed\\pitchdata'
pth2 = 'D:\\study\\major project\\scl\\preprocessed\\metadata'
os.chdir(pth1)
X = np.array([0]*1200)
Y = np.array([0])

with open("D:\\study\\major project\\scl\\src\\modNGram.txt", 'w') as modNGram:
    cnt=1
    for fname in os.listdir():
        with open(pth2+"\\"+fname, newline='') as csvf:
            reader = csv.DictReader(csvf)
            for row in reader:
                if float(row['song_hotttnesss']) > threshold:
                    Y = np.append(Y, [1])
                else:
                    Y = np.append(Y, [0])
        pitch = np.array([ [] for i in range(12) ])
        with open(fname, newline='') as csvf:
            reader = csv.DictReader(csvf)
            for row in reader:
                pitch = np.hstack([pitch, [[float(row['st{}'.format(i)])] for i in range(12)] ] )
        X_i, lp = [0]*1200, len(pitch[0])
        for i in range(12):
            for j in range(1, lp):
                if pitch[i][j]>0.99:
                    pitch[i][j] = 0.99
                if pitch[i][j-1]>0.99:
                    pitch[i][j-1] = 0.99
                X_i[i*100 + floor(pitch[i][j]*10)*10 + floor(pitch[i][j-1]*10)] += 1
        modNGram.write("processed {}/4214\n".format(cnt))
        cnt+=1
        print(cnt)
        X = np.vstack([X, X_i])
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
    clf = GaussianNB()
    clf.fit(X_train, Y_train)
    modNGram.write("\n\n Gaussian NB accuracy: {}".format(clf.score(X_test, Y_test)) )

    clf2 = LogisticRegression()
    clf2.fit(X_train, Y_train)
    modNGram.write("\n\n LogisticRegression accuracy: {}".format(clf2.score(X_test, Y_test)) )