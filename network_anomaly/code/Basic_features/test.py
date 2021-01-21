# -*- coding: utf-8 -*-

import pandas as pd
import csv
import collections
from pandas import DataFrame as df


def test(data):
    print(data['TIME'])
    return 100
#    data['TIME'] = data['TIME'].astype('float')
#    data['TIME'] = data['TIME'].astype('int')
#    
#    # IP, PORT, IP_PORT 데이터셋 생성 -> new_data
#    new_data = data['dstip']
#    new_data = pd.DataFrame(new_data)
#    IP = []
#    PORT = []
#    dst = []
#    land=[]
#    
#    dst = data['dstip'].values.tolist()
#    src = data['srcip'].values.tolist()
#    
#    
#    for i in range(len(new_data)):
#        IP.append(new_data.iloc[i][0].split(':')[0])
#        PORT.append(new_data.iloc[i][0].split(':')[1])
#    
#    for i in range(len(new_data)):
#        if src==dst:
#            land.append(1)
#        else:
#            land.append(0)
#    
#    
#    IP = pd.DataFrame(IP, columns=['IP'])
#    PORT = pd.DataFrame(PORT, columns=['PORT'])
#    IP_PORT = pd.DataFrame(dst, columns=['IP_PORT'])
#    LAND=pd.DataFrame(land,columns=['LAND'])
#    
#    
#    
#    new_data = pd.concat([data['TIME'], IP], axis=1)
#    new_data = pd.concat([new_data, PORT], axis=1)
#    new_data = pd.concat([new_data, IP_PORT], axis=1)
#    new_data = pd.concat([new_data,LAND],axis=1)
#    
#    
#    
#    # timestamp에 각 초에 따른 데이터를 넣어줌
#    timestamp_IP_PORT = []
#    for i in range((max(new_data['TIME']))+1):
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
#    return land

    
if __name__ == '__main__':
    pass