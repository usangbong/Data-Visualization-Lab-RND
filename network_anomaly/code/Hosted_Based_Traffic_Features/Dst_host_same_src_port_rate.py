# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 20:10:27 2019

@author: KJH
"""
import pandas as pd
import csv
import collections
from pandas import DataFrame as df


def Dst_host_same_src_port_rate(target): #csv파일이 있는 위치를 target으로!

    
    new_data = pd.read_csv(target, sep='|', dtype = 'unicode', names = ['no','time','protocol','text description','srcip','dstip','total pkt length','L4 payload hexdump'])#'no','time','highest protocol(L4 protocol)','text description','srcipaddress:srcport','dst ip address:dst port','total pkt length','L4 payload hexdump')
    
    
    
    
    """dst IP와 Port split"""
    split_dst = new_data.dstip.str.split(':')
    split_dst = split_dst.apply(lambda x: pd.Series(x))
    split_dst.columns = ["dstIP","dport"]
    
    counter_DPort=collections.Counter(split_dst["dport"]) #같은 목적지 port 개수
    counter_DPort_list = [(k,counter_DPort[k]) for k in counter_DPort]
    counter_DPort = pd.DataFrame(counter_DPort_list, columns = ['dport','dport_count'])
    # display(counter_DPort)
    
    """src IP와 Port split"""
    
    split_src = data.srcip.str.split(':')
    split_src = split_src.apply(lambda x: pd.Series(x))
    split_src.columns = ["srcIP","sport"]
    
    counter_SPort=collections.Counter(split_src["sport"]) #같은 목적지 port 개수
    counter_SPort_list = [(k,counter_SPort[k]) for k in counter_SPort]
    counter_SPort = pd.DataFrame(counter_SPort_list, columns = ['sport','sport_count'])
    
    
    
    """dport와 sport가 같은 거 출력"""
    dport_same_sport = pd.concat([split_dst, split_src], axis=1)
    a = dport_same_sport.loc[dport_same_sport['dport'] == dport_same_sport['sport']]
    # display(a)
    a1=collections.Counter(a["sport"]) #같은 목적지 port 개수
    a_list = [(k,a1[k]) for k in a1]
    counter_SPort_DPort_same = pd.DataFrame(a_list, columns = ['dport','same_count'])
    # display(counter_SPort_DPort_same)#dport와 sport값이 같은 포트 개수
    
    
    
    """같은dport값의 개수와 sport와 dport가 같은 개수(이게뭔말이야..)"""
    result = pd.merge(counter_DPort, counter_SPort_DPort_same, on = 'dport', how='outer')
    #display(result.fillna(0))
    # display(b)
    
    """확률 계산"""
    rate_result = result["same_count"]/result["dport_count"]
    rate_result = rate_result.fillna(0)
    rate_result = pd.DataFrame(rate_result, columns=['rate'])
    rate_result = pd.concat([rate_result, result['dport']], axis=1)
    print(rate_result)
    