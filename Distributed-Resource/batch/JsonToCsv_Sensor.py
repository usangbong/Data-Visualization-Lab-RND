import csv
import json
import pandas as pd
import os
import glob
import datetime
# .json -> .csv


base_dir        = 'C:/solar/HY_TEST/'
#base_dir        = 'D:/elsys/solar/'
sensor_dir      = base_dir + 'SENSOR/_json'
save_dir        = base_dir + 'SENSOR/_csv/'

column_list     = ['id','loc_oid','TIME','solarradiation','uv','temp','humidity','winddir','windspeed','windgust','dewpoint','maxdailygust','feelslike','hourlyrainin','dailyrainin','weeklyrainin','monthlyrainin','yearlyrainin']

json_pattern    = os.path.join(sensor_dir,'*.json')
file_list       = glob.glob(json_pattern)


for file in file_list:
    with open(file) as json_file:
        
        # parsing json file
        json_data = json.load(json_file)
        data = json_data['result']

        _id              = []
        loc_oid          = []
        TIME             = []
        solarradiation   = []
        uv               = []
        temp             = []
        humidity         = []
        winddir          = []
        windspeed        = []
        windgust         = []
        dewpoint         = []
        maxdailygust     = []
        feelslike        = []
        hourlyrainin     = []
        dailyrainin      = []
        weeklyrainin     = []
        monthlyrainin    = []
        yearlyrainin     = []

        for dataline in data:
            _id.append(dataline['id'])
            loc_oid.append(dataline['loc_oid'])
            TIME.append(dataline['TIME'])
            solarradiation.append(dataline['solarradiation'])
            uv.append(dataline['uv'])
            temp.append(dataline['temp'])
            humidity.append(dataline['humidity'])
            winddir.append(dataline['winddir'])
            windspeed.append(dataline['windspeed'])
            windgust.append(dataline['windgust'])
            dewpoint.append(dataline['dewpoint'])
            maxdailygust.append(dataline['maxdailygust'])
            feelslike.append(dataline['feelslike'])
            hourlyrainin.append(dataline['hourlyrainin'])
            dailyrainin.append(dataline['dailyrainin'])
            weeklyrainin.append(dataline['weeklyrainin'])
            monthlyrainin.append(dataline['monthlyrainin'])
            yearlyrainin.append(dataline['yearlyrainin'])
                
        df = pd.DataFrame(columns=column_list)
        df['id'] = _id
        df['loc_oid'] = loc_oid
        df['TIME'] = TIME
        df['solarradiation'] = solarradiation
        df['uv'] = uv
        df['temp'] = temp
        df['humidity'] = humidity
        df['winddir'] = winddir
        df['windspeed'] = windspeed
        df['windgust'] = windgust
        df['dewpoint'] = dewpoint
        df['maxdailygust'] = maxdailygust
        df['feelslike'] = feelslike
        df['hourlyrainin'] = hourlyrainin
        df['dailyrainin'] = dailyrainin
        df['weeklyrainin'] = weeklyrainin
        df['monthlyrainin'] = monthlyrainin
        df['yearlyrainin'] = yearlyrainin
        
        # save csv file
        df.to_csv(save_dir + file[-13:-5] + '.csv', index=False, header=True)
