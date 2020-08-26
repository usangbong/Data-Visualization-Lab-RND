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


DIRPATH = "../sti/"
dir_list = os.listdir(DIRPATH)

OUT_PATH = "../sti_features/log/"
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
        csvPath = OUT_PATH + dirname+ "_" + _sti[:-4] + ".csv"

        _stiPath = _path + _sti
        print(_stiPath)
        img = cv2.imread(_stiPath, 0)
        WIDTH = img.shape[1]
        calc = int(WIDTH*img.shape[0]/img.shape[1])
        img = cv2.resize(img, (WIDTH, calc))

        c = cv2.dft(np.float32(img), flags = cv2.DFT_COMPLEX_OUTPUT)
        mag = np.sqrt(c[:,:,0]**2 + c[:,:,1]**2)
        spectralResidual = np.exp(np.log(mag) - cv2.boxFilter(np.log(mag), -1, (3,3)))

        log_spectrum = np.log(mag)
        csvWriter(csvPath, log_spectrum)


        stiCount += 1
        dirChange += 1
print("log spectrum feature extraction done")



# IMG_DIR = "../vs/"
# file_list = os.listdir(IMG_DIR)

# OUT_DIR = "./out/"
# create_dir(OUT_DIR)

# IMG_DIR = "./vs/"

# for IMG_NAME in file_list:
#     IMG_FULL_PATH = IMG_DIR+IMG_NAME
#     img = cv2.imread(IMG_FULL_PATH, 0)

#     WIDTH = img.shape[1]
#     calc = int(WIDTH*img.shape[0]/img.shape[1])
#     img = cv2.resize(img, (WIDTH, calc))

#     c = cv2.dft(np.float32(img), flags = cv2.DFT_COMPLEX_OUTPUT)
#     mag = np.sqrt(c[:,:,0]**2 + c[:,:,1]**2)
#     spectralResidual = np.exp(np.log(mag) - cv2.boxFilter(np.log(mag), -1, (3,3)))

#     log_spectrum = np.log(mag)

#     OUTPUT_FULL_PATH = OUT_DIR+IMG_NAME[:-4]+"_log_spectrum.csv"
#     csvWriter(OUTPUT_FULL_PATH, log_spectrum)
# print("log spectrum feature extraction done")