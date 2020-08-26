import os
import csv
import cv2
import numpy as np
from skimage import img_as_float

import pySaliencyMap


def calc_features(_path):
    img = cv2.imread(_path)
    # initialize
    imgsize = img.shape
    img_width  = imgsize[1]
    img_height = imgsize[0]
    sm = pySaliencyMap.pySaliencyMap(img_width, img_height)

    # computation
    feature_intensity = sm.SMGetICM(img)
    feature_color = sm.SMGetCCM(img)
    feature_orientation = sm.SMGetOCM(img)
    feature_saliency_map = sm.SMGetOnlySM(img)

    intensity_res = img_as_float(feature_intensity)
    color_res = img_as_float(feature_color)
    orientation_res = img_as_float(feature_orientation)
    saliency_map_res = img_as_float(feature_saliency_map)

    _sfeatures = []
    _sfeatures.append(intensity_res)
    _sfeatures.append(color_res)
    _sfeatures.append(orientation_res)

    return _sfeatures

def create_dir(_dirpath):
    try:
        if not os.path.exists(_dirpath):
            os.makedirs(_dirpath)
    except OSError:
        print("Error: creating directory."+_dirpath)

def save_csv(_data, _csvfilename, _featureType):
    f = open(_csvfilename+"_"+_featureType+".csv", 'w', newline='', encoding='utf-8')
    c = csv.writer(f)
    for _row in _data:
        c.writerow(_row)
    f.close()

def getHighestVal(_data):
    _m = 0

    for _row in _data:
        for _p in _row:
            if _m < _p:
                _m = _p
    return _m

def calcContrastMat(_data, _mVal):
    _c_mat = []

    for _row in _data:
        _r_c = []
        for _p in _row:
            _v = _mVal-_p
            _r_c.append(_v)
        _c_mat.append(_r_c)

    return _c_mat

DIRPATH = "../sti/"
dir_list = os.listdir(DIRPATH)
FEATURESTYPE = ["intensity", "color", "orientation"]

OUT_PATH = "../sti_features/contrast/"
create_dir(OUT_PATH)

stiCount = 0
dirChange = 0
for dirname in dir_list:
    print(stiCount)
    if stiCount == 60:
        break
    _path = DIRPATH + dirname + "/"
    sti_list = os.listdir(_path)

    for _sti in sti_list:
        if dirChange != 0 and dirChange%3 == 0:
            dirChange = 0
            break
        _stiPath = _path + _sti
        print(_stiPath)
        
        csvPath = OUT_PATH + dirname+ "_" + _sti[:-4]
        
        s_f = calc_features(_stiPath)    
        mVals = []
        c_s_f = []

        for i in range(0, len(s_f)):
            mVals.append(getHighestVal(s_f[i]))

        for i in range(0, len(s_f)):
            c_s_f.append(calcContrastMat(s_f[i], mVals[i]))

        for i in range(0, len(s_f)):
            save_csv(c_s_f[i], csvPath, FEATURESTYPE[i])


        stiCount += 1
        dirChange += 1
print("contrast features extraction done")


# IMAGE_FILELIST = os.listdir(IMGDIR)

# for IMGFILENAME in IMAGE_FILELIST:
#     IMGPATH = IMGDIR+IMGFILENAME
#     s_f = calc_features(IMGPATH)

#     mVals = []
#     c_s_f = []
#     for i in range(0, len(s_f)):
#         mVals.append(getHighestVal(s_f[i]))

#     for i in range(0, len(s_f)):
#         c_s_f.append(calcContrastMat(s_f[i], mVals[i]))

#     for i in range(0, len(s_f)):
#         save_csv(c_s_f[i], csvSaveDir, IMGFILENAME[:-4], FEATURESTYPE[i])
# print("contrast features extraction done")