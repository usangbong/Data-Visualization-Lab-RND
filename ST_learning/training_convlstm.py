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
import pickle
from sklearn.preprocessing import minmax_scale

from keras.callbacks import EarlyStopping
from keras.models import load_model
from keras.models import Sequential
from keras.models import Model
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from keras.layers import Input
from keras.layers import RepeatVector
from keras.layers import TimeDistributed
from keras.layers import Activation
from keras.layers import Flatten,Reshape, BatchNormalization
from keras.layers.merge import concatenate
from keras.layers.convolutional import Conv3D
from keras.layers.convolutional_recurrent import ConvLSTM2D
from keras.layers import Conv2D

#import import_ipynb
#import libs
my_path="data/npy/72/"
my_model_path='model/convlstm/72/model'

X_train=np.load(my_path+"X_train_grid.npy")
Y_train=np.load(my_path+"Y_train_grid.npy")#[:,0,:,:]
X_val=np.load(my_path+"X_val_grid.npy")
Y_val=np.load(my_path+"Y_val_grid.npy")#[:,0,:,:]
#X_test=np.load(my_path+"X_val_grid.npy")
#Y_test=np.load(my_path+"Y_val_grid.npy")#[:,0,:,:]
#with open('data/sc.pickle', 'rb') as handle: sc =pickle.load(handle)

print("load")    

n_steps_in=X_train.shape[1]
n_features=X_train.shape[-1]

idx=[]
for i in range(1,6):
    idx=idx+list(itertools.combinations(list(range(5)), i))
k=int(input())
idx=idx[k]#[(0,)+idx[k]]
n_features=len(idx)

X_train=X_train[:,:,:,:,idx];X_val=X_val[:,:,:,:,idx];#X_test=X_test[:,:,:,:,idx]

n_step_in=X_train.shape
n_sam,n_step_in,r,c,n_f=X_train.shape;rs=32
seq = Sequential()
seq.add(ConvLSTM2D(filters=rs, kernel_size=(5, 5),
                   input_shape=(n_step_in, r, c, n_f),
                   padding='same', return_sequences=True))
seq.add(BatchNormalization())

seq.add(ConvLSTM2D(filters=rs, kernel_size=(5, 5),
                   padding='same', return_sequences=False))
seq.add(BatchNormalization())

seq.add(Conv2D(filters=1, kernel_size=5,
               activation='sigmoid',
               padding='same', data_format='channels_last'))
seq.compile(loss='mse', optimizer='rmsprop')
callbacks = [EarlyStopping(monitor='val_loss', patience=10)]#optimal-15
history=seq.fit(X_train,Y_train[:,:,:,3:4],batch_size=32,epochs=256,
                  validation_data=(X_val,Y_val[:,:,:,3:4]),callbacks=callbacks)

seq.save(my_model_path+str(idx)+'.h5')# # of feature=3,5,7,9,?,12,14,16,18
