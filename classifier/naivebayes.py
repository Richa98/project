# -*- coding: utf-8 -*-


import pandas as pd

#Importing dataset
dataset=pd.read_csv('data.csv')

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

#Feature Scaling 
from sklearn.preprocessing import StandardScaler
sc_X=StandardScaler()
X_train=sc_X.fit_transform(X_train)
X_test=sc_X.transform(X_test)

#Fitting the Naive Bayes Classifier to the Training set
from sklearn.naive_bayes import GaussianNB
classifier=GaussianNB()
classifier.fit(X_test,Y_test)

#Predicting the test set result
Y_pred=classifier.predict(X_test)

#Creating the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm=confusion_matrix(Y_test,Y_pred)

print(Y_test)
print(Y_pred)
print(cm)
accuracy=(cm[0][0]+cm[1][1])/(cm[0][0]+cm[1][1]+cm[0][1]+cm[1][0])*100
print(accuracy)
