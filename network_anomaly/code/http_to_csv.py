import sys
from scapy.all import *
import pandas as pd
from pandas import DataFrame

CNT = 549#
p_list = list()



def run(target) :
    # try:
    pkt = rdpcap(target, count=CNT)
    # except MemoryError :
    # print ("M Error")
    # sys.exit()

    numPkt = len(pkt)

    print("Analyzing :"+ target)
    print("Total packet : %d\n" %numPkt)
    print('********', pkt)
    for packet in pkt:
        layer =packet.payload
        p_dict = dict()

        while layer:
            layerName = layer.name
            if layerName=="IP":
                p_dict["srcip"]  = layer.src
                p_dict["dstip"]  = layer.dst
            if layerName=="TCP":
                if layer.flags == 2 : flags = "SYN"
                p_dict["sport"] = layer.sport
                p_dict["dport"] = layer.dport
            if layerName == "Raw":
                result = processHTTP(layer.load)
                for k,j in result.items():
                    p_dict[k] = j

            layer = layer.payload
            # print(p_dict)

            if 'http' in p_dict :
                p_list.append(p_dict)

    p_pandas = pd.DataFrame(p_list) # fillna()로 결측값 처리하기
    p_pandas.to_csv('./result.csv')

def processHTTP(data):
    info = dict()
    headers = str(data).splitlines();
    for header in headers :
        if header.startswith("GET",2):
            # print(header)
            info['http'] = "request"
            info['method'] = header.split()[0]
            info['uri'] = header.split()[1]

        if header.startswith('POST',2):
            info['http'] = "request"
            info['method'] = header.split()[0]
            info['uri'] = header.split()[1]

        if header.startswith('HTTP',2):
            info['http'] = "response"
            info['status'] = header.split()[1]
            info['content-type'] = header.split(":")[4].split("\\r\\n")[0]



        if 'Host' in header : info['host'] = header.split(":")[1].split("\\r\\n")[0]
        if 'User-Agent' in header: info['user-agnet'] = header.split(":")[2].split("\\r\\n")[0]
        # if 'Content-Type' in header: info['content-type'] = header.split(":")[4].split("\\r\\n")[0]
        # if header.startswith('User-Agent', 2): info['user-agent'] = header.split("\n")[1]

        # if header.startswith('User-Agent',2) : info['user-agent'] = header.split("\n")[0]
        # if header.startswith('Referer',2) : info['referer'] = header.split("\n")[0]
        # if header.startswith('Cookie',2) : info['cookies'] = header.split("\n")[0]

    return info


run("./test.pcap")


