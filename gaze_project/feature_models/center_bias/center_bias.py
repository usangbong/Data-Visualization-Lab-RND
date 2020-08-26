import os
import csv
from PIL import Image

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

OUT_PATH = "../sti_features/center_bias/"
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
        i = Image.open(_stiPath)

        img_width, img_height = i.size

        center_x = img_width/2.0
        center_y = img_height/2.0
        x_mv = 5.0/center_x
        y_mv = 5.0/center_y
        
        center_bias_mat = []
        for _r in range(0, img_height):
            _row = []
            for _c in range(0, img_width):
                _val = x_mv*_c + y_mv*_r
                _row.append(_val)
                
            center_bias_mat.append(_row)
        csvWriter(csvPath, center_bias_mat)
        stiCount += 1
        dirChange += 1
print("center-bias feature extraction done")
        

        





# IMG_DIR = "../sti/"
# file_list = os.listdir(IMG_DIR)

# OUT_DIR = "../sti_features/"
# create_dir(OUT_DIR)

# for IMG_NAME in file_list:
#     IMG_FULL_PATH = IMG_DIR+IMG_NAME
#     i = Image.open(IMG_FULL_PATH)
#     img_width, img_height = i.size

#     # center max val = 10, min val = 0
#     center_x = img_width/2.0
#     center_y = img_height/2.0
#     x_mv = 5.0/center_x
#     y_mv = 5.0/center_y

#     center_bias_mat = []
#     for _c in range(0, img_width):
#         _row = []
#         for _r in range(0, img_height):
#             _val = x_mv*_c + y_mv*_r
#             _row.append(_val)
            
#         center_bias_mat.append(_row)


#     OUT_FULL_PATH = OUT_DIR+IMG_NAME[:-4]+"_center-bias.csv"

#     csvWriter(OUT_FULL_PATH, center_bias_mat)
