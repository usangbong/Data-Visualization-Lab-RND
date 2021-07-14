import os
import csv
import numpy as np

import cv2
# https://elife-asu.github.io/PyInform/timeseries.html#id24
from pyinform import entropy_rate
from skimage import feature, filters, io, color


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


# DIRPATH = "../backup_full/"
# dir_list = os.listdir(DIRPATH)
# OUTDIR = "../output/vis_sti_feature/entropy_rate/"
# create_dir(OUTDIR)


# for dirname in dir_list:
#     _path = DIRPATH + dirname + "/"
#     if dirname == 'MIT1003':
#         _stiNameList = os.listdir(_path)
#         for _stiName in _stiNameList:
#             _stiPath = _path + _stiName
#             print(_stiPath)
#             csvPath = OUTDIR + dirname +"/"
#             create_dir(csvPath)
#             csvPath = csvPath + _stiName.split('.')[0]+".csv"
#             if os.path.isfile(csvPath):
#                 continue
#             img = cv2.imread(_stiPath, 0)
#             er = entropy_rate(img, k=2, local=True)
#             csvWriter(csvPath, er)
#     else:
#         _stiClassList = os.listdir(_path)
#         for _stiClass in _stiClassList:
#             _stiPath = _path + _stiClass + "/"
#             _stiNameList = os.listdir(_stiPath)
#             for _stiName in _stiNameList:
#                 _stiPath = _path + _stiClass + "/" + _stiName
#                 print(_stiPath)
#                 csvPath = OUTDIR + dirname +"/"
#                 create_dir(csvPath)
#                 csvPath = csvPath + _stiClass +"/"
#                 create_dir(csvPath)
#                 csvPath = csvPath + _stiName.split('.')[0]+".csv"
#                 if os.path.isfile(csvPath):
#                     continue
#                 img = cv2.imread(_stiPath, 0)
#                 er = entropy_rate(img, k=2, local=True)
#                 csvWriter(csvPath, er)
# print("curvature feature extraction done")

_stiPath = "./nullschool.png"
csvPath = "./entropy_rate.csv"
img = cv2.imread(_stiPath, 0)
er = entropy_rate(img, k=2, local=True)
csvWriter(csvPath, er)
print("curvature feature extraction done")