import cv2
import os
import csv

def create_dir(_dirpath):
    try:
        if not os.path.exists(_dirpath):
            os.makedirs(_dirpath)
    except OSError:
        print("Error: creating directory."+_dirpath)

def csvWriter(_data, _outputfilename):
    f = open(_outputfilename, 'w', newline='', encoding='utf-8')
    c = csv.writer(f)
    for _row in _data:
        c.writerow(_row)
    f.close()

DIRPATH = "../sti/"
dir_list = os.listdir(DIRPATH)

OUT_PATH = "../sti_features/horizontal_line/"
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

        # Load image, convert to grayscale, Otsu's threshold
        image = cv2.imread(_stiPath)
        if image is None:
            stiCount += 1
            dirChange += 1
            continue

        result = image.copy()
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # Detect horizontal lines
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40,1))
        detect_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
        cnts = cv2.findContours(detect_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            cv2.drawContours(result, [c], -1, (36,255,12), 2)

        # Detect vertical lines
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,10))
        detect_vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
        cnts = cv2.findContours(detect_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            cv2.drawContours(result, [c], -1, (36,255,12), 2)

        _meanMat = []
        for _row in result:
            _mean = []
            for _p in _row:
                _sVal = float(_p[0])+float(_p[1])+float(_p[2])
                _mVal = _sVal/3
                _mean.append(_mVal)
            _meanMat.append(_mean)
        csvWriter(_meanMat, csvPath)
        
        stiCount += 1
        dirChange += 1
print("horizontal-line feature extraction done")


# IMG_DIR = "../vs/"
# file_list = os.listdir(IMG_DIR)

# OUT_DIR = "./out/"
# create_dir(OUT_DIR)

# for IMG_NAME in file_list:
#     OUT_FULL_PATH = IMG_DIR+IMG_NAME
#     print(OUT_FULL_PATH)
#     # Load image, convert to grayscale, Otsu's threshold
#     image = cv2.imread(OUT_FULL_PATH)
#     if image is None:
#         continue
#     result = image.copy()
#     gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
#     thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

#     # Detect horizontal lines
#     horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40,1))
#     detect_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
#     cnts = cv2.findContours(detect_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     cnts = cnts[0] if len(cnts) == 2 else cnts[1]
#     for c in cnts:
#         cv2.drawContours(result, [c], -1, (36,255,12), 2)

#     # Detect vertical lines
#     vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,10))
#     detect_vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
#     cnts = cv2.findContours(detect_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     cnts = cnts[0] if len(cnts) == 2 else cnts[1]
#     for c in cnts:
#         cv2.drawContours(result, [c], -1, (36,255,12), 2)

#     _rMat = []
#     _gMat = []
#     _bMat = []
#     _sumMat = []
#     _meanMat = []
#     for _row in result:
#         _r = []
#         _g = []
#         _b = []
#         _sum = []
#         _mean = []
#         for _p in _row:
#             _r.append(float(_p[0]))
#             _g.append(float(_p[1]))
#             _b.append(float(_p[2]))
#             _sVal = float(_p[0])+float(_p[1])+float(_p[2])
#             _sum.append(_sVal)
#             _mVal = _sVal/3
#             _mean.append(_mVal)
#         _rMat.append(_r)
#         _gMat.append(_g)
#         _bMat.append(_b)
#         _sumMat.append(_sum)
#         _meanMat.append(_mean)

#     OUT_FULL_PATH = OUT_DIR+IMG_NAME[:-4]+"_horizon_r"+".csv"
#     csvWriter(_rMat, OUT_FULL_PATH)
#     OUT_FULL_PATH = OUT_DIR+IMG_NAME[:-4]+"_horizon_g"+".csv"
#     csvWriter(_gMat, OUT_FULL_PATH)
#     OUT_FULL_PATH = OUT_DIR+IMG_NAME[:-4]+"_horizon_b"+".csv"
#     csvWriter(_bMat, OUT_FULL_PATH)
#     OUT_FULL_PATH = OUT_DIR+IMG_NAME[:-4]+"_horizon_sum"+".csv"
#     csvWriter(_sumMat, OUT_FULL_PATH)
#     OUT_FULL_PATH = OUT_DIR+IMG_NAME[:-4]+"_horizon_mean"+".csv"
#     csvWriter(_meanMat, OUT_FULL_PATH)
# print("horizontal line feature extraction done")