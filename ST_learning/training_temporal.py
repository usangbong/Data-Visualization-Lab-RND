from flask import Flask, render_template,flash,request
import json
from minepy import MINE

import numpy as np
np.set_printoptions(suppress=True)
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import mean_squared_error,r2_score
from sklearn.preprocessing import MinMaxScaler
from scipy.stats import iqr
import os
from os import listdir
from os.path import isfile, join
from collections import Counter
import itertools

from keras.callbacks import EarlyStopping
from keras.models import load_model
from keras.models import Sequential
from keras.models import Model
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import GRU
from keras.layers import Dropout
from keras.layers import Input
from keras.layers import RepeatVector
from keras.layers import TimeDistributed
from keras.layers import Activation
from keras.layers import Flatten,Reshape, BatchNormalization
from keras.layers.merge import concatenate
#import import_ipynb
#import libs

'''location=pd.read_csv('data/location_seoul3_345.csv')
location['no'] = location['no'].astype(str)
onlyfiles=location['no'].values
onlyfiles.sort()'''

n_in=24
my_path="data/npy/24/"
my_model_path="model/lstm/24/model"

X_train=np.load(my_path+"X_train.npy")
Y_train=np.load(my_path+"Y_train.npy")[:,0,:,:]
X_val=np.load(my_path+"X_val.npy")
Y_val=np.load(my_path+"Y_val.npy")[:,0,:,:]

X_train=np.mean(X_train,axis=2)
Y_train=np.mean(Y_train,axis=1)
X_val=np.mean(X_val,axis=2)
Y_val=np.mean(Y_val,axis=1)
'''
X_train=X_train.transpose((0,2,1,3)).reshape((-1,n_in,5))
X_val=X_val.transpose((0,2,1,3)).reshape((-1,n_in,5))
Y_train=Y_train.reshape((-1,5))
Y_val=Y_val.reshape((-1,5))
'''



n_steps_in=X_train.shape[1]
n_features=X_train.shape[2]

#sc = MinMaxScaler(feature_range = (0, 1))
#X_train = sc.fit_transform(X_train.reshape((-1,n_features))).reshape((-1,n_steps_in,n_features))
#Y_train =sc.transform(Y_train)

#sc_val= MinMaxScaler(feature_range = (0, 1))
#X_val=sc_val.fit_transform(X_val.reshape((-1,n_features))).reshape((-1,n_steps_in,n_features))
#Y_val=sc_val.transform(Y_val)

idx=[]
for i in range(1,6):
    idx=idx+list(itertools.combinations(list(range(5)), i))
k=int(input())
idx=idx[k]#[(0,)+idx[k]]
n_features=len(idx)

X_train=X_train[:,:,idx];X_val=X_val[:,:,idx]

model = Sequential()
model.add(LSTM(128, activation='relu',input_shape=(n_steps_in, n_features), return_sequences=True))
model.add(LSTM(128, activation='relu', return_sequences=False))
model.add(Dense(1))
#X_train.shape,Y_train.shape, np.min(X_train),np.max(X_train),np.min(Y_train),np.max(Y_train)

model.compile(loss='mse', optimizer='rmsprop')
callbacks = [EarlyStopping(monitor='val_loss', patience=15)]#optimal-15
history=model.fit(X_train,Y_train[:,3],batch_size=64,epochs=256,
                  validation_data=(X_val,Y_val[:,3]),callbacks=callbacks)

model.save(my_model_path+str(idx)+'.h5')# # of feature=3,5,7,9,?,12,14,16,18
