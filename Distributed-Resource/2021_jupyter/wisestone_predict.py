import pandas as pd
import numpy as np
import os
import sys
import tensorflow as tf
import json
import joblib
import time
from tensorflow import keras
from keras import optimizers
from datetime import datetime,timedelta
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime
pd.set_option('display.max_columns', None)

#---------------------------------------
# variables
#---------------------------------------
start = time.time()
DATASET_NUM = 7
MODEL_NUM = 10

# path
PATH_BASE       = './'
PATH_MODEL      = PATH_BASE + '/model/'
PATH_RESULT     = PATH_BASE + '/result/'
# power capacity
power_nm_list   = ['onm1_h','onm2_h','onm3_h','onm4_h']
capacity_list   = [89.7, 96.6, 90, 46.2]
RSRS_ID         = 0
POWER_NM        = power_nm_list[RSRS_ID]
CAPACITY        = capacity_list[RSRS_ID]
print("POWER_NM:{}, CAPACITY:{}".format(POWER_NM,CAPACITY))
# timesteps
SHIFT_DAYS      = 7
PRED_STEPS      = 24
dataX_STEPS     = SHIFT_DAYS*PRED_STEPS

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

# load sol omn
def load_power(POWER_NM):
    df_power = pd.read_csv(PATH_BASE + '/df_power.csv',index_col=0)
    df_power['POWER']=df_power['POWER'].apply(power_anomal).apply(lambda x:x)
    df_power.sort_values(by=['DATE'], axis=0)
    df_power = df_power.set_index(pd.DatetimeIndex(df_power['DATE']))
    df_power.drop(['_id','DATE'], axis=1, inplace=True)
    df_power = df_power.interpolate(method='linear',limit_direction='forward')
    return df_power

# load sensor
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

def get_df(df_power, df_sensor, POWER_NM):
    # load the scaler
    power_scaler = joblib.load(open('{}scaler/power_{}.pkl'.format(PATH_MODEL,POWER_NM[:-2]), 'rb'))
    weather_scaler = joblib.load(open('{}scaler/weather.pkl'.format(PATH_MODEL), 'rb'))
    # power
    scaledpower = power_scaler.fit_transform(df_power.values)
    scaledpower_df = pd.DataFrame(scaledpower, columns=df_power.columns, index=list(df_power.index.values))
    # weather
    df_weather = df_sensor.copy()
    df_weather.drop(['dailyrainin','weeklyrainin','monthlyrainin','yearlyrainin'], axis=1, inplace=True)
    scaledweather = weather_scaler.fit_transform(df_weather.values)
    scaledweather_df = pd.DataFrame(scaledweather, columns=df_weather.columns, index=list(df_weather.index.values))
    # JOIN (index merge)
    df = pd.merge(scaledpower_df,scaledweather_df, how='outer',left_index=True, right_index=True)
    df = df[[ 'POWER', 'solarradiation', 'humidity', 'windspeed', 'windgust', 'temp', 'winddir' ]]
    df = df.interpolate(method='linear')
    return power_scaler, df

#---------------------------------------
# MODEL_TYPE iteration
#---------------------------------------
total_accRate = 0
total_accRate_list = []
result_pred = pd.DataFrame()
result_acc  = pd.DataFrame()
result_target= pd.DataFrame()

for m in range(0,MODEL_NUM):
# for m in range(0,1):
    model = tf.keras.models.load_model(PATH_MODEL+'model'+str(m)+'.h5')
    print("\n\n MODEL", m, "-"*100)
    accRate_sum = 0
    #---------------------------------------
    # dataset iteration
    #---------------------------------------
    for T in range(0,DATASET_NUM):
        PRED_DAY  = datetime(2021, 8, 25, 0,0,0)+timedelta(T)
        PRED_DAY  = datetime(PRED_DAY.year, PRED_DAY.month, PRED_DAY.day, 0,0,0)
        
        X_START   = PRED_DAY - timedelta(7)
        X_END     = PRED_DAY - timedelta(1)
        X_END     = datetime(X_END.year, X_END.month, X_END.day, 23,0,0)
        # print("X DATA: {} ~ {} => PRED: {} ".format(str(X_START)[:10], str(X_END)[:10], str(PRED_DAY)[:10]))
        
        # get data
        df_power = load_power(POWER_NM)
        df_sensor = load_sensor()
        power_scaler, df = get_df(df_power, df_sensor,POWER_NM)

        # create x,y arr
        x_arr = []
        X_df = df.loc[str(X_START):str(X_END)]
        x_arr.append(X_df.iloc[:].values.tolist())
        x_arr=np.asarray(x_arr).astype(np.float64)
        
        y_arr = []
        Y_df = df.loc[str(PRED_DAY):str(PRED_DAY + timedelta(1))]
        y_arr.append(Y_df.iloc[:,[0]].values.tolist())
        y_arr=np.asarray(y_arr).astype(np.float64)
        
        #---------------------------------------
        # predict
        #---------------------------------------
        n_dataset= x_arr.shape[0]
        predList=[]
        accRate=[]
        yList=[]

        pred = model.predict([x_arr])
        pred[pred<0] = 0
        pred = pred[:,:,0]
        pred = power_scaler.inverse_transform(pred)
        predList = pred.reshape(-1,1)

        #---------------------------------------
        # calculate predictaccRate
        #---------------------------------------
        if(str(PRED_DAY.strftime("%Y-%m-%d")) > str(df.index[-1])[:10]):
            for hr in range(0, PRED_STEPS):
                accRate.append(0)
        else:
            y = power_scaler.inverse_transform(y_arr[:,:,0])
            yList = y.reshape(-1,1)
            
            for hr in range(0, PRED_STEPS):
                pred   = predList[hr]
                target = yList[hr]
                difference = np.abs(target-pred)
                accRate.append(100-np.round(difference/CAPACITY*100, 2))

        accRate_df = pd.DataFrame(np.array(accRate).reshape(1,-1))
        accRate_df.insert(0,'PRED_DATE',PRED_DAY, allow_duplicates=False)
        accRate_df.insert(0,'MODEL',m, allow_duplicates=False)
    
        pred_df = pd.DataFrame(np.array(predList).reshape(1,-1))
        pred_df.insert(0,'PRED_DATE',PRED_DAY, allow_duplicates=False)
        pred_df.insert(0,'MODEL',m, allow_duplicates=False)
        
        y_df = pd.DataFrame(np.array(yList).reshape(1,-1))
        y_df.insert(0,'PRED_DATE',PRED_DAY, allow_duplicates=False)
        y_df.insert(0,'MODEL',m, allow_duplicates=False)

        mean_accRate = np.round(accRate_df.mean(axis = 1,numeric_only = True)[0],2)
        accRate_sum = accRate_sum + mean_accRate
        print("dataset {} : {}".format(T+1,mean_accRate))
    
        if result_pred.shape[0] == 0:
            result_pred = pred_df
            result_acc  = accRate_df
            result_target= y_df
        else:
            result_pred = pd.concat([result_pred, pred_df])
            result_acc  = pd.concat([result_acc, accRate_df])
            result_target= pd.concat([result_target, y_df])
    
    result_pred.append(pred_df)
    total_accRate_list.append(np.round(accRate_sum/DATASET_NUM,2))

pd.DataFrame(result_pred).to_csv(PATH_RESULT + '/result_pred.csv',mode='w',index=False, encoding='CP949')
pd.DataFrame(result_pred).to_csv(PATH_RESULT + '/result_pred.csv',mode='w',index=False, encoding='CP949')
pd.DataFrame(result_target).to_csv(PATH_RESULT + '/result_target.csv',mode='w',index=False, encoding='CP949')

print("========================================== [ ACCURACY RATE ]==========================================")
print("\t ACC\t",total_accRate_list)
print("\t TOTAL\t",np.round(np.mean(total_accRate_list),2))
print("=======================================================================================================")