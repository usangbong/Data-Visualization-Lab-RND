# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 15:35:58 2019

@author: KJH
"""
def fixed_csv(path):
    count = 0
    train_path, train_dirs, train_files = next(os.walk(path))
    train_files.sort()
    for i in range(len(train_files)):
        if "csv" in train_files[i]:
            if "fixed" not in train_files[i]:
                try:
                    pd.read_csv(train_path + "/" + train_files[i])
                    print(train_files[i] , ": Successfully completed!!") 
                except Exception as e:
                    count += 1
                    #print("Error Opening CSV...be under repair....")
                    error_split = str(e).strip().split(' ')
                    err_num = error_split[10].split(',')
                    int_num = int(err_num[0]) - 1
                    with open(train_path + "/" + train_files[i], 'r') as f1:
                        for p, line in enumerate(f1):
                            if p == int_num: #column의 개수가 22개 이상이라면
                                err_line = line.strip().split(',') #,기준으로 해당 라인을 나눈다
                                max_line = len(err_line) #에러난 라인의 columns 개수
                                a = err_line[21:max_line] #22개 columns에서 초과된 값들을 a 로 설정
                                a_21 = ' '.join(a).replace('""', " ") #초과된 값들을 하나로 만듦
                                error_line = err_line[0:21] + [a_21] #22개의 column에서 초과된 값 붙이기
                                error_line_list = []#에러라인에 쌍따움표 빼기
                                for n in error_line:
                                    a = n.replace('"','')
                                    error_line_list.append(a)
                                error_row = pd.DataFrame(error_line_list).transpose()
                                error_row.columns = ["_ws.col.UTCtime","_ws.col.Protocol","ip.src","ip.dst","tcp.srcport","tcp.dstport","tcp.len","tcp.seq","tcp.ack","udp.srcport","udp.dstport","udp.length","http.request.method","http.request.uri","http.user_agent","http.connection","http.host","http.response.code","http.server","http.content_type","http.content_length","http.cache_control"]
                                data = pd.read_csv(train_path + "/" +train_files[i], sep = ',', warn_bad_lines=False, error_bad_lines=False)
                                con_data = pd.concat([data, error_row], axis=0)
                                con_data.to_csv(train_path + "/" +"fixed_"+train_files[i], index = False)
                                #print(train_set1_path + "/" +"fixed_"+train_set1_files[i]+ "   Successfully repaired it!!")
                                print("fixed_"+train_files[i]+ "   Successfully repaired it!!")
        else:
            print(train_files[i],"is not csv_file")
    print("##### End #####  ->", count ,"files fixed")
    
# train_set1_path, train_set2_path
# ts = time.time()
# fixed_csv(train_set1_path)
# fixed_csv(train_set2_path)
# print(time.time() - ts)