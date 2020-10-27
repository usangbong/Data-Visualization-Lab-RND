# -*- coding: utf-8 -*-

def split_csv(matrix):
    ip_combine = matrix['ip.src'].str.cat(matrix['ip.dst'], sep=":")
#     ip_combine = list(set(ip_combine))
#     print(len(ip_combine))
    print("before : ",len(ip_combine))
    ip_combine = del_duplicate(ip_combine)
    print("after : " ,len(ip_combine))
    for i in range(len(ip_combine)):
        if type(ip_combine[i]) == str:
            src, dst = ip_combine[i].split(':')
            stream1 = matrix[(matrix['ip.src'] ==  src) & (matrix['ip.dst'] ==  dst)]
            stream2 = matrix[(matrix['ip.src'] ==  dst) & (matrix['ip.dst'] ==  src)]
            stream = pd.concat([stream1, stream2]).sort_index()
            #stream = stream.sort_index()
            stream.to_csv("./split1/"+ip_combine[i]+".csv")
            print("Done:",i,"/",len(ip_combine),src,":",dst)
            
# split_csv(matrix)