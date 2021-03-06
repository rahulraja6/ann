# -*- coding: utf-8 -*-

# Classification template

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the dataset
dataset = pd.read_csv('Churn_Modelling.csv')
X = dataset.iloc[:, 3 : 13].values
y = dataset.iloc[:, 13].values

# Encoding categorical data
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
labelencoder_X_1 = LabelEncoder()
X[:, 1] = labelencoder_X_1.fit_transform(X[:, 1])
labelencoder_X_2 = LabelEncoder()
X[:, 2] = labelencoder_X_2.fit_transform(X[:, 2])
onehotencoder = OneHotEncoder(categorical_features = [1])
X = onehotencoder.fit_transform(X).toarray()
X=X[:, 1:]

#Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

#import keras libraray
#import keras
#from keras.models import Sequential
#from keras.layers import Dense
#from keras.layers import Dropout
##initializing ANN
#classifier=Sequential()
#classifier.add(Dense(activation="relu", input_dim=11, units=6, kernel_initializer="uniform"))
#classifier.add(Dropout(p=0.1))
#classifier.add(Dense(activation="relu", units=6, kernel_initializer="uniform"))
#classifier.add(Dropout(p=0.1))
#
##Output Layer
#classifier.add(Dense(activation="sigmoid", units=1, kernel_initializer="uniform"))
##Compile
#classifier.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])
#
## Fitting classifier to the Training set
#classifier.fit(x=X_train,y=y_train,batch_size=10,epochs=100)
## Create your classifier here
#
## Predicting the Test set results
#y_pred = classifier.predict(X_test)
#
## Making the Confusion Matrix
#y_pred=(y_pred>0.5)
##Single Prediction
#new_prediction=classifier.predict(sc.transform(np.array[[0,0,600.0,1,40,3,60000,2,1,1,50000]]))
#new_prediction=(new_prediction>0.5)
#
#from sklearn.metrics import confusion_matrix
#cm = confusion_matrix(y_test, y_pred)

from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import cross_val_score
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
def build_classifier(): 
   classifier=Sequential()
   classifier.add(Dense(activation="relu", input_dim=11, units=6, kernel_initializer="uniform"))
   classifier.add(Dropout(p=0.2))
   classifier.add(Dense(activation="relu", units=6, kernel_initializer="uniform"))
   classifier.add(Dropout(p=0.2))
   classifier.add(Dense(activation="sigmoid", units=1, kernel_initializer="uniform"))
   classifier.compile(optimizer='rmsprop',loss='binary_crossentropy',metrics=['accuracy'])
   return classifier
classifier=KerasClassifier(build_fn=build_classifier,batch_size=175,epochs=350)
accuracies=cross_val_score(estimator=classifier,X=X_train,y=y_train,cv=10,n_jobs=1)
mean=accuracies.mean()
variance=accuracies.std()

#Tuning ANN
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import GridSearchCV
from keras.models import Sequential
from keras.layers import Dense

#Building a Classifier
def build_classifier(optimizer): 
   classifier=Sequential()
   classifier.add(Dense(activation="relu", input_dim=11, units=6, kernel_initializer="uniform"))
   classifier.add(Dense(activation="relu", units=6, kernel_initializer="uniform"))
   classifier.add(Dense(activation="sigmoid", units=1, kernel_initializer="uniform"))
   classifier.compile(optimizer=optimizer,loss='binary_crossentropy',metrics=['accuracy'])
   return classifier
classifier=KerasClassifier(build_fn=build_classifier)
#parameters={'batch_size':[25,32],'epochs'3100,500],'optimizer':['adam','rmsprop']}
parameters={'batch_size':[175],'epochs':[500,350],'optimizer':['rmsprop']}
grid_search=GridSearchCV(estimator=classifier,param_grid=parameters,scoring='accuracy',cv=10)
grid_search=grid_search.fit(X_train,y_train)
best_parameters=grid_search.best_params_
best_accuracy=grid_search.best_score_