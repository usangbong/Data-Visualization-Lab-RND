#---- to do list -----
# err_data_list 파일자동화
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import openpyxl
import fnmatch
import tensorflow as tf
import random
import datetime
from tensorflow.keras.models import load_model
from tensorflow.python.keras.optimizer_v2.rmsprop import RMSProp
from math import sqrt
from numpy import concatenate
from matplotlib import pyplot
from pandas import read_csv, DataFrame, concat
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense, RepeatVector, LSTM, Input, TimeDistributed, Activation, Dropout
from keras.optimizers import SGD
from pandas import read_csv
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import PowerTransformer 
#from feature_engine import variable_transformers as vt
from scipy.stats import yeojohnson

np.set_printoptions(suppress=True)

EPOCHS       = 500
BATCH_SIZE   = 64

SHIFT_DAYS   = 3
PRED_STEPS   = 48 #48hr * 10분단위 예측
TIME_STEPS   = SHIFT_DAYS*PRED_STEPS #hours step
DIMENSION    = 15
MODEL_NUM    = 10
CAPACITY     = 89.7

TRAIN_RATIO  = 0.6
VAL_RATIO    = 0.2

START_DATE = '2021012899'
END_DATE   = '2021042924'

NOWDATE = str(datetime.datetime.now()).replace("-", "").replace(":", "").replace(" ", "_").replace(".", "_")
SAVE_PATH = './data/'+str(NOWDATE)+'/'
os.mkdir(SAVE_PATH)

FILE_SEED = NOWDATE[-6:]
SAVE_NAME = str(FILE_SEED)+'_1h_'+str(EPOCHS)+'e_'+str(BATCH_SIZE)+'b'
print("SAVE_NAME : ", SAVE_NAME)

#############################################
# get weather, power
#############################################
def getData():
    # power
    power_file  = './data/power_20210129_20210429_preprocess_1hour'
    power_df = read_csv(power_file+'.csv', encoding='CP949', converters={'date':int})
    print(power_df.shape)
        
    # sensor    
    sensor_file = 'data/sensor_20210129_20210429_preprocess_1hour'
    sensor_df = read_csv(sensor_file+'.csv', encoding='CP949', converters={'date':int})
    #sensor_df['date'] = sensor_df['date'].astype('int')
    sensor_df = sensor_df.sort_values('date')
    print(sensor_df.shape)

    ''' JOIN TEST '''
    join_test = sensor_df.copy()

    # pow + weather + powY
    join_test.insert(0, 'pow', power_df['power'].values, True)
    print(join_test)
    join_test.to_csv(SAVE_PATH+"join_test"+SAVE_NAME+".csv",mode='w',index=False, encoding='CP949')

    # scale
    power_df.drop(['date'], axis=1, inplace=True)
    pow_scaler = MinMaxScaler(feature_range = (0, 1))
    scaled_pow = pow_scaler.fit_transform(power_df.values)
    power_scaleddf = pd.DataFrame(scaled_pow, columns=power_df.columns, index=list(power_df.index.values))

    weather_df = sensor_df.copy()
    weather_df.drop(['date'], axis=1, inplace=True)
    weather_scaler = MinMaxScaler(feature_range = (0, 1))#scale
    scaled_weather = weather_scaler.fit_transform(weather_df.values)
    weather_scaleddf = pd.DataFrame(scaled_weather, columns=weather_df.columns, index=list(weather_df.index.values))

    # JOIN 
    df = weather_scaleddf.copy()

    # pow + weather + powY
    df.insert(0, 'pow', power_scaleddf.values, True)
    df = df.iloc[0:-TIME_STEPS, :]
    df.insert(df.shape[1], 'pow_Y', power_scaleddf.iloc[TIME_STEPS:, :].values, True)

    df.to_csv(SAVE_PATH+"total_scaled"+SAVE_NAME+".csv",mode='w',index=False, encoding='CP949')
    #display(df) 

    return pow_scaler, df

pow_scaler, df = getData()

#correlation
corr_df = df.corr()
corr_df = corr_df.apply(lambda x: round(x ,2))
#display(corr_df[0:1])
corr_df1 = corr_df.nlargest(df.shape[0], 'pow')
corr_df1 = corr_df1[list(corr_df1.index)]
print(corr_df1[0:1])

#############################################
# create nparray
#############################################
# time step만큼 window 움직여 dataset 생성
totalsize = df.shape[0]
dataX, dataY = [], []
print("TIME_STEPS: {}, PRED_STEPS: {}".format(TIME_STEPS, PRED_STEPS))
for i in range(0, totalsize-TIME_STEPS-24+1, PRED_STEPS):
    dataX.append(df.iloc[i:(i + TIME_STEPS),0:-1])
    dataY.append(df.iloc[i:(i + PRED_STEPS),[-1]])

print("len(dataX) : ", len(dataX), dataX[0].shape)
print("len(dataY) : ", len(dataY), dataY[0].shape)

#  Split train/test 
train_size = int(len(dataX) * TRAIN_RATIO)
val_size   = int(len(dataX) * VAL_RATIO)
test_size  = len(dataX) - train_size - val_size
val_idx = train_size+val_size

trainX, valX, testX = np.array(dataX[0:train_size]), np.array(dataX[train_size:val_idx]), np.array(dataX[val_idx:val_idx+test_size])
trainY, valY, testY = np.array(dataY[0:train_size]), np.array(dataY[train_size:val_idx]), np.array(dataY[val_idx:val_idx+test_size])

print('train X : ', trainX.shape, '\tY : ', trainY.shape)
print('val   X : ', valX.shape,   '\tY : ', valY.shape)
print('test  X : ', testX.shape,  '\tY : ', testY.shape)

np.save(SAVE_PATH+"npset_"+SAVE_NAME+"_trainX",trainX)
np.save(SAVE_PATH+"npset_"+SAVE_NAME+"_trainY",trainY)
np.save(SAVE_PATH+"npset_"+SAVE_NAME+"_valX",valX)
np.save(SAVE_PATH+"npset_"+SAVE_NAME+"_valY",valY)
np.save(SAVE_PATH+"npset_"+SAVE_NAME+"_testX",testX)
np.save(SAVE_PATH+"npset_"+SAVE_NAME+"_testY",testY)

def show_shapes(): # can make yours to take inputs; this'll use local variable values
    print("Expected: (num_samples, TIME_STEPS, channels)")
    print("trainX:{}\t {} \t/ {}\t {}".format(trainX.dtype, trainX.shape, trainY.dtype, trainY.shape))
    print("valX:  {}\t {} \t/ {}\t {}".format(valX.dtype, valX.shape, valY.dtype, valY.shape))
    print("testX: {}\t {} \t/ {}\t {}".format(testX.dtype, testX.shape, testY.dtype, testY.shape))

show_shapes()

trainX=np.asarray(trainX).astype(np.float64)
trainY=np.asarray(trainY).astype(np.float64)
valX=np.asarray(valX).astype(np.float64)
valY=np.asarray(valY).astype(np.float64)
testX=np.asarray(testX).astype(np.float64)
testY=np.asarray(testY).astype(np.float64)

#############################################
# modeling
#############################################
model = tf.keras.Sequential()
model.add(tf.keras.layers.LSTM(256, input_shape=(trainX.shape[1], trainX.shape[2])))
model.add(tf.keras.layers.RepeatVector(PRED_STEPS))
model.add(tf.keras.layers.LSTM(256, return_sequences=True))
model.add(tf.keras.layers.TimeDistributed(tf.keras.layers.Dense(256, activation='relu')))
model.add(tf.keras.layers.TimeDistributed(tf.keras.layers.Dense(1)))
model.summary()

modelList  = []
histList   = []
resultList = []
for i in range(MODEL_NUM):#0,5):#
    #keras.optimizers.RMSprop(lr=0.005, rho=0.9, epsilon=None, decay=0.0)
    model.compile(loss='mean_squared_error', 
                    optimizer=RMSProp()
                    #optimizer=RMSProp(learning_rate=0.001)
                    #optimizer=SGD(lr=0.01, momentum=0.9, nesterov=True), 
                    #metrics=['acc'])
                    )

    hist = model.fit(trainX, trainY, epochs=EPOCHS, batch_size=BATCH_SIZE, validation_data=(valX, valY))
    results = model.evaluate(testX, testY)
    model.save(SAVE_PATH+'model_'+SAVE_NAME+'_'+str(i)+'.h5')# # of feature=3,5,7,9,?,12,14,16,18
    model.save(SAVE_PATH+'model_'+SAVE_NAME+'_'+str(i)+'.h5')# # of feature=3,5,7,9,?,12,14,16,18
    
    modelList.append(model)
    histList.append(hist)
    resultList.append(results)


#############################################
# Prediction Error Rate
#############################################
# 예측 오차율 계산
#plt.rcParams['font.size'] = 10
predErrRate_list = []
modelList = []
for n in range(MODEL_NUM):
    modelList.append(load_model(SAVE_PATH+'model_'+SAVE_NAME+'_'+str(n)+'.h5'))

for n in range(MODEL_NUM):
    errRate = []
    y = pow_scaler.inverse_transform(trainY[:,:,0])
    plotY = y.reshape(-1,1)

    pred = modelList[n].predict(trainX)[:,:,0]
    pred[pred<0] = 0
    x = pow_scaler.inverse_transform(pred)
    plot_pred = x.reshape(-1,1)

    target_list=[]
    for i in range(0, plotY.shape[0], PRED_STEPS):
        for hr in range(0, PRED_STEPS):
            pred   = plot_pred[i+hr]
            target = plotY[i+hr]
            difference = np.abs(target-pred)
            errRate.append(np.round(difference/CAPACITY*100, 2))

            #print("|t:",target,"-p:",pred,"|=",err,",예측오차율:",predErrRate)
            #err_list.append(err)
            
            target_list.append(target)
            
    predErrRate_list.append(errRate)
    #print(n,";",np.shape(predErrRate_list[n]))
    print(n," avg;",np.round(sum(predErrRate_list[n])/len(predErrRate_list[n]),4),end='')
    print("\t max;",max(predErrRate_list[n]),end='')
    print("\t val_loss;",np.round(resultList[n],4))
    
# save csv files    
print(np.shape(predErrRate_list))
predErrRate_df = pd.DataFrame(predErrRate_list).transpose()
predErrRate_df.to_csv(SAVE_PATH+"predErrRate_"+SAVE_NAME+".csv",mode='w',index=False, encoding='CP949')

histList_df = pd.DataFrame(histList).transpose()
histList_df.to_csv(SAVE_PATH+"histList_"+SAVE_NAME+".csv",mode='w',index=False, encoding='CP949')

resultList_df = pd.DataFrame(resultList).transpose()
resultList_df.to_csv(SAVE_PATH+"resultList_"+SAVE_NAME+".csv",mode='w',index=False, encoding='CP949')

print("SAVE_NAME : ", SAVE_NAME)


# print Err Rate
listsize = len(predErrRate_list[0])
count = []
column_names = ["0 < x < 6","(%)","6 < x < 8","(%)","8 < x < 10","(%)", "0 < x < 10","(%)",]
for m in range(MODEL_NUM):
    testList = predErrRate_list[m].copy()
    testList.sort()
    #count = sum(map(lambda x : x>5, listOfElems))
    count.append(int(sum(map(lambda x : x<6, testList))))
    count.append(np.round(count[-1]/listsize*100,2))
    count.append(int(sum(map(lambda x : x>6 and x < 8, testList))))
    count.append(np.round(count[-1]/listsize*100,2))
    count.append(int(sum(map(lambda x : x>8 and x < 10, testList))))
    count.append(np.round(count[-1]/listsize*100,2))
    count.append(np.round(sum(map(lambda x : x < 10, testList))))
    count.append(np.round(count[-1]/listsize*100,2))
    
countArr = np.array(count).reshape(10,-1)
countDf = pd.DataFrame(countArr, columns = column_names)
print(countDf)
#acc_list.append(acc_rate)
#print("   pred: ",pred," | target: ",target," | error: ",error," | err rate: ",error_rate," | acc: ",acc_rate,sep="")