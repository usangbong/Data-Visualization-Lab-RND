import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import mean_squared_error,r2_score
#from sklearn.preprocessing import MinMaxScaler
from scipy.stats import iqr
import os
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
from keras.callbacks import EarlyStopping
from keras.callbacks import ModelCheckpoint
from keras.layers import SimpleRNN
from keras.layers import GRU
from utils import Minmaxscaler
import sys

def main(argv):
    ########################
    n_steps_in=72
    n_steps_out=24
    dataset_dir='data'
    n_features_w=int(argv)#n_features_w=10#1,...,11
    print('n_features_w',n_features_w)
    idx=[9,  5, 11,  3, 10,  4,  1,  2,  8,  6,  7]
    idx=np.array(idx[:n_features_w])
    idx=np.concatenate([[0],idx*2-1,idx*2],axis=0)
    idx=np.setdiff1d(idx,[12,14,16,18,20,22])
    idx=np.sort(idx)
    print('idx',idx)
    n_features=len(idx)
    print('n_features',n_features)
    ########################
    print('tmp')
    
    np_load_old = np.load
    np.load = lambda *a,**k: np_load_old(*a, allow_pickle=True, **k)# modify the default parameters of np.load
    data = {}
    for category in ['train', 'val', 'test']:
        cat_data = np.load(os.path.join(dataset_dir, category + '.npz'))
        data['x_' + category] = cat_data['x']
        data['y_' + category] = cat_data['y']
    np.load = np_load_old# restore np.load for future normal usage

    scaler = Minmaxscaler(minvalue=np.min(data['x_train'],axis=(0,1)), maxvalue=np.max(data['x_train'],axis=(0,1)))
    for category in ['train', 'val', 'test']:
        #data['x_' + category][..., 0] = scaler.transform(data['x_' + category][..., 0])
        #data['y_' + category][..., 0] = scaler.transform(data['y_' + category][..., 0])
        data['x_' + category] = scaler.transform(data['x_' + category])[...,idx]
        data['y_' + category] = scaler.transform(data['y_' + category])[:,:,:1]
    for cat in ["train", "val", "test"]: print(data['x_'+cat].shape,data['y_'+cat].shape)
    for cat in ["train", "val", "test"]: print(cat,np.min(data['x_'+cat]),np.max(data['x_'+cat]),np.min(data['y_'+cat]),np.max(data['y_'+cat]))

    model = Sequential()
    #model.add(LSTM(256, activation='relu',dropout=0.5, input_shape=(n_steps_in, n_features)))#9
    model.add(LSTM(256, activation='relu',input_shape=(n_steps_in, n_features)))
    model.add(RepeatVector(n_steps_out))
    model.add(LSTM(256, activation='relu', return_sequences=True))
    model.add(TimeDistributed(Dense(256, activation='relu')))
    #model.add(TimeDistributed(Dense(50, activation='relu')))
    model.add(TimeDistributed(Dense(1)))

    #training
    model.compile(loss='mse', optimizer='rmsprop')
    cb = EarlyStopping(monitor='val_loss', patience=30)
    mc = ModelCheckpoint('saved_model/'+str(n_features_w)+'/model-{epoch:03d}-{val_loss:03f}.h5', verbose=1, monitor='val_loss',save_best_only=True)  
    history=model.fit(data['x_train'],data['y_train'],batch_size=64,epochs=128,
                      validation_data=(data['x_val'],data['y_val']),callbacks=[cb,mc])
    model.save('saved_model/'+str(n_features)+'_last.h5')#

if __name__ == "__main__":
    main(sys.argv[1])