import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
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

#pow 낮값만 추출 test
#pow = 0인 구간 : 0~4, 21-23시
powhr_start = 5
powhr_end   = 20

shift_days  = 3
hoursteps   = powhr_end-powhr_start+1 #(16)
timesteps   = shift_days*hoursteps #hours step

data_dim    = 15
out_dim     = 1
n_model     = 10
facltyCapacty = 200000

load_path = 'C:/solar/pow_24/'
save_path = 'C:/Users/VISLAB_PHY/Desktop/D_WORKSPACE/Data/'
save_name = '210504'

date_start = '10100901'
date_end   = '30191201'

err_date_list = ['20190912','20191122','20191130','20191217','20200501',
                 '20200502','20191028','20191107','20191108','20191109',
                 '20191110','20191111','20191112','20200214','20200307',
                 '20200308','20200309','20200310','20200328','20200329',
                 '20200625','20200809','20201003','20201029','20201226','20201227','20201228','20201229']
# pow 파일 load
dir_path = 'C:/solar/pow_24/UR00000126_csv'
file_list   = os.listdir(dir_path)
print(len(file_list))
hrPow  = []    

# pow측정값 에러가 큰 일자 제거
for filename in file_list:
    if (filename[:-4] not in err_date_list):
        if ((filename[:-4]>=date_start) & (filename<date_end)):
            filedata = pd.read_csv(dir_path+'/'+filename).values[:,0]
            hrPow.append(filedata)
            #print(filename[:-4])


#낮시간 추출 (5~20시)
pow_dataset = pd.DataFrame(hrPow)
pow_dataset[23] = 0# 23시 data 쌓이지 않으므로 0으로 채움
pow_dataset =pow_dataset.iloc[:,powhr_start:powhr_end+1]
pow_dataset.to_csv(save_path+"/pow_test_"+save_name+".csv",mode='w',index=False)

# 결측값 보간, reshape
pow_dataset = pow_dataset.interpolate(method='linear')
pow_dataset = pow_dataset.values.reshape(-1,1)
pow_dataset = pd.DataFrame(pow_dataset)
pow_dataset.columns = ['pow']
pow_dataset.to_csv(save_path+"/pow_"+save_name+".csv",mode='w',index=False)


# scale
sc_pow = MinMaxScaler(feature_range = (0, 1))
scaled_pow = sc_pow.fit_transform(pow_dataset.values)
df_pow = pd.DataFrame(scaled_pow, columns=pow_dataset.columns, index=list(pow_dataset.index.values))

#get test data
X_test = np.load("npset/"+save_name+"_testX.npy")
y_test = np.load("npset/"+save_name+"_testY.npy")

#get pow scale form
#powdata, scaler = libs_yeon.get_pow()

print("X_test : ", X_test.shape)
print("y_test : ", y_test.shape)

n_dataset   = y_test.shape[0]
acc_list    = []
acc_model   = []
predictModel = []
predErrRate_list_test = []
predList=[]
yList=[]
for i in range(n_model):
    predictModel.append(load_model('model/model_'+save_name+'_'+str(i)+'.h5'))
    acc_model.append(0)
    
print("[ dataset ]")
for m in range(n_model):
#for m in range(2):
    plot_target=[]
    plot_predict=[]
    for i in range(n_dataset):
    #for i in range(5):
    #if(i in [2,3,4,5,6,7,8]): continue;
        y = sc_pow.inverse_transform(y_test[i:i+1,:,0])

        #print("(model",m+1,")\t",end="")

        pred = predictModel[m].predict([X_test[i:i+1]])
        pred[pred<0] = 0
        pred = pred[:,:,0]
        pred = sc_pow.inverse_transform(pred)
        predSum = np.sum(pred)
            
        predList = pred.reshape(-1,1)
        yList = y.reshape(-1,1)
        for hr in range(0, hoursteps):
            predTest   = predList[hr]
            targetTest = yList[hr]
            differenceTest = np.abs(targetTest-predTest)
            predErrRateTest = np.round(differenceTest/facltyCapacty*100, 2)
            plot_target.append(targetTest)
            plot_predict.append(predTest)

            #print("|t:",target,"-p:",pred,"|=",err,",예측오차율:",predErrRate)
            #err_list.append(err)
            predErrRate_list_test.append(predErrRateTest)
        
        target      = round(np.sum(y), 2)
        error       = round(np.abs(target-predSum), 2)
        error_rate  = np.min([round(error/target, 2),1])
        acc_rate    = round((1.0-error_rate)*100, 2)
        acc_list.append(acc_rate)
        acc_model[m] += acc_rate

        #print("   pred: ",pred," | target: ",target," | error: ",error," | err rate: ",error_rate," | acc: ",acc_rate,sep="")
    #print("acc rate: ",np.mean(acc_list[-n_model:]),sep='')
    print(np.mean(acc_list[-n_model:]), " / ",sep='', end='')

    # target, predict 비교차트 찍기
    plt.title(str(m)+" Model")
    plt.plot(plot_target, label="TARGET VALUE",linewidth=3)#,linewidth=4, alpha=0.7)
    plt.plot(plot_predict,label="PREDICT VALUE",linewidth=3)#,linewidth=2, alpha=1)
    plt.rcParams['font.size'] = 20
    #plt.figure(figsize=(30,4))
    plt.gcf().set_size_inches(30, 5, forward=True)
    #plt.rcParams["figure.figsize"] = (30,4)
    # step_test=hoursteps*10
    # for i in range(0, n_dataset, step_test):
    #     plt.plot(plot_target[i:i+step_test], label="TARGET VALUE",linewidth=3)#,linewidth=4, alpha=0.7)
    #     plt.plot(plot_predict[i:i+step_test],label="PREDICT VALUE",linewidth=3)#,linewidth=2, alpha=1)
    plt.grid()
    plt.legend()
    #plt.show()
    plt.savefig(save_path+'/predict_'+str(m)+'model.jpg')
    plt.clf()
print("\n----------------------------------------------")
print("mean(acc rate): ",np.mean(acc_list),sep='')
print("----------------------------------------------")
print("[ model ]")
for i in range(n_model):
    acc_model[i] = round(acc_model[i]/(n_dataset),2)
    print(acc_model[i])