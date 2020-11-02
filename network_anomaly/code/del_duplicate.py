# -*- coding: utf-8 -*-

def del_duplicate(ip_combine):
    ip_combine = list(set(ip_combine))
    ip_combine_temp = []
    del ip_combine[0]
#     print(len(ip_combine))
    for i in range(len(ip_combine)):
        ip1, ip2 = ip_combine[i].split(":")
        if ip2+":"+ip1 not in ip_combine_temp:
            ip_combine_temp.append(ip_combine[i])
#     print(len(ip_combine_temp))
    return ip_combine_temp