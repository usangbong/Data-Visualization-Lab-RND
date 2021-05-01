import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import csv
import json
import pandas as pd
import os
import glob
import datetime

# pow 파일 load
dir_path    = "C:/Users/VISLAB_PHY/Desktop/WORKSPACE/DATA/pow_24/UR00000126_csv"
file_list   = os.listdir(dir_path)
print(len(file_list))
hrPow  = []    
for file in file_list:
    filedata = pd.read_csv(dir_path+'/'+file).values[:,0]
    hrPow.append(filedata)        
pow_dataset = pd.DataFrame(hrPow)

print(pow_dataset)
# 23시 data 쌓이지 않으므로 0으로 채움
pow_dataset[23] = 0

# 결측값 보간, reshape
pow_dataset = pow_dataset.interpolate(method='linear')
pow_dataset = pow_dataset.values.reshape(-1,1)
pow_dataset = pd.DataFrame(pow_dataset)
pow_dataset.columns = ['pow']

# save csv file
pow_dataset.to_csv("C:/Users/VISLAB_PHY/Desktop/WORKSPACE/DATA/pow.csv",mode='w',index=False)