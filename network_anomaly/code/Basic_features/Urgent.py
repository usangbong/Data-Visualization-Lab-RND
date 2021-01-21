# -*- coding:utf-8 -*-

import pandas as pd
import csv
import collections


# from pandas import DataFrame as df

def Urgent(new_data, data):
    # data = pd.read_csv("../../dataset/test_younggil.csv", sep='|', dtype='unicode', names=['no', 'time', 'protocol', 'text description', 'srcip', 'dstip', 'total pkt length', 'L4 payload hexdump'])  # 'no','time','highest protocol(L4 protocol)','text description','srcipaddress:srcport','dst ip address:dst port','total pkt length','L4 payload hexdump')
    URG_list = []

    for i in range(len(new_data)):
        URG_list.append(data['URG on'][i])

    Urgent = pd.DataFrame(URG_list, columns=['Urgent'])

    return Urgent


if __name__ == '__main__':
    pass