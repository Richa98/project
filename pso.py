# -*- coding: utf-8 -*-

from random import random
from math import sin,cos
def f6(param):
    para = param*10
    num = (sin(para) *cos(para)) - 0.5
    denom = (1.0 + 0.001 * ((para * para))) * (1.0 + 0.001 * ((para * para)))
    f6 =  0.5 - (num/denom)
    errorf6 = 1 - f6
    return f6, errorf6;

import pandas as pd

#Importing dataset
dataset=pd.read_csv('data_new.csv')

#Creating Matrix of Dependent Variable
X=dataset.iloc[:, :-1].values

#Dependent Variable Vector
Y=dataset.iloc[:,-1].values

#Splitting dataset into Trainig set and Test set
from sklearn.model_selection import train_test_split
X_train,X_test,Y_train,Y_test=train_test_split(X,Y,train_size=0.75,random_state=0)


#Encoding Categorical data
from sklearn.preprocessing import LabelEncoder
labelencoder_X=LabelEncoder()

for i in range(0,30):
    X_train[:, i]=labelencoder_X.fit_transform(X_train[:, i].astype(str))
    X_test[:, i]=labelencoder_X.fit_transform(X_test[:, i].astype(str))

c1=2
c2=2  
for i in range(30):
    pbest = X_train[0][i]
    gbest = 0
    co = 0
    for j in range(len(X_train)):
        gbest+= X_train[j][i]
        co+=1
        a,b=f6(X_train[j][i])
        if a>pbest:
            pbest=a
          
    gbest/=(1.0*co)
    #print(pbest,gbest)
    for j in range(len(X_train)):
        a = X_train[j][i] + c1 * random() * (pbest- X_train[j][i]) + c2 * random() * (gbest - X_train[j][i])
        X_train[j][i] = a + X_train[j][i]
        print(X_train[j][i])

c1=2
c2=2  
for i in range(30):
    pbest = X_test[0][i]
    gbest = 0
    co = 0
    for j in range(len(X_test)):
        gbest+= X_test[j][i]
        co+=1
        a,b=f6(X_test[j][i])
        if a>pbest:
            pbest=a
          
    gbest/=(1.0*co)
    #print(pbest,gbest)
    for j in range(len(X_test)):
        a = X_test[j][i] + c1 * random() * (pbest- X_test[j][i]) + c2 * random() * (gbest - X_test[j][i])
        X_test[j][i] = a + X_test[j][i]
        #print(X_test[j][i])

#print(X_train)

#Feature Scaling 
from sklearn.preprocessing import StandardScaler
sc_X=StandardScaler()
X_train=sc_X.fit_transform(X_train)
X_test=sc_X.transform(X_test)

#Fitting the SVM Classifier to the Training set
from sklearn.svm import SVC
classifier=SVC(kernel='rbf',random_state=0)
classifier.fit(X_train,Y_train)

#Predicting the test set result
Y_pred=classifier.predict(X_test)

#Creating the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm=confusion_matrix(Y_test,Y_pred)


