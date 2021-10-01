import pandas as pd
import numpy as np
import os
import tensorflow as tf
import json
import joblib
from tensorflow import keras
from keras import optimizers
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime,timedelta
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
import time

#---------------------------------------
# variables
#---------------------------------------
# time performance
start = time.time()

# path
PATH_BASE       = './'
PATH_DATASET    = PATH_BASE + '/dataset/'
PATH_MODEL      = PATH_BASE + '/model/'
# power capacity
power_nm_list   = ['onm1_h','onm2_h','onm3_h','onm4_h']
capacity_list   = [89.7, 96.6, 90, 46.2]
RSRS_IDX        = 0
POWER_NM        = power_nm_list[RSRS_IDX]
RSRS_ID         = POWER_NM[:-2]
CAPACITY        = capacity_list[RSRS_IDX]
print("POWER_NM:{}, CAPACITY:{}".format(POWER_NM,CAPACITY))
# timesteps
SHIFT_DAYS      = 7
PRED_STEPS      = 24
dataX_STEPS     = SHIFT_DAYS*PRED_STEPS
# model param
DIMENSION       = 15
MODEL_NUM       = 1
EPOCHS          = 500
BATCH_SIZE      = 2
EARLY_STOP_PATIENCE = 150
# data ratio
TRAIN_RATIO     = 0.8
VAL_RATIO       = 0.2
# date
PRED_DAY        = datetime(2021, 8, 25, 0,0,0)
MODEL_DAY       = (PRED_DAY).strftime("%Y-%m-%d")
print("--------------------------------------------------------")
print("PRED_DAY:",PRED_DAY)
print("--------------------------------------------------------")

#---------------------------------------
# functions
#---------------------------------------
# 이상치 nan 처리
def power_anomal(x) :
    if x > CAPACITY :
        return np.nan
    return x

def sensor_anomal(x) :
    if x < -900 :
        return np.nan
    return x

# 쏠1 omn 로드
def load_power(POWER_NM):
    df_power = pd.read_csv(PATH_BASE + '/df_power.csv',index_col=0)
    df_power['POWER']=df_power['POWER'].apply(power_anomal).apply(lambda x:x)
    df_power.sort_values(by=['DATE'], axis=0)
    df_power = df_power.set_index(pd.DatetimeIndex(df_power['DATE']))
    df_power.drop(['_id','DATE'], axis=1, inplace=True)
    df_power = df_power.interpolate(method='linear',limit_direction='forward')
    return df_power

# 센서 로드
def load_sensor():
    df_sensor= pd.read_csv(PATH_BASE + '/df_sensor.csv',index_col=0)
    df_sensor.sort_values(by=['DATE'], axis=0)
    df_sensor = df_sensor.set_index(pd.DatetimeIndex(df_sensor['DATE']))
    df_sensor.drop(['_id','DATE'], axis=1, inplace=True)
    df_sensor['uv']=df_sensor['uv'].apply(sensor_anomal).apply(lambda x:x)
    df_sensor['solarradiation']=df_sensor['solarradiation'].apply(sensor_anomal).apply(lambda x:x)
    df_sensor['humidity']=df_sensor['humidity'].apply(sensor_anomal).apply(lambda x:x)
    df_sensor['windspeed']=df_sensor['windspeed'].apply(sensor_anomal).apply(lambda x:x)
    df_sensor['windgust']=df_sensor['windgust'].apply(sensor_anomal).apply(lambda x:x)
    df_sensor['temp']=df_sensor['temp'].apply(sensor_anomal).apply(lambda x:x)
    df_sensor['winddir']=df_sensor['winddir'].apply(sensor_anomal).apply(lambda x:x)
    df_sensor = df_sensor.interpolate(method='linear',limit_direction='forward')
    return df_sensor

def get_df(df_power, df_sensor):
    # power
    pow_scaler = MinMaxScaler(feature_range = (0, 1))
    scaledpower = pow_scaler.fit_transform(df_power.values)
    scaledpower_df = pd.DataFrame(scaledpower, columns=df_power.columns, index=list(df_power.index.values))
    # weather
    df_weather = df_sensor.copy()
    df_weather.drop(['dailyrainin','weeklyrainin','monthlyrainin','yearlyrainin'], axis=1, inplace=True)
    weather_scaler = MinMaxScaler(feature_range = (0, 1))#scale
    scaledweather = weather_scaler.fit_transform(df_weather.values)
    scaledweather_df = pd.DataFrame(scaledweather, columns=df_weather.columns, index=list(df_weather.index.values))

    # join (index merge)
    df = pd.merge(scaledpower_df,scaledweather_df, how='outer',left_index=True, right_index=True)
    df = df[[ 'POWER', 'solarradiation', 'humidity', 'windspeed', 'windgust', 'temp', 'winddir' ]]
    df = df.interpolate(method='linear')
    
    # # insert TARGET
    df_temp = df.copy()
    df = df.iloc[0:-dataX_STEPS+24*(SHIFT_DAYS-1), :]
    target = np.append(df_temp.iloc[dataX_STEPS:, 0].values,np.zeros(24*(SHIFT_DAYS-1)))
    df.insert(df.shape[1], 'TARGET', target, True)
    return pow_scaler, weather_scaler, df

#---------------------------------------
# get data
#---------------------------------------
df_power = load_power(POWER_NM)
df_sensor = load_sensor()
pow_scaler, weather_scaler, df = get_df(df_power, df_sensor)
# test data 확보 (10days)
df = df.iloc[0:-(PRED_STEPS*10), :]
# scaler
joblib.dump(pow_scaler, '{}scaler/power_{}.pkl'.format(PATH_MODEL,RSRS_ID))
joblib.dump(weather_scaler, '{}scaler/weather.pkl'.format(PATH_MODEL))

#---------------------------------------
# create nparray
#---------------------------------------
totalsize = df.shape[0]
dataX, dataY = [], []
print("dataX_STEPS: {}, PRED_STEPS: {}".format(dataX_STEPS, PRED_STEPS))
for i in range(0, totalsize-dataX_STEPS-24+1, PRED_STEPS):
    dataX.append(df.iloc[i:(i + dataX_STEPS),0:-1].values.tolist())
    dataY.append(df.iloc[i:(i + PRED_STEPS),[-1]].values.tolist())
print("len(dataX) : ", len(dataX), np.array(dataX[0]).shape)
print("len(dataY) : ", len(dataY), np.array(dataY[0]).shape)

# Split train/test 
train_size  = int(len(dataX) * TRAIN_RATIO)
val_size    = len(dataX) - train_size
test_size   = 0
val_idx     = train_size+val_size

trainX, valX, testX = np.asarray(dataX[0:train_size]), np.asarray(dataX[train_size:val_idx]), np.asarray(dataX[val_idx:val_idx+test_size])
trainY, valY, testY = np.asarray(dataY[0:train_size]), np.asarray(dataY[train_size:val_idx]), np.asarray(dataY[val_idx:val_idx+test_size])
print('train X : ', trainX.shape, '\tY : ', trainY.shape)
print('val   X : ', valX.shape,   '\tY : ', valY.shape)
print('test  X : ', testX.shape,  '\tY : ', testY.shape)

# convert type
trainX=np.asarray(trainX).astype(np.float64)
trainY=np.asarray(trainY).astype(np.float64)
valX=np.asarray(valX).astype(np.float64)
valY=np.asarray(valY).astype(np.float64)
testX=np.asarray(testX).astype(np.float64)
testY=np.asarray(testY).astype(np.float64)

#---------------------------------------
# modeling
#---------------------------------------
model = tf.keras.Sequential()
model.add(tf.keras.layers.LSTM(dataX_STEPS, input_shape=(trainX.shape[1], trainX.shape[2])))
model.add(tf.keras.layers.RepeatVector(PRED_STEPS))
model.add(tf.keras.layers.LSTM(dataX_STEPS, return_sequences=True))
model.add(tf.keras.layers.TimeDistributed(tf.keras.layers.Dense(dataX_STEPS, activation='relu')))
model.add(tf.keras.layers.TimeDistributed(tf.keras.layers.Dense(1)))
model.summary()

for i in range(MODEL_NUM):

    filename1 = PATH_MODEL+'{}_{}_model1.h5'.format(RSRS_ID,MODEL_DAY)
    print("ModelCheckpoint filename:",filename1)
    checkpoint = ModelCheckpoint(filename1, 
                                monitor='val_loss',
                                verbose=1,# log
                                save_best_only=True,
                                mode='auto'
                            )

    earlystopping = EarlyStopping(monitor='val_loss',
                                patience=EARLY_STOP_PATIENCE,
                                )

    opt = keras.optimizers.RMSprop(lr=0.005, rho=0.9, epsilon=None, decay=0.0)
    model.compile(loss='mean_squared_error', 
                    optimizer=opt
                    )

    hist = model.fit(trainX, trainY, 
                    epochs=EPOCHS, 
                    batch_size=BATCH_SIZE, 
                    validation_data=(valX, valY), 
                    callbacks=[checkpoint, earlystopping])

    filename2 = PATH_MODEL+'{}_{}_model2.h5'.format(RSRS_ID,MODEL_DAY)
    model.save(filename2)

print("time :", time.time() - start)