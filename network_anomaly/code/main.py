# -*- coding: utf-8 -*-

import Basic_Features 
from Content_Related_Features import *
from Time_Related_Traffic_Features import *
from Hosted_Based_Traffic_Features import *

    
import pandas as pd
import csv
import collections
from pandas import DataFrame as df


def make_new_data(data):
    
    # data['time'] -> object에서 float으로 변형, 초단위로 자름
    data['TIME'] = data['time'].astype('float')
    data['TIME_SEC'] = data['TIME'].astype('int')
    
    

    # SRC -> IP, PORT, IP_PORT 분리
    SRC_IP = []
    SRC_PORT =[]
    SRC_IP_PORT =[]
    
    for i in range(len(data)):
        SRC_IP.append(data['srcip'][i].split(':')[0])
        SRC_PORT.append(data['srcip'][i].split(':')[1])
        SRC_IP_PORT.append(data['srcip'][i])
        
        
        
    # DST -> IP, PORT, IP_PORT 분리
    DST_IP = []
    DST_PORT = []
    DST_IP_PORT = []
    
    for i in range(len(data)):
        DST_IP.append(data['dstip'][i].split(':')[0])
        DST_PORT.append(data['dstip'][i].split(':')[1])
        DST_IP_PORT.append(data['dstip'][i])
        
        
        
    # merge new_data
    new_data = pd.DataFrame({
            'TIME' : data['TIME'],          # object에서 float으로 변형된 시간 값
            'TIME_SEC' : data['TIME_SEC'],  # TIME을 초단위로 바꿈
            'SRC_IP': SRC_IP,               # 출발지 IP
            'SRC_PORT': SRC_PORT,           # 출발지 PORT
            'SRC_IP_PORT': SRC_IP_PORT,     # 출발지 IP:PORT
            'DST_IP': DST_IP,               # 도착지 IP
            'DST_PORT': DST_PORT,           # 도착지 PORT
            'DST_IP_PORT': DST_IP_PORT,     # 도착지 IP:PORT
            'PROTOCOL': data['protocol']
            })
    
    return new_data


if __name__ == '__main__':    # 프로그램의 시작점일 때만 아래 코드 실행
    
    # import data
    data = pd.read_csv("../dataset/test_younggil.csv", sep='|', dtype='unicode', names=['no', 'time', 'protocol', 'text description', 'srcip', 'dstip', 'ver.', 'totallength', 'IP id', 'IP Flags','TTL','URG on','total pkt length', 'L4 payload hexdump'])  # 'no','time','highest protocol(L4 protocol)','text description','srcipaddress:srcport','dst ip address:dst port','total pkt length','L4 payload hexdump')
    
    # transform new_data
    new_data = make_new_data(data)
    
    # timestamp에 각 초에 따른 데이터를 넣어줌
#    timestamp_IP_PORT = []
#    for i in range((max(new_data['TIME'])+1)):
#        line = []
#        timestamp_IP_PORT.append(line)
#    
#    for j in range(len(new_data['TIME'])):
#        timestamp_IP_PORT[new_data['TIME'].iloc[j]].append(new_data['IP_PORT'].iloc[j])
#    
#    # timestamp를 이용해서 counter에 각 초당 IP&PORT 개수를 저장함
#    counter_IP_PORT = []
#    for k in range(len(timestamp_IP_PORT)):
#        counter_IP_PORT.append(collections.Counter(timestamp_IP_PORT[k]))
#    
#    timestamp_IP = []
#    
#    # 초단위로 바꾼 값 중의 최대값 크기만큼의 (timestamp)리스트를 만듦
#    for i in range((max(new_data['TIME']))+1):
#        line = []
#        timestamp_IP.append(line)
#    
#    
#    
#    # (timestamp)안에 각 초단위에 해당하는 dstip를 리스트형태로 넣음
#    # 아래 코드 실행 후 timestamp[0:2] 로 출력하면 0초,1초에 대한 dstip 출력
#    for j in range(len(new_data['TIME'])):
#    
#        timestamp_IP[new_data['TIME'].iloc[j]].append(new_data['IP'].iloc[j])
#    # f.write(str(timestamp_IP)) 테스트
#    
#    
#    # timestamp를 이용해서 counter에 각 초당 IP&PORT 개수를 저장함
#    counter_IP = []
#    for k in range(len(timestamp_IP)):
#        counter_IP.append(collections.Counter(timestamp_IP[k]))
#    
#    timestamp_PORT = []
#    # 초단위로 바꾼 값 중의 최대값 크기만큼의 (timestamp)리스트를 만듦
#    for i in range((max(new_data['TIME']))+1):
#        line = []
#        timestamp_PORT.append(line)
#    
#    # (timestamp)안에 각 초단위에 해당하는 dstip를 리스트형태로 넣음
#    # 아래 코드 실행 후 timestamp[0:2] 로 출력하면 0초,1초에 대한 dstip 출력
#    for j in range(len(new_data['TIME'])):
#        # print(data['time'].iloc[j])
#        timestamp_PORT[new_data['TIME'].iloc[j]].append(new_data['PORT'].iloc[j])
#    
#    counter_PORT = []
#    for k in range(len(timestamp_PORT)):
#        counter_PORT.append(collections.Counter(timestamp_PORT[k]))
#    
    
#    print("counter_IP_PORT")
#    print (counter_IP_PORT)
    
    """
    구현해야 할 Features
    """
    
    # Feature_1
    
    
    
    # Featrue_2
    Protocol_type = Basic_Features.Protocol_type(new_data)
    print("Protocol_type : ", Protocol_type)
    
    
    # Feature_3
    # Feature_4
    # Feature_5
    # Feature_6
    
    # Feature_7 : Land
    Land = Basic_Features.Land(new_data)
    print("land : ", Land)
    
    # Feature_8
    # Feature_9
    Urgent = Basic_Features.Urgent(new_data, data)
    print("Urgent : ", Urgent)


    # Feature_10
    # Featrue_11
    # Feature_12
    