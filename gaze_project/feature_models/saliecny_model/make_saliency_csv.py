import os
import csv
import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage import img_as_float

import pySaliencyMap
import pySaliencyMapOriginal

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
    _sfeatures.append(saliency_map_res)

    return _sfeatures

def make_saliency_map(_path, _fname):
    img = cv2.imread(_path)
    # initialize
    imgsize = img.shape
    img_width  = imgsize[1]
    img_height = imgsize[0]
    sm = pySaliencyMapOriginal.pySaliencyMapOriginal(img_width, img_height)
    # computation
    saliency_map = sm.SMGetSM(img)
    
    cvtedImg = cv2.convertScaleAbs(saliency_map, alpha=(255.0))
    cv2.imwrite(_fname, cvtedImg)
    print("saliency map saved.")

def create_dir(_dirpath):
    try:
        if not os.path.exists(_dirpath):
            os.makedirs(_dirpath)
    except OSError:
        print("Error: creating directory."+_dirpath)

def create_dir(_dirpath):
    try:
        if not os.path.exists(_dirpath):
            os.makedirs(_dirpath)
    except OSError:
        print("Error: creating directory."+_dirpath)

def csvWriter(_outputfilename, _data):
    f = open(_outputfilename, 'w', newline='', encoding='utf-8')
    c = csv.writer(f)
    for _row in _data:
        c.writerow(_row)
    f.close()

FEATURESTYPE = ["intensity", "color", "orientation", "sm"]

DIRPATH = "../sti/"
dir_list = os.listdir(DIRPATH)

OUT_PATH = "../sti_features/saliency/"
create_dir(OUT_PATH)

stiCount = 0
dirChange = 0
for dirname in dir_list:
    if stiCount == 60:
        break
    _path = DIRPATH + dirname + "/"
    sti_list = os.listdir(_path)

    for _sti in sti_list:
        if dirChange != 0 and dirChange%3 == 0:
            dirChange = 0
            break
        else:
            print(stiCount)
        csvPath = OUT_PATH + dirname+ "_" + _sti[:-4]

        _stiPath = _path + _sti
        print(_stiPath)
        s_f = calc_features(_stiPath)

        for i in range(0, len(s_f)):
            OUT_FULL_PATH = csvPath+"_"+FEATURESTYPE[i]+".csv"
            csvWriter(OUT_FULL_PATH, s_f[i])
        stiCount += 1
        dirChange += 1
print("saliency features extraction done")
        


# FEATURESTYPE = ["intensity", "color", "orientation", "saliency_map"]

# #IMG_DIR = "../vs/"
# IMG_DIR = "F:/data/IEEEVIS2020/test/Ehinger_vs/"
# file_list = os.listdir(IMG_DIR)

# OUT_DIR = "./out/"
# create_dir(OUT_DIR)

# for IMG_NAME in file_list:
#     IMG_FULL_PATH = IMG_DIR+IMG_NAME
#     s_f = calc_features(IMG_FULL_PATH)

#     for i in range(0, len(s_f)):
#         OUT_FULL_PATH = OUT_DIR+IMG_NAME[:-4]+"_"+FEATURESTYPE[i]+".csv"
#         csvWriter(OUT_FULL_PATH, s_f[i])
# print("saliency features extraction done")