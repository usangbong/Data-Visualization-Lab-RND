from flask import Flask, render_template,flash,request
import os
from os import listdir
from os.path import isfile, join
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import pandas as pd
import numpy as np
import json
import pickle
from sklearn.metrics import mean_squared_error,r2_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import scipy
from scipy.stats import iqr
from scipy.interpolate import griddata
from PIL import Image, ImageDraw
from collections import Counter
import itertools
from datetime import date
import matplotlib.pyplot as plt
from lib import toimage

from keras.models import load_model
from keras import backend as K

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


def getting_data():
    df = pd.read_csv("data/04_10558.csv", sep='|', engine='python',header=None)
    df.columns = ['date', 'sensor','flag','pm10','co2','vocs','noise','temp','humi','co','hcho','pm25','n']
    df=df.drop(['flag','co2','vocs','co','hcho','n'], axis=1)
    df=df.dropna()
    df_corr=df.iloc[:,[2,3,4,5,6]].corr(method ='pearson')
    df_corr= df_corr.to_dict(orient='records')
    df_corr = json.dumps(df_corr, indent=2)
    #scatter data
    tmpc=pd.Series(['a', 'b', 'c','d'])
    tmpc=tmpc.repeat(360)
    tmpc=tmpc[:df.shape[0]]
    df['sepcolor'] = tmpc.values
    chart_data = df.to_dict(orient='records')
    chart_data = json.dumps(chart_data, indent=2)
    #result_seoul=pd.DataFrame({"pred":["test.png"]})
    #data = {'chart_data': chart_data,'records': records.to_dict(orient='records'),'result_seoul': result_seoul.to_dict(orient='records')}
    #data = {'chart_data': chart_data,'records': records.to_dict(orient='records'),'records_inter': records_inter.to_dict(orient='records')}

    #numpy
    corr_np = np.load("data/pmcorr.npy")
    df_corr = pd.DataFrame(columns=['x','y','corr'])
    xs = []
    ys = []
    corrs = []
    for i_corr in range(len(corr_np)):
        for j_corr in range(len(corr_np)):
            xs.append(i_corr)
            ys.append(j_corr)
            corrs.append(corr_np[i_corr,j_corr])
    df_corr["x"] = xs
    df_corr["y"] = ys
    df_corr["corr"] = corrs
    corr_data = df_corr.to_dict(orient='records')
    corr_data = json.dumps(corr_data,indent=2)
    #multi line numpy

    multi_np = np.load("data/array_413.npy")
    df_multi = pd.DataFrame(columns=['x'])
    for s in range(multi_np.shape[1]):
        auto_corr = []
        tmp = 'a' + str(s)
        for i in range(1,80):
            ac = pd.Series(multi_np[:,s,3]).autocorr(lag=i)
            auto_corr.append(ac)
        df_multi[tmp]=auto_corr
    index_tmp = []
    for i in range(1,80):
        index_tmp.append(i)
    df_multi['x']=index_tmp
    multi_data = df_multi.to_dict(orient='records')
    multi_data = json.dumps(multi_data,indent=2)


    data = {'chart_data': chart_data,'records': records.to_dict(orient='records'), 'corr_data':corr_data, 'multi_data':multi_data}
    #data = {'chart_data': chart_data,'records': records.to_dict(orient='records'), 'corr_data':corr_data}

    return data


@app.route('/', methods=['GET', 'POST'])
def response():
    data=getting_data()
    if request.method == "POST":
        features = request.form.getlist('feature')#features = request.form['features']
        models = request.form.getlist('model')
        interpolations = request.form.getlist('interpolation')
        form_predict_date = request.form['trip-start']
        #with open('log/predict_date.pickle', 'wb') as handle:
        #    pickle.dump(predict_date, handle, protocol=pickle.HIGHEST_PROTOCOL)
        with open('data/sc.pickle', 'rb') as handle: sc = pickle.load(handle)
        with open('data/sc_val.pickle', 'rb') as handle: sc_val = pickle.load(handle)
        def get_colorname(acc):
            if acc<25.0:
                return "red"
            elif acc<50.0:
                return "orange"
            elif acc<75.0:
                return "yellow"
            else:
                return "green"

        def get_result(i,model_name,interpolation_name,predict_date):
            model=load_model('model/'+model_name+"/model"+str(i)+'.h5')
            #model.save('log/trained_model.h5')
            #getting accuracy
            X_val=np.load("data/npy/X_val_scaled.npy")
            Y_val=np.load("data/npy/Y_val_scaled.npy")
            pred=model.predict(X_val[:,:,i])
            pred=sc_val.inverse_transform(np.array([pred[:,0]]*5).T)[:,2]
            true=Y_val
            true=sc_val.inverse_transform(true)[:,3]
            mape=(np.mean(np.abs((true - pred) / true))) * 100

            #getting image
            tmpi=i#(0,1,3)
            #del model
            #model=load_model('model/'+"gru"+"/model"+str(tmpi)+'.h5')
            with open('data/sc2.pickle', 'rb') as handle: sc = pickle.load(handle)
            d0 = date(2019, 9, 5)
            d1 = date(int(predict_date[:4]), int(predict_date[5:7]),int(predict_date[-2:]))
            delta = d1 - d0
            pred_from_idx=delta.days*24
            pred_to_idx=pred_from_idx+24
            time_lag=24
            input_from_idx=pred_from_idx-time_lag+15
            input_to_idx=pred_to_idx-time_lag
            n_station=array.shape[1]


            if np.sum(np.isnan(array[input_from_idx:pred_to_idx]))==0:
                input_array=array[input_from_idx:input_from_idx+time_lag]
                input_array=sc.transform(input_array.reshape((-1,5))).reshape((-1,n_station,5))
                input_array=np.transpose(input_array,(1,0,2))
                pred=model.predict(input_array[:,:,tmpi])
                pred=sc.inverse_transform(np.array([pred[:,0]]*5).T)[:,3]
                sd=np.nanstd(array,axis=0)[:,3]
                gt=array[input_from_idx+time_lag:input_from_idx+time_lag+1,:,3][0]

                #interpolation
                r=500;c=700
                grid_array = np.empty((r, c))
                grid_array=grid_array*np.nan
                grid_array_sd=np.empty((r, c))*np.nan
                grid_array_gt=np.empty((r, c))*np.nan
                grid_array_res=np.empty((r, c))*np.nan
                for lt,lg,p,s,t in zip(lat,long,pred,sd,gt):
                    grid_array[int(lt),int(lg)]=p
                    grid_array_sd[int(lt),int(lg)]=s
                    grid_array_gt[int(lt),int(lg)]=t
                grid_array_res=np.abs(grid_array_gt-grid_array)
                xx, yy = np.meshgrid(np.arange(0,c), np.arange(0,r))

                #pred
                ma_array=np.ma.array(grid_array, mask=np.isnan(grid_array).astype('bool'))
                x1 = xx[~ma_array.mask]
                y1 = yy[~ma_array.mask]
                newarr = ma_array[~ma_array.mask]
                x_inter1=griddata((x1, y1), newarr.ravel(),(xx, yy),method=interpolation_name)
                x_inter1=np.flip(x_inter1,axis=0)
                cm = plt.get_cmap('CMRmap')#cm = plt.get_cmap('gist_rainbow')
                colored_image = cm(x_inter1/40)
                colored_image=toimage(colored_image, cmin=0, cmax=1)
                colored_image.putalpha(mask)
                colored_image_url='static/images/results/tmpcolored_image2.png'
                colored_image.save(colored_image_url)

                #sd
                ma_array=np.ma.array(grid_array_sd, mask=np.isnan(grid_array_sd).astype('bool'))
                newarr = ma_array[~ma_array.mask]
                x_inter1_sd=griddata((x1, y1), newarr.ravel(),(xx, yy),method=interpolation_name)
                x_inter1_sd=np.flip(x_inter1_sd,axis=0)
                cm = plt.get_cmap('spring')#cm = plt.get_cmap('gist_rainbow')
                colored_image = cm(x_inter1_sd/40)
                colored_image=toimage(colored_image, cmin=0, cmax=1)
                colored_image.putalpha(mask)
                #colored_image_url='static/images/results/'+str(i)+str(model_name)+predict_date+'.png'
                colored_image_url_sd='static/images/results/std/tmpcolored_image2.png'
                colored_image.save(colored_image_url_sd)

                #gt
                ma_array=np.ma.array(grid_array_gt, mask=np.isnan(grid_array_gt).astype('bool'))
                newarr = ma_array[~ma_array.mask]
                x_inter1_gt=griddata((x1, y1), newarr.ravel(),(xx, yy),method=interpolation_name)
                x_inter1_gt=np.flip(x_inter1_gt,axis=0)
                cm = plt.get_cmap('Greens')#cm = plt.get_cmap('gist_rainbow')
                colored_image = cm(x_inter1_gt/40)
                colored_image=toimage(colored_image, cmin=0, cmax=1)
                colored_image.putalpha(mask)
                colored_image_url_gt='static/images/results/gt/tmpcolored_image2.png'
                colored_image.save(colored_image_url_gt)

                #res
                ma_array=np.ma.array(grid_array_res, mask=np.isnan(grid_array_res).astype('bool'))
                newarr = ma_array[~ma_array.mask]
                x_inter1_res=griddata((x1, y1), newarr.ravel(),(xx, yy),method=interpolation_name)
                x_inter1_res=np.flip(x_inter1_res,axis=0)
                cm = plt.get_cmap('Greys')#cm = plt.get_cmap('gist_rainbow')
                colored_image = cm(x_inter1_res/40)
                colored_image=toimage(colored_image, cmin=0, cmax=1)
                colored_image.putalpha(mask)
                colored_image_url_res='static/images/results/res/tmpcolored_image2.png'
                colored_image.save(colored_image_url_res)


            else: colored_image_url="";colored_image_url_sd="";colored_image_url_gt="";colored_image_url_res=""

            K.clear_session()
            del model
            return [round(100-mape,2),get_colorname(100-mape),colored_image_url,colored_image_url_sd,colored_image_url_gt,colored_image_url_res]

        f_dict={'humi':0,'noise':1,'pm10':2,'pm25':3,'temp':4}
        m_dict={'lstm':0,'gru':1}
        idx=[f_dict[i] for i in features]
        idx.sort();idx=tuple(idx)

        if models[0]!="lstm" and models[0]!="gru":
            a=0;c="black"
        else:
            a,c,resultimg,resultimg_sd,resultimg_gt,resultimg_res=get_result(idx,models[0],interpolations[0],form_predict_date)
        with open('log/records.pickle', 'rb') as handle:
                records = pickle.load(handle)
        for f in features:
            records=pd.concat((records,pd.DataFrame({'from':f,'to':[models[0]],'style':[c],'weight':[0.5],'acc':[a]})),axis=0)
        records=records.drop_duplicates(subset=['from', 'to','style','weight','acc'])
        with open('log/records.pickle', 'wb') as handle:
            pickle.dump(records, handle, protocol=pickle.HIGHEST_PROTOCOL)
        data=getting_data()
        data["records"]=records.to_dict(orient='records')

        #resultimg="/static/images/tmpresult.png"
        result_seoul=pd.DataFrame({"pred":[resultimg],"sd":[resultimg_sd],"gt":[resultimg_gt],"res":[resultimg_res]})#pd.DataFrame({"pred":["tmpresult.png"]})
        data["result_seoul"]=result_seoul.to_dict(orient='records')
        return  render_template("indexva.html", data=data)

    return  render_template("indexva.html", data=data)

@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


if __name__ == "__main__":
    f=["pm10"]*6+["pm25"]*6+["noise"]*6+["humi"]*6+["temp"]*6
    t=(["lstm"]+["gru"]+["arima"]+["ha"]+["convlstm"]+["dcrnn"])*5
    w=[0.5]*30
    a=[0.0]*30
    s=['color:#111;'+'opacity: 0.0;']*30#["None"]*150#["#fdbf6f",'#a6cee3','#fb9a99']*50#
    records = pd.DataFrame({"from":f,  "to":t, "weight":w, "style":s,"acc":a})
    #interpolation
    f=["lstm"]*4+["gru"]*4+["arima"]*4+["ha"]*4+["convlstm"]*4+["dcrnn"]*4
    t=(["RBFnet"]+["nearest"]+["linear"]+["cubic"])*6
    w=[0.5]*24
    a=[0.0]*24
    s=['color:#111;'+'opacity: 0.0;']*24#["None"]*150#["#fdbf6f",'#a6cee3','#fb9a99']*50#
    records_inter = pd.DataFrame({"from":f,  "to":t, "weight":w, "style":s,"acc":a})
    records=pd.concat((records,records_inter),axis=0)

    with open('log/records.pickle', 'wb') as handle:
        pickle.dump(records, handle, protocol=pickle.HIGHEST_PROTOCOL)

    location=pd.read_csv('data/location_seoul_413.csv')
    array=np.load("data/npy/array_413.npy")
    r=500;c=700
    sc1=MinMaxScaler(feature_range=(0,r-1))
    lat=sc1.fit_transform((location['lat'].values).reshape((-1,1))).flatten()
    sc2=MinMaxScaler(feature_range=(0,c-1))
    long=sc2.fit_transform((location['long'].values).reshape((-1,1))).flatten()
    mask = Image.open("static/images/mask.png")

    app.run(host='127.0.0.1', port=5000,debug=True,use_reloader=False)
