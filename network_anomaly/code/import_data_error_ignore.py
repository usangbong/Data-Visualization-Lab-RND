# -*- coding: utf-8 -*-

def import_data_ignore_error(path):
    count = 0
    result = []
    train_path, train_dirs, train_files = next(os.walk(path))
    train_files.sort()
    for i in range(len(train_files)):
        if "csv" in train_files[i]:
            try:
                result.append(pd.read_csv(train_path + "/" + train_files[i], sep = ',', warn_bad_lines=False, error_bad_lines=False))
                print(train_files[i] , ": import") 
            except:
                print(train_files[i], " : passed")
                pass
        else:
            print(train_files[i],"is not csv_file")
    return result
            
# train_set1_path, train_set2_path
# ts = time.time()
# set1 = import_data_ignore_error(train_set1_path)
# set2 = import_data_ignore_error(train_set2_path)
# print(time.time() - ts)