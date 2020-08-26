import sys
import os
import csv
import cv2
import numpy as np
import math

# fovea
FOVEA = 1
FOVEA_PX = FOVEA * 45
data_path = './processed_data_tobii'
dataFile_list = os.listdir(data_path)
STI_WIDTH = 1920
STI_HEIGHT = 1080

def checkFoveaRange(_fovea, _x, _y, _c, _r):
    _flag = False
    if (_x-_c)*(_x-_c) + (_y-_r)*(_y-_r) < _fovea*_fovea:
        _flag = True
    
    return _flag

def create_dir(_dirpath):
    try:
        if not os.path.exists(_dirpath):
            os.makedirs(_dirpath)
    except OSError:
        print("Error: creating directory."+_dirpath)

output_dir_path = './gaze_features'
create_dir(output_dir_path)
fileCount = 0
for _dataFilePath in dataFile_list:
    fileCount += 1
    # if fileCount != 7:
    #     continue
    _filePath = data_path + "/" + _dataFilePath
    print(_filePath)
    
    rf = open(_filePath, 'r', encoding='utf-8')
    rdr = csv.reader(rf)
    rowsInFile = []
    _t = True
    for _row in rdr:
        if _t:
            _t = False
            continue
        rowsInFile.append(_row)
    rf.close()

    output_file_path = output_dir_path + "/" + _filePath
    
    _center = []
    _cont_c = []
    _cont_i = []
    _cont_o = []
    _hog = []
    _horizontal = []
    _log = []
    _sm = []
    _sm_c = []
    _sm_i = []
    _sm_o = []

    _stiFeaturesPath = "./sti_features/"
    _featureType = os.listdir(_stiFeaturesPath)
    _contrastType = ["color", "intensity", "orientation"]
    _smType = ["color", "intensity", "orientation", "sm"]
    for num in range(0, len(_featureType)):
        print(num)
        _fPath = ""
        if num == 1:
            for _type in _contrastType:
                _fPath = _stiFeaturesPath + _featureType[num] + "/" + _dataFilePath.split("_")[4] + "_" + _dataFilePath.split("_")[5][:-4] + "_" + _type + ".csv"
                
                rf = open(_fPath, 'r' , encoding='utf-8')
                rdr = csv.reader(rf)
                _arr = []
                for _row in rdr:
                    _arr.append(_row)
            
                for _p in rowsInFile:
                    _x = int(math.trunc(float(_p[1])))
                    _y = int(math.trunc(float(_p[2])))
                    if _x >= STI_WIDTH or _y >= STI_HEIGHT or _x < 0 or _y < 0:
                        continue
                    #print("%d, %d"%(_x, _y))
                    _aggre = []
                    
                    for _r in range(0, len(_arr)):
                        if _r < _y-(FOVEA_PX+5) or _r > _y+FOVEA_PX+5:
                            continue
                        for _c in range(0, len(_arr[_r])):
                            if _c < _x-(FOVEA_PX+5) or _c > _x+FOVEA_PX+5:
                                continue
                            if checkFoveaRange(FOVEA_PX, _x, _y, _c, _r):
                                _v = float(_arr[_r][_c])
                                _aggre.append(_v)
                                
                    _avgVal = 0
                    _count = 0
                    for _f in _aggre:
                        _avgVal += _f
                        _count += 1
                    _avgVal = _avgVal/_count

                    if _type == _contrastType[0]:
                        _cont_c.append(_avgVal)
                    elif _type == _contrastType[1]:
                        _cont_i.append(_avgVal)
                    elif _type == _contrastType[2]:
                        _cont_o.append(_avgVal)
        
        elif num == 5:
            for _type in _smType:
                _fPath = _stiFeaturesPath + _featureType[num] + "/" + _dataFilePath.split("_")[4] + "_" + _dataFilePath.split("_")[5][:-4] + "_" + _type + ".csv"
        
                rf = open(_fPath, 'r' , encoding='utf-8')
                rdr = csv.reader(rf)
                _arr = []
                for _row in rdr:
                    _arr.append(_row)
            
                for _p in rowsInFile:
                    _x = int(math.trunc(float(_p[1])))
                    _y = int(math.trunc(float(_p[2])))
                    if _x >= STI_WIDTH or _y >= STI_HEIGHT or _x < 0 or _y < 0:
                        continue
                    _aggre = []
                    
                    for _r in range(0, len(_arr)):
                        if _r < _y-(FOVEA_PX+5) or _r > _y+FOVEA_PX+5:
                            continue
                        for _c in range(0, len(_arr[_r])):
                            if _c < _x-(FOVEA_PX+5) or _c > _x+FOVEA_PX+5:
                                continue
                            if checkFoveaRange(FOVEA_PX, _x, _y, _c, _r):
                                _v = float(_arr[_r][_c])
                                _aggre.append(_v)
                    
                    _avgVal = 0
                    _count = 0
                    for _f in _aggre:
                        _avgVal += _f
                        _count += 1
                    _avgVal = _avgVal/_count

                    if _type == _smType[0]:
                        _sm_c.append(_avgVal)
                    elif _type == _smType[1]:
                        _sm_i.append(_avgVal)
                    elif _type == _smType[2]:
                        _sm_o.append(_avgVal)
                    elif _type == _smType[3]:
                        _sm.append(_avgVal)
            
        else:
            _fPath = _stiFeaturesPath + _featureType[num] + "/" + _dataFilePath.split("_")[4] + "_" + _dataFilePath.split("_")[5][:-4] + ".csv"
    
            rf = open(_fPath, 'r' , encoding='utf-8')
            rdr = csv.reader(rf)
            _arr = []
            for _row in rdr:
                _arr.append(_row)
        
            for _p in rowsInFile:
                _x = int(math.trunc(float(_p[1])))
                _y = int(math.trunc(float(_p[2])))
                if _x >= STI_WIDTH or _y >= STI_HEIGHT or _x < 0 or _y < 0:
                    continue
                _aggre = []
                for _r in range(0, len(_arr)):
                    if _r < _y-(FOVEA_PX+5) or _r > _y+FOVEA_PX+5:
                        continue
                    for _c in range(0, len(_arr[_r])):
                        if _c < _x-(FOVEA_PX+5) or _c > _x+FOVEA_PX+5:
                            continue
                        if checkFoveaRange(FOVEA_PX, _x, _y, _c, _r):
                            _v = float(_arr[_r][_c])
                            _aggre.append(_v)
                
                _avgVal = 0
                _count = 0
                for _f in _aggre:
                    _avgVal += _f
                    _count += 1
                _avgVal = _avgVal/_count

                if num == 0:
                    _center.append(_avgVal)
                elif num == 2:
                    _hog.append(_avgVal)
                elif num == 3:
                    _horizontal.append(_avgVal)
                elif num == 4:
                    _log.append(_avgVal)
    # if fileCount == 7:
    #     print("center_bias")
    #     print(len(_center))
    #     print(_center)
    #     print("c_c")
    #     print(len(_cont_c))
    #     print(_cont_c)
    #     print("c_i")
    #     print(len(_cont_i))
    #     print(_cont_i)
    #     print("c_o")
    #     print(len(_cont_o))
    #     print(_cont_o)
    #     print("hog")
    #     print(len(_hog))
    #     print(_hog)
    #     print("horizontal")
    #     print(len(_horizontal))
    #     print(_horizontal)
    #     print("log")
    #     print(len(_log))
    #     print(_log)
    #     print("sm_c")
    #     print(len(_sm_c))
    #     print(_sm_c)
    #     print("sm_i")
    #     print(len(_sm_i))
    #     print(_sm_i)
    #     print("sm_o")
    #     print(len(_sm_o))
    #     print(_sm_o)
    #     print("sm")
    #     print(len(_sm))
    #     print(_sm)
    out_gf_path = output_dir_path + "/" + _dataFilePath
    wf = open(out_gf_path, "w", newline='', encoding='utf-8')
    wdr = csv.writer(wf)
    _t = True
    _idx = 0
    
    for _p in rowsInFile:
        _x = int(math.trunc(float(_p[1])))
        _y = int(math.trunc(float(_p[2])))
        if _x >= STI_WIDTH or _y >= STI_HEIGHT or _x < 0 or _y < 0:
            continue
        
        if _t:
            _t = False
            wdr.writerow(["t", "x", "y", "center_bias", "c_c", "c_i", "c_o", "hog", "horizontal", "log", "sm_c", "sm_i", "sm_o", "sm"])
        _x = _p[1]
        _y = _p[2]
        
        wdr.writerow([str(_idx), _x, _y, str(_center[_idx]), str(_cont_c[_idx]), str(_cont_i[_idx]), str(_cont_o[_idx]), str(_hog[_idx]), str(_horizontal[_idx]), str(_log[_idx]), str(_sm_c[_idx]), str(_sm_i[_idx]), str(_sm_o[_idx]), str(_sm[_idx])])
        _idx += 1
    wf.close()




                        



                


    









#print(dataFile_list)
#img = np.zeros((STI_HEIGHT, STI_WIDTH, 3), np.uint8)
#img = cv2.line(img, (0,0), (1919, 1079), (255,0,0), 5)
#img = cv2.circle(img, (960, 540), 40, (255, 0, 0), -1)
#img = cv2.circle(img, (960, 540), 1, (0, 0, 0), -1)
# _c = 0
# for _dataFilePath in dataFile_list:
#     _filePath = data_path + "/" + _dataFilePath    
#     rf = open(_filePath, 'r', encoding='utf-8')
#     rdr = csv.reader(rf)
#     rowsInFile = []
#     for _row in rdr:
#         rowsInFile.append(_row)
#     rf.close()

#     if _c == 3:
#         i = 0
#         for _p in rowsInFile:
#             if i==0:
#                 i += 1
#                 continue
#             if i==6:
#                 break
#             _x = float(_p[1])
#             _y = float(_p[2])
#             #img = cv2.rectangle(img, (_x, _y-10), (_x, _y+10), (255, i*50, 0))
#             #img = cv2.rectangle(img, (_x-10, _y), (_x+10, _y), (255, i*50, 0))
#             img = cv2.circle(img, (int(_x), int(_y)), 5, (255, 255, 255), -1)
#             i += 1
#     _c += 1
#cv2.imshow('image', img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()