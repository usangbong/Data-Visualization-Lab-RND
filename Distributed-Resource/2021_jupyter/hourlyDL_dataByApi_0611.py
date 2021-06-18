#---- to do list -----
# err_data_list 파일자동화
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import openpyxl
import fnmatch
import time
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
#from keras.optimizers import SGD
from pandas import read_csv
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import PowerTransformer 
#from feature_engine import variable_transformers as vt
from scipy.stats import yeojohnson

np.set_printoptions(suppress=True)

start = time.time() 

EPOCHS       = 200
BATCH_SIZE   = 64

SHIFT_DAYS   = 3
PRED_STEPS   = 48 #48hr * 10분단위 예측
TIME_STEPS   = SHIFT_DAYS*PRED_STEPS #hours step
MODEL_NUM    = 10

TRAIN_RATIO  = 0.6
VAL_RATIO    = 0.2

START_DATE = '20210129'
END_DATE   = '20210531'
FILE_NAME  =  START_DATE+'_'+END_DATE

RSRS_IDX = 3
BASE_PATH = 'C:/elsys/solar/'
RSRSID_list=['RSRS0000000239', 'RSRS0000000241', 'RSRS0000000247', 'RSRS0000000249']
RSRS_SAVE_NM = RSRSID_list[RSRS_IDX][11:14]
CAPACITY_list = [89.7, 96,6, 90, 46.2]
CAPACITY     = float(CAPACITY_list[RSRS_IDX])

NOWDATE = str(datetime.datetime.now()).replace("-", "").replace(":", "").replace(" ", "_").replace(".", "_")
SAVE_PATH = BASE_PATH+'data/'+RSRS_SAVE_NM+'_'+str(NOWDATE)+'/'
os.mkdir(SAVE_PATH)

FILE_SEED = NOWDATE[-6:]
SAVE_NAME = str(FILE_SEED)+'_1h_'+str(EPOCHS)+'e_'+str(BATCH_SIZE)+'b'
print("SAVE_NAME : ", SAVE_NAME)

def zeroTo24(x) :
    if str(x).endswith("00") == True :
        return str(x)[0:8]+"24"
    return str(x)

#############################################
# get weather, power
#############################################
def getData():
    ''' Load Data '''
    # ASOS weather
    weather_df = read_csv(BASE_PATH+'OBS_ASOS_20210129_20210531.csv', encoding='CP949')
    weather_df['DATE'] = weather_df['일시'].str[0:4]+weather_df['일시'].str[5:7]+weather_df['일시'].str[8:10]+weather_df['일시'].str[11:13]# DATE 처리(format변환: 00~23시 -> 01~24시)
    for r in range(weather_df.shape[0]):
            if weather_df.iloc[r,-1].endswith("00") == True:
                weather_df.iloc[r,-1] = weather_df.iloc[r-1,-1][0:8]+"24"
    weather_df=weather_df.drop(['일시', '지점', '지점명','5cm 지중온도(°C)', '10cm 지중온도(°C)', '20cm 지중온도(°C)', '30cm 지중온도(°C)','지면상태(지면상태코드)'], axis=1)
    weather_df = weather_df.interpolate(method='slinear')
    weather_df = weather_df.fillna(0)
    
    # power
    power_df = read_csv(BASE_PATH+'_'+RSRS_SAVE_NM+'_onm_df_20210129_20210531_1hour.csv', encoding='CP949', converters={'DATE':int})
    
    # sensor    
    SENSOR_CSV_NM = '_sensor_MIX(hourly)'
    sensor_df = read_csv(BASE_PATH+'_MERGE_'+ SENSOR_CSV_NM + '_power_weather.csv', encoding='CP949', converters={'DATE':int})
    sensor_df = sensor_df.interpolate(method='linear')
    sensor_df.to_csv(BASE_PATH+'_sensor_df_1hour_interpolate.csv', encoding='CP949',mode='w',index=False)

    ''' 결측시간 처리 위해 DATE로 merge '''
    # merge (sensor, weather) => weather_df
    sensor_df['DATE']=sensor_df['DATE'].astype(str)
    weather_df['DATE']=weather_df['DATE'].astype(str)
    weather_df = sensor_df.merge(weather_df, left_on='DATE', right_on='DATE', how='right', suffixes=(False, False))
    weather_df.to_csv(BASE_PATH+'_sensor_df_1hour_interpolate_test.csv', encoding='CP949',mode='w',index=False)

    # merge (power, sensor, weather) => df
    weather_df['DATE']=weather_df['DATE'].astype(str)
    power_df['DATE']=power_df['DATE'].astype(str)
    df = power_df.merge(weather_df, left_on='DATE', right_on='DATE', how='right', suffixes=(False, False))
    df.to_csv(BASE_PATH+'_MERGED DF_power+sensor+asos.csv', encoding='CP949',mode='w',index=False)
        
    ''' scaler 구하기 '''
    # power , weather 분리
    power_df = df.iloc[:,1:2]
    weather_df=df.iloc[:,2:]

    pow_scaler = MinMaxScaler(feature_range = (0, 1))
    scaled_pow = pow_scaler.fit_transform(power_df.values)
    power_scaleddf = pd.DataFrame(scaled_pow, columns=power_df.columns, index=list(power_df.index.values))

    weather_scaler = MinMaxScaler(feature_range = (0, 1))#scale
    scaled_weather = weather_scaler.fit_transform(weather_df.values)
    weather_scaleddf = pd.DataFrame(scaled_weather, columns=weather_df.columns, index=list(weather_df.index.values))

    # pow + weather + powY
    df = weather_scaleddf.copy()
    df.insert(0, 'POWER', power_scaleddf.values, True)
    df = df.iloc[0:-TIME_STEPS, :]
    df.insert(df.shape[1], 'POWER_Y', power_scaleddf.iloc[TIME_STEPS:, :].values, True)
    df.to_csv(BASE_PATH+"/_total_scaled_df_"+FILE_NAME+"_1hour.csv",mode='w',index=False, encoding='CP949')
    
    ''' Feature Selection '''
    df = df[['POWER',
        'uv', 'solarradiation', '일조(hr)', '지면온도(°C)', '풍속(m/s)', 
        'windspeed', 'windgust', 'temp', 'feelslike'
        ,'POWER_Y']]

    df.to_csv(BASE_PATH+'_TOTAL SCALED DF_sum(sensor)+ASOS.csv', encoding='CP949',mode='w',index=False)

    return pow_scaler, df

# --------------------------------------------------------------------------------------------------------------

pow_scaler, df = getData()


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



####################################################### TEST
n_dataset   = testY.shape[0]
acc_list    = []
acc_model   = []
predictModel = []
predList=[]
predErrRate_list=[]
yList=[]
print(n_dataset)

print("[ model ]")
for m in range(MODEL_NUM):
    errRate=[]
    print("-"*70,"[ model {} ]".format(m))
#for m in range(2):
    plot_target=[]
    plot_predict=[]
    for i in range(n_dataset):
        #print("(dataset {}) : ".format(i), end='')
    #for i in range(5):
    #if(i in [2,3,4,5,6,7,8]): continue;
        y = pow_scaler.inverse_transform(testY[i:i+1,:,0])
        yList = y.reshape(-1,1)

        pred = modelList[m].predict([testX[i:i+1]])
        pred[pred<0] = 0
        pred = pred[:,:,0]
        pred = pow_scaler.inverse_transform(pred)
        predSum = np.sum(pred)
        predList = pred.reshape(-1,1)

        target_list=[]
        for i in range(0, yList.shape[0], PRED_STEPS):
            for hr in range(0, PRED_STEPS):
                pred   = predList[i+hr]
                target = yList[i+hr]
                difference = np.abs(target-pred)
                errRate.append(np.round(difference/CAPACITY*100, 2))
                target_list.append(target)

        target      = round(np.sum(y), 2)
        error       = round(np.abs(target-predSum), 2)
        error_rate  = np.min([round(error/target, 2),1])
        acc_rate    = round((1.0-error_rate)*100, 2)
        acc_list.append(acc_rate)
        #print("acc rate: ",np.mean(acc_list[-n_model:]),sep='')
        #predErrRateTest_AllModel.append(predErrRateTest)
        print(np.round(np.mean(acc_list[-MODEL_NUM:]),2), " / ",sep='',end='')
        
    predErrRate_list.append(errRate)
    print(" \tErr Rate avg;",np.round(sum(predErrRate_list[m])/len(predErrRate_list[m]),2),end='')
    print(" \t max;",np.max(predErrRate_list[m]))

print("\npredErrRate_list:{}".format(np.shape(predErrRate_list)))
predErrRate_df = pd.DataFrame(predErrRate_list).transpose()
predErrRate_df.to_csv(SAVE_PATH+"predErrRate_"+SAVE_NAME+"_TEST333.csv",mode='w',index=False, encoding='CP949')
print("----------------------------------------------")
print("mean(acc rate): ",np.mean(acc_list),sep='')
print("----------------------------------------------")
print("[ model ]")
#for m in range(MODEL_NUM):
    #print(predErrRateTest_AllModel[m])
    #acc_model[i] = round(acc_model[i]/(n_dataset),2)
    #print(acc_model[i])

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
print("0 < x < 10 (%) : AVG {} \t MIN {} \t MAX {}".format(np.mean(countDf.iloc[:,-1]), np.min(countDf.iloc[:,-1]), np.max(countDf.iloc[:,-1])))
#acc_list.append(acc_rate)
#print("   pred: ",pred," | target: ",target," | error: ",error," | err rate: ",error_rate," | acc: ",acc_rate,sep="")
print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간
print("SAVE_NAME : ", RSRS_SAVE_NM+'_'+SAVE_NAME)