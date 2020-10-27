#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def import_data(path):
    count = 0
    result = []
    train_path, train_dirs, train_files = next(os.walk(path))
    train_files.sort()
    for i in range(len(train_files)):
        if "csv" in train_files[i]:
            try:
                result.append(pd.read_csv(train_path + "/" + train_files[i]))
                print(train_files[i] , ": import") 
            except:
                print(train_files[i], " : passed")
                pass
        else:
            print(train_files[i],"is not csv_file")
    return result
            
# train_set1_path, train_set2_path
# ts = time.time()
# set1 = import_data(train_set1_path)
# set2 = import_data(train_set2_path)
# print(time.time() - ts)