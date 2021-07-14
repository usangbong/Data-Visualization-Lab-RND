import numpy as np
import cv2
import csv
import os

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
# OUTDIR = "../output/vis_sti_feature/log_spectrum/"
# create_dir(OUTDIR)

# for dirname in dir_list:
#     _path = DIRPATH + dirname + "/"
#     if dirname == 'MIT1003':
#         _stiNameList = os.listdir(_path)
#         for _stiName in _stiNameList:
#             _stiPath = _path + _stiName
#             print(_stiPath)
#             img = cv2.imread(_stiPath, 0)
#             WIDTH = img.shape[1]
#             calc = int(WIDTH*img.shape[0]/img.shape[1])
#             img = cv2.resize(img, (WIDTH, calc))
#             c = cv2.dft(np.float32(img), flags = cv2.DFT_COMPLEX_OUTPUT)
#             mag = np.sqrt(c[:,:,0]**2 + c[:,:,1]**2)
#             spectralResidual = np.exp(np.log(mag) - cv2.boxFilter(np.log(mag), -1, (3,3)))
#             log_spectrum = np.log(mag)
            
#             csvPath = OUTDIR + dirname +"/"
#             create_dir(csvPath)
#             csvPath = csvPath + _stiName.split('.')[0]+".csv"
#             csvWriter(csvPath, log_spectrum)
#     else:
#         _stiClassList = os.listdir(_path)
#         for _stiClass in _stiClassList:
#             _stiPath = _path + _stiClass + "/"
#             _stiNameList = os.listdir(_stiPath)
#             for _stiName in _stiNameList:
#                 _stiPath = _path + _stiClass + "/" + _stiName
#                 print(_stiPath)
#                 img = cv2.imread(_stiPath, 0)
#                 WIDTH = img.shape[1]
#                 calc = int(WIDTH*img.shape[0]/img.shape[1])
#                 img = cv2.resize(img, (WIDTH, calc))
#                 c = cv2.dft(np.float32(img), flags = cv2.DFT_COMPLEX_OUTPUT)
#                 mag = np.sqrt(c[:,:,0]**2 + c[:,:,1]**2)
#                 spectralResidual = np.exp(np.log(mag) - cv2.boxFilter(np.log(mag), -1, (3,3)))
#                 log_spectrum = np.log(mag)
                
#                 csvPath = OUTDIR + dirname +"/"
#                 create_dir(csvPath)
#                 csvPath = csvPath + _stiClass +"/"
#                 create_dir(csvPath)
#                 csvPath = csvPath + _stiName.split('.')[0]+".csv"
#                 csvWriter(csvPath, log_spectrum)
# print("log spectrum feature extraction done")

_stiPath = "./nullschool.png"
csvPath = "./log_spectrum.csv"

img = cv2.imread(_stiPath, 0)
WIDTH = img.shape[1]
calc = int(WIDTH*img.shape[0]/img.shape[1])
img = cv2.resize(img, (WIDTH, calc))
c = cv2.dft(np.float32(img), flags = cv2.DFT_COMPLEX_OUTPUT)
mag = np.sqrt(c[:,:,0]**2 + c[:,:,1]**2)
spectralResidual = np.exp(np.log(mag) - cv2.boxFilter(np.log(mag), -1, (3,3)))
log_spectrum = np.log(mag)
csvWriter(csvPath, log_spectrum)
print("log spectrum feature extraction done")