import pandas as pd
from scipy import stats
import numpy as np
import impyute as impy

########## imputation

def custom_imp_min(df):
    min_value = df.min()
    output = df.fillna(min_value)
    return output

def custom_imp_max(df):
    max_value = df.max()
    output = df.fillna(max_value)
    return output

def custom_imp_mean(col_name, df):
    temp = impy.mean(df.values)
    output = pd.DataFrame(temp, columns = [col_name])
    return output

def custom_imp_median(col_name, df):
    temp = impy.median(df.values)
    output = pd.DataFrame(temp, columns = [col_name])
    return output

def custom_imp_em(col_name, df):
    temp = impy.em(df.values, loops = 50)
    output = pd.DataFrame(temp, columns = [col_name])
    return output

def custom_imp_locf(col_name, df):
    temp = impy.locf(df.values, axis = 1)
    output = pd.DataFrame(temp, columns = [col_name])
    return output
