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
    
IMG_DIR = "../vs/"
file_list = os.listdir(IMG_DIR)

OUT_DIR = "./out/"
create_dir(OUT_DIR)

for IMG_NAME in file_list:
    IMG_FULL_PATH = IMG_DIR+IMG_NAME
    i = Image.open(IMG_FULL_PATH)
    img_width, img_height = i.size

    # center max val = 10, min val = 0
    center_x = img_width/2.0
    center_y = img_height/2.0
    x_mv = 5.0/center_x
    y_mv = 5.0/center_y

    center_bias_mat = []
    for _c in range(0, img_width):
        _row = []
        for _r in range(0, img_height):
            _val = x_mv*_c + y_mv*_r
            _row.append(_val)
            
        center_bias_mat.append(_row)


    OUT_FULL_PATH = OUT_DIR+IMG_NAME[:-4]+"_center-bias.csv"

    csvWriter(OUT_FULL_PATH, center_bias_mat)
