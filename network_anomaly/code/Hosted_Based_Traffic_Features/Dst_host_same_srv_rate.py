# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 18:07:21 2019

@author: KJH
"""

import pandas as pd
import csv
import collections
from pandas import DataFrame as df


def Dst_host_same_srv_rate(target):
    
    data = pd.read_csv(target, sep='|', dtype = 'unicode', names = ['no','time','protocol','text description','srcip','dstip','total pkt length','L4 payload hexdump'])#'no','time','highest protocol(L4 protocol)','text description','srcipaddress:srcport','dst ip address:dst port','total pkt length','L4 payload hexdump')
    counter_same_src = collections.Counter(data['dstip'])
    data
    new_data = data['dstip']#IP랑 Port 묶여있음
    
    new_data = pd.DataFrame(new_data)
    
    
    IP_PORT_COUNT = []
    
    for i in range(len(new_data)):
        IP_PORT_COUNT.append(counter_same_src[new_data.iloc[i][0]])
        #IP_PORT_COUNT(new_data.iloc[i][1])
        
    df_IP_PORT_COUNT = pd.DataFrame(IP_PORT_COUNT, columns = ['IP_PORT_COUNT'])
    split = data.dstip.str.split(':')
    split = split.apply(lambda x: pd.Series(x))
    split.columns = ["dstIP","dport"]
    counter_IP=collections.Counter(split["dstIP"]) #같은 목적지 ip 개수
    counter_IP_list = [(k,counter_IP[k]) for k in counter_IP]
    
    
    IP_COUNT = []
    for i in range(len(new_data)):
        IP = new_data.iloc[i][0].split(':')[0]
        IP_COUNT.append(counter_IP[new_data.iloc[i][0].split(':')[0]])
        
    df_IP_COUNT = pd.DataFrame(IP_COUNT, columns = ['IP_COUNT'])
        
    
    temp = pd.concat([df_IP_PORT_COUNT, df_IP_COUNT],axis=1)
    result_temp = pd.concat([new_data,temp],axis=1)
    #print(result_temp)
    
    result = df.drop_duplicates(result_temp)
    
    # print(result)
    rate_result = result["IP_PORT_COUNT"]/result["IP_COUNT"]
    print(rate_result)
