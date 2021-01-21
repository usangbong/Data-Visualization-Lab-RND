# -*- coding:utf-8 -*-

import pandas as pd
import csv
import collections
#from pandas import DataFrame as df

def Land(new_data):
    #data = pd.read_csv("../../dataset/test_younggil.csv", sep='|', dtype='unicode', names=['no', 'time', 'protocol', 'text description', 'srcip', 'dstip', 'total pkt length', 'L4 payload hexdump'])  # 'no','time','highest protocol(L4 protocol)','text description','srcipaddress:srcport','dst ip address:dst port','total pkt length','L4 payload hexdump')
    Land_list = []
    for i in range(len(new_data)):
        count  = 0
        if new_data['SRC_IP_PORT'][i] == new_data['DST_IP_PORT'][i]:
            count += 1
        Land_list.append(count)
    Land = pd.DataFrame(Land_list, columns=['Land'])
    
    return Land

if __name__ == '__main__':
    pass