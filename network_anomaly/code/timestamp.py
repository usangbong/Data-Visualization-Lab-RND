# -*- coding:utf-8 -*-
# 2초 단위 카운터

import pandas as pd
import csv
import collections
from pandas import DataFrame as df

data = pd.read_csv("./dataset/test_younggil.csv", sep='|', dtype='unicode',
                   names=['no', 'time', 'protocol', 'text description', 'srcip', 'dstip', 'total pkt length',
                          'L4 payload hexdump'])  # 'no','time','highest protocol(L4 protocol)','text description','srcipaddress:srcport','dst ip address:dst port','total pkt length','L4 payload hexdump')
data['time'] = data['time'].astype('float')
data['TIME'] = data['time'].astype('int')

# IP, PORT, IP_PORT 데이터셋 생성 -> new_data
new_data = data['dstip']
new_data = pd.DataFrame(new_data)
IP = []
PORT = []
dst = []
for i in range(len(new_data)):
    IP.append(new_data.iloc[i][0].split(':')[0])
    PORT.append(new_data.iloc[i][0].split(':')[1])

IP = pd.DataFrame(IP, columns=['IP'])
PORT = pd.DataFrame(PORT, columns=['PORT'])
dst = data['dstip'].values.tolist()
IP_PORT = pd.DataFrame(dst, columns=['IP_PORT'])

new_data = pd.concat([data['TIME'], IP], axis=1)
new_data = pd.concat([new_data, PORT], axis=1)
new_data = pd.concat([new_data, IP_PORT], axis=1)

# timestamp에 각 초에 따른 데이터를 넣어줌
timestamp_IP_PORT = []
for i in range((max(new_data['TIME'])+1)):
    line = []
    timestamp_IP_PORT.append(line)

for j in range(len(new_data['TIME'])):
    timestamp_IP_PORT[new_data['TIME'].iloc[j]].append(new_data['IP_PORT'].iloc[j])

# timestamp를 이용해서 counter에 각 초당 IP&PORT 개수를 저장함
counter_IP_PORT = []
for k in range(len(timestamp_IP_PORT)):
    counter_IP_PORT.append(collections.Counter(timestamp_IP_PORT[k]))

timestamp_IP = []

# 초단위로 바꾼 값 중의 최대값 크기만큼의 (timestamp)리스트를 만듦
for i in range((max(new_data['TIME']))+1):
    line = []
    timestamp_IP.append(line)



# (timestamp)안에 각 초단위에 해당하는 dstip를 리스트형태로 넣음
# 아래 코드 실행 후 timestamp[0:2] 로 출력하면 0초,1초에 대한 dstip 출력
for j in range(len(new_data['TIME'])):

    timestamp_IP[new_data['TIME'].iloc[j]].append(new_data['IP'].iloc[j])
# f.write(str(timestamp_IP)) 테스트


# timestamp를 이용해서 counter에 각 초당 IP&PORT 개수를 저장함
counter_IP = []
for k in range(len(timestamp_IP)):
    counter_IP.append(collections.Counter(timestamp_IP[k]))

timestamp_PORT = []
# 초단위로 바꾼 값 중의 최대값 크기만큼의 (timestamp)리스트를 만듦
for i in range((max(new_data['TIME']))+1):
    line = []
    timestamp_PORT.append(line)

# (timestamp)안에 각 초단위에 해당하는 dstip를 리스트형태로 넣음
# 아래 코드 실행 후 timestamp[0:2] 로 출력하면 0초,1초에 대한 dstip 출력
for j in range(len(new_data['TIME'])):
    # print(data['time'].iloc[j])
    timestamp_PORT[new_data['TIME'].iloc[j]].append(new_data['PORT'].iloc[j])

counter_PORT = []
for k in range(len(timestamp_PORT)):
    counter_PORT.append(collections.Counter(timestamp_PORT[k]))


print("counter_IP_PORT")
print (counter_IP_PORT)


# timestamp_IP -> 초 단위로 IP를 자름
# timestamp_PORT -> 초 단위로 PORT를 자름
# timestamp_IP_PORT -> 초 단위로 IP_PORT를 자름
#
#
# counter_IP -> 초 단위로 잘린 IP의 개수를 반환
# counter_PORT -> 초 단위로 잘린 IP의 개수를 반환
# counter_IP_PORT -> 초 단위로 잘린 IP의 개수를 반환