import pandas as pd
import tensorflow as tf
import autokeras as ak
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tensorflow as tf

from numpy import concatenate
from pandas import read_csv, DataFrame, concat
from sklearn.preprocessing import MinMaxScaler

np.set_printoptions(suppress=True)

EPOCHS       = 10
BATCH_SIZE   = 128

SHIFT_DAYS   = 3
PRED_STEPS   = 24*6 #48hr * 10분단위 예측
TIME_STEPS   = SHIFT_DAYS*PRED_STEPS #hours step
DIMENSION    = 15
MODEL_NUM    = 10
CAPACITY     = 89.7

TRAIN_RATIO = 0.6
VAL_RATIO = 0.2

START_DATE = '2021012899'
END_DATE   = '2021042924'

SAVE_PATH = './data/'
SAVE_NAME = 'autoML_Test'


def getData():
    # power
    power_file  = './data/power_20210129_20210429_preprocess_1hour'
    power_df = read_csv(power_file+'.csv', encoding='CP949', converters={'date':int})
    print(power_df.shape)
        
    # sensor    
    sensor_file = 'data/sensor_20210129_20210429_preprocess_1hour'
    sensor_df = read_csv(sensor_file+'.csv', encoding='CP949', converters={'date':int})
    sensor_df = sensor_df.sort_values('date')
    print(sensor_df.shape)

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
    #df = df.iloc[0:-TIME_STEPS, :]
    #df.insert(df.shape[1], 'pow_Y', power_scaleddf.iloc[TIME_STEPS:, :].values, True)
    #df.insert(df.shape[1], 'pow_Y', power_scaleddf.iloc[TIME_STEPS:, :].values, True)

    #df.to_csv(SAVE_PATH+"total_scaled"+SAVE_NAME+".csv",mode='w',index=False, encoding='CP949')
    #display(df) 

    return pow_scaler, df

pow_scaler, df = getData()
#display(df)

dataset    = df
val_split  = int(len(dataset) * 0.7)
data_train = dataset[:val_split]
validation_data = dataset[val_split:]

data_x = data_train[
    [
        'pow', 'temp', 'humidity', 'windspeed', 'windgust', 'maxdailygust',
        'winddir', 'hourlyrainin', 'dailyrainin', 'weeklyrainin',
        'monthlyrainin', 'yearlyrainin', 'solarradiation', 'uv', 'feelslike',
        'dewpoint', 'outside_status'
    ]
].astype("float64")

data_x_val = validation_data[
    [
        'pow', 'temp', 'humidity', 'windspeed', 'windgust', 'maxdailygust',
        'winddir', 'hourlyrainin', 'dailyrainin', 'weeklyrainin',
        'monthlyrainin', 'yearlyrainin', 'solarradiation', 'uv', 'feelslike',
        'dewpoint', 'outside_status'
    ]
].astype("float64")

# Data with train data and the unseen data from subsequent time steps.
data_x_test = dataset[
    [
        'pow', 'temp', 'humidity', 'windspeed', 'windgust', 'maxdailygust',
        'winddir', 'hourlyrainin', 'dailyrainin', 'weeklyrainin',
        'monthlyrainin', 'yearlyrainin', 'solarradiation', 'uv', 'feelslike',
        'dewpoint', 'outside_status'
    ]
].astype("float64")

data_y = data_train["pow"].astype("float64")

data_y_val = validation_data["pow"].astype("float64")

print(data_x.shape)  # (6549, 12)
print(data_y.shape)  # (6549,)

predict_from = 1
predict_until = 10
lookback = 3
clf = ak.TimeseriesForecaster(
    lookback=lookback,
    predict_from=predict_from,
    #predict_until=predict_until,
    #max_trials=1,
    objective="val_loss",
)
# Train the TimeSeriesForecaster with train data
clf.fit(
    x=data_x,
    y=data_y,
    validation_data=(data_x_val, data_y_val),
    batch_size=128,
    epochs=10,
)
# Predict with the best model(includes original training data).
predictions = clf.predict(data_x_test)
print(predictions.shape)
# Evaluate the best model with testing data.
print(clf.evaluate(data_x_val, data_y_val))