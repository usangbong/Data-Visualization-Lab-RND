import sys
import os
import csv
import math

STI_WIDTH = 1920
STI_HEIGHT = 1080

fDirPath = "./gaze_features"
fileList = os.listdir(fDirPath)
F_IDX = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
F_NAME = ["center-bias", "contrast_color", "contrast_intensity", "contrast_orientation", "HOG", "horizontal_line", "LOG_spectrum", "saliency_color", "saliency_intensity", "saliency_orientation", "computed_saliency"]

featureData = []
groupData = []
groupIdx = 1
fileCount = 0
print("load feature data from .csv files")
for _fIdx in F_IDX:
    groupIdx = 1

    # read feature values
    for _fileName in fileList:
        filePath = fDirPath + "/" + _fileName

        rf = open(filePath, 'r', encoding='utf-8')
        rdr = csv.reader(rf)
        
        _t = True
        for _row in rdr:
            if _t:
                _t = False
                continue
            # out of range error exception
            _x = int(math.trunc(float(_row[1])))
            _y = int(math.trunc(float(_row[2])))
            if _x >= STI_WIDTH or _y >= STI_HEIGHT or _x < 0 or _y < 0:
                continue
            groupData.append([float(_row[_fIdx]), groupIdx])
        rf.close()
        groupIdx += 1
        featureData.append(groupData)
        fileCount += 1
    
fileCount = fileCount/len(F_IDX)
print("loaded all feature data from %d number of .csv files"%fileCount)