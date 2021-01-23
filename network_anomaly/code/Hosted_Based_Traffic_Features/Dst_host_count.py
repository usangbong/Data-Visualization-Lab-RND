# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 18:07:21 2019

@author: KJH
"""

import pandas as pd
import csv
import collections

def Dst_host_count(target): #csv파일이 있는 위치를 target으로!
    data = pd.read_csv(target, sep='|', dtype = 'unicode', names = ['no','time','protocol','text description','srcip','dstip','total pkt length','L4 payload hexdump'])#'no','time','highest protocol(L4 protocol)','text description','srcipaddress:srcport','dst ip address:dst port','total pkt length','L4 payload hexdump')
    """목적지 IP와 Port 나누는 코드"""
    split = data.dstip.str.split(':')
    split = split.apply(lambda x: pd.Series(x))
    split.columns = ["dstIP","dstPort"]
    counter_IP=collections.Counter(split["dstIP"]) #같은 목적지 port 개수
    counter_IP_list = [(k,counter_IP[k]) for k in counter_IP]
    display(pd.DataFrame(counter_IP_list, columns=['dstIP','Dst_host_count']))
