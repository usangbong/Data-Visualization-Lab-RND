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

from keras.models import load_model
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
from sklearn.metrics import mean_squared_error
#import import_ipynb
#import libs
n_in=72
my_path="data/npy/72/"
my_model_path="model/lstm/72/model"
my_result_path="results/lstm/72/"

import itertools
idx=[]
for i in range(1,6):
    idx=idx+list(itertools.combinations(list(range(5)), i))
k=int(input())
idx=idx[k]#[(0,)+idx[k]]
n_features=len(idx)

#X_test=np.load(my_path+"X_test.npy")
#Y_test=np.load(my_path+"Y_test.npy")[:,0,:,:]
X_test=np.load(my_path+"X_test.npy")
Y_test=np.load(my_path+"Y_test.npy")[:,0,:,:]

X_test=X_test.transpose((0,2,1,3)).reshape((-1,n_in,5))
Y_test=Y_test.reshape((-1,5))
X_test=X_test[:,:,idx]

import pickle
with open("data/sc.pickle", "rb") as input_file:
    sc = pickle.load(input_file)
    
n_steps_in=X_test.shape[1]
n_features=X_test.shape[2]
#print(my_model_path+str(idx)+'.h5')
model=load_model(my_model_path+str(idx)+'.h5')

pred=model.predict(X_test)

pred=sc.inverse_transform(np.array([pred.flatten()]*5).T)[:,3].reshape((-1,336))
y_true=sc.inverse_transform(Y_test.reshape((-1,5)))[:,3].reshape((-1,336))

np.save(my_result_path+str(idx)+"pred",pred)
#np.save(my_result_path+str(idx)+"y_true",y_true)