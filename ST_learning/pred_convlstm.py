import numpy as np
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

from keras.models import load_model


print("Start")
n_in=6

my_result_path="results/convlstm/"+str(n_in)+"/"
import itertools
idx=[]
for i in range(1,6):
    idx=idx+list(itertools.combinations(list(range(5)), i))
k=int(input())
idx=idx[k]#[(0,)+idx[k]]
n_features=len(idx)

my_model_path='model/convlstm/'+str(n_in)+'/model'
X_test=np.load("data/npy/"+str(n_in)+"/X_test_grid.npy")
Y_test=np.load("data/npy/"+str(n_in)+"/Y_test_grid.npy")#[:,0,:,:]
with open('data/sc.pickle', 'rb') as handle: sc =pickle.load(handle)
X_test=X_test[:,:,:,:,idx]

model=load_model(my_model_path+str(idx)+'.h5')

pred=model.predict(X_test)
grid_array=np.load("data/grid.npy")
idx=np.where(~np.isnan(grid_array.flatten()))
n_s=pred.shape[0]
pred=np.array([grid_array]*n_s)*pred[:,:,:,0]
pred=pred.reshape((n_s,-1))
pred=pred[:,idx[0]]

y_true=Y_test[:,:,:,3:4]
y_true=np.array([grid_array]*n_s)*y_true[:,:,:,0]
y_true=y_true.reshape((n_s,-1))
y_true=y_true[:,idx[0]]

pred=sc.inverse_transform(np.array([pred.flatten()]*5).T)[:,3].reshape((-1,336))
y_true=sc.inverse_transform(np.array([y_true.flatten()]*5).T)[:,3].reshape((-1,336))


idx=[]
for i in range(1,6):
    idx=idx+list(itertools.combinations(list(range(5)), i))
idx=idx[k]
np.save(my_result_path+str(idx)+"pred",pred)

print("done")
