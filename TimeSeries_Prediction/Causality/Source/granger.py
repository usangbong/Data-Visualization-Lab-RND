import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
from statsmodels.tsa.stattools import grangercausalitytests
from pandas import read_csv

'''
Calculate granger causality
Save csv file (p-value & lag)
'''

# get min value (val>0)
def minExceptZero(iterator, threshold = 0):
    minvalue = float('inf')
    for x in iterator:
        if (x > threshold) and (x < minvalue):
            minvalue = x
    if minvalue==float('inf'):
        minvalue=0
    return minvalue

### get granger causality (val, idx)
maxlag = 10
def grangers_causation_matrix(data, variables, test='ssr_chi2test', verbose=False):    
    df_val = pd.DataFrame(np.zeros((len(variables), len(variables))), columns=variables, index=variables)
    df_idx = pd.DataFrame(np.zeros((len(variables), len(variables))), columns=variables, index=variables)
    count  = 1

    for c in df_val.columns:
        start = time.time()
        print(count, c, '\t', sep='\t', end='')

        for r in df_val.index:
            if(r==c):
                continue;
            test_result = grangercausalitytests(data[[r, c]], maxlag=maxlag, verbose=False)
            p_values = [round(test_result[i+1][0][test][1],4) for i in range(maxlag)]
            if verbose: print(f'Y = {r}, X = {c}, P Values = {p_values}')
                
            min_p_val = minExceptZero(p_values)#np.min(temp[temp>0])
            min_p_idx = p_values.index(min_p_val)
            df_val.loc[r, c] = min_p_val
            df_idx.loc[r, c] = min_p_idx

        count += 1
        end = time.time()
        print(end-start)
    
    df_val.to_csv(file_path+"/granger_pval.csv",mode='w',index=True)
    df_idx.to_csv(file_path+"/granger_lag.csv",mode='w',index=True)
    return df_val


### load csv data
file_path = './data/'
file_name = '_csv_metr-la.csv'

dataset = read_csv(file_path + file_name, encoding='CP949')
dataset = dataset.drop(['Unnamed: 0'], axis=1)
print(file_path, file_name, dataset.shape)

### granger cuasality test
#g_matrix_df=dataset.iloc[:,0:5]
o = grangers_causation_matrix(dataset, variables = dataset.columns)