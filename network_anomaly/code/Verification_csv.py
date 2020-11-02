# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 15:39:24 2019

@author: KJH
"""

import pandas as pd
import csv
import numpy as np

fix_data = pd.read_csv("Train_Set1_Split/fixed_network_train_set1_00008.csv", sep=',') #fix된 데이터 경로
origin_data = pd.read_csv("Train_Set1_Split/network_train_set1_00008.csv", sep=',', warn_bad_lines=False, error_bad_lines=False) #원본데이터 경로 

fix_data = fix_data.fillna(-1)#fix data에 있는 nan 값을 -1로 변경
origin_data = origin_data.fillna(-1) #origin data에 있는 nan 값을 -1로 변경
np_fdata = fix_data.values
np_odata = origin_data.values
# np_fdata.shape
x = np.delete(np_fdata, (-1), axis=0) #fix data 마지막 줄 삭제(why? 마지막줄은 origin data에 없기때문)
def nan_equal(a,b):
        try:
             np.testing.assert_equal(a,b)
        except AssertionError:
            return False
        return True
print(nan_equal(x,np_odata))