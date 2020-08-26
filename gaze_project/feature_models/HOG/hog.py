# reference github address
# https://github.com/PENGZhaoqing/Hog-feature/blob/master/hog.py
import os
import csv
import cv2
import numpy as np
import math
import matplotlib.pyplot as plt


class Hog_descriptor():
    def __init__(self, img, cell_size=16, bin_size=8):
        self.img = img
        self.img = np.sqrt(img / float(np.max(img)))
        self.img = self.img * 255
        self.cell_size = cell_size
        self.bin_size = bin_size
        self.angle_unit = 360 / self.bin_size
        if self.isInt(self.angle_unit):
            self.angle_unit = int(self.angle_unit)
        assert type(self.bin_size) == int, "bin_size should be integer,"
        assert type(self.cell_size) == int, "cell_size should be integer,"
        assert type(self.angle_unit) == int, "bin_size should be divisible by 360"

    def isInt(self, x):
        if int(x) != x:
            return False
        else:
            return True

    def extract(self):
        height, width = self.img.shape
        gradient_magnitude, gradient_angle = self.global_gradient()
        gradient_magnitude = abs(gradient_magnitude)
        cell_gradient_vector = np.zeros((int(height / self.cell_size), int(width / self.cell_size), self.bin_size))
        for i in range(cell_gradient_vector.shape[0]):
            for j in range(cell_gradient_vector.shape[1]):
                cell_magnitude = gradient_magnitude[i * self.cell_size:(i + 1) * self.cell_size,
                                 j * self.cell_size:(j + 1) * self.cell_size]
                cell_angle = gradient_angle[i * self.cell_size:(i + 1) * self.cell_size,
                             j * self.cell_size:(j + 1) * self.cell_size]
                cell_gradient_vector[i][j] = self.cell_gradient(cell_magnitude, cell_angle)

        hog_image = self.render_gradient(np.zeros([height, width]), cell_gradient_vector)
        hog_vector = []
        for i in range(cell_gradient_vector.shape[0] - 1):
            for j in range(cell_gradient_vector.shape[1] - 1):
                block_vector = []
                block_vector.extend(cell_gradient_vector[i][j])
                block_vector.extend(cell_gradient_vector[i][j + 1])
                block_vector.extend(cell_gradient_vector[i + 1][j])
                block_vector.extend(cell_gradient_vector[i + 1][j + 1])
                mag = lambda vector: math.sqrt(sum(i ** 2 for i in vector))
                magnitude = mag(block_vector)
                if magnitude != 0:
                    normalize = lambda block_vector, magnitude: [element / magnitude for element in block_vector]
                    block_vector = normalize(block_vector, magnitude)
                hog_vector.append(block_vector)
        return hog_vector, hog_image

    def global_gradient(self):
        gradient_values_x = cv2.Sobel(self.img, cv2.CV_64F, 1, 0, ksize=5)
        gradient_values_y = cv2.Sobel(self.img, cv2.CV_64F, 0, 1, ksize=5)
        gradient_magnitude = cv2.addWeighted(gradient_values_x, 0.5, gradient_values_y, 0.5, 0)
        gradient_angle = cv2.phase(gradient_values_x, gradient_values_y, angleInDegrees=True)
        return gradient_magnitude, gradient_angle

    def cell_gradient(self, cell_magnitude, cell_angle):
        orientation_centers = [0] * self.bin_size
        for i in range(cell_magnitude.shape[0]):
            for j in range(cell_magnitude.shape[1]):
                gradient_strength = cell_magnitude[i][j]
                gradient_angle = cell_angle[i][j]
                min_angle, max_angle, mod = self.get_closest_bins(gradient_angle)
                orientation_centers[min_angle] += (gradient_strength * (1 - (mod / self.angle_unit)))
                orientation_centers[max_angle] += (gradient_strength * (mod / self.angle_unit))
        return orientation_centers

    def get_closest_bins(self, gradient_angle):
        idx = int(gradient_angle / self.angle_unit)
        mod = gradient_angle % self.angle_unit
        if idx == self.bin_size:
            return idx - 1, (idx) % self.bin_size, mod
        return idx, (idx + 1) % self.bin_size, mod

    def render_gradient(self, image, cell_gradient):
        cell_width = self.cell_size / 2
        max_mag = np.array(cell_gradient).max()
        for x in range(cell_gradient.shape[0]):
            for y in range(cell_gradient.shape[1]):
                cell_grad = cell_gradient[x][y]
                cell_grad /= max_mag
                angle = 0
                angle_gap = self.angle_unit
                for magnitude in cell_grad:
                    angle_radian = math.radians(angle)
                    x1 = int(x * self.cell_size + magnitude * cell_width * math.cos(angle_radian))
                    y1 = int(y * self.cell_size + magnitude * cell_width * math.sin(angle_radian))
                    x2 = int(x * self.cell_size - magnitude * cell_width * math.cos(angle_radian))
                    y2 = int(y * self.cell_size - magnitude * cell_width * math.sin(angle_radian))
                    cv2.line(image, (y1, x1), (y2, x2), int(255 * math.sqrt(magnitude)))
                    angle += angle_gap
        return image

def create_dir(_dirpath):
    try:
        if not os.path.exists(_dirpath):
            os.makedirs(_dirpath)
    except OSError:
        print("Error: creating directory."+_dirpath)

def csvWriter(_data, _outputfilename):
    f = open(_outputfilename, 'w')
    c = csv.writer(f, lineterminator='\n')
    for _row in _data:
        c.writerow(_row)
    f.close()

DIRPATH = "../sti/"
dir_list = os.listdir(DIRPATH)

OUT_PATH = "../sti_features/hog/"
create_dir(OUT_PATH)

stiCount = 0
dirChange = 0

for dirname in dir_list:
    if stiCount == 60:
        break
    _path = DIRPATH + dirname + "/"
    sti_list = os.listdir(_path)

    for _sti in sti_list:
        print(stiCount)
        if dirChange != 0 and dirChange%3 == 0:
            dirChange = 0
            break
        _stiPath = _path + _sti
        print(_stiPath)
        csvPath = OUT_PATH + dirname+ "_" + _sti[:-4] + ".csv"

        img = cv2.imread(_stiPath, cv2.IMREAD_GRAYSCALE)    
        hog = Hog_descriptor(img, cell_size=8, bin_size=8)
        vector, image = hog.extract()

        csvWriter(image, csvPath)

        stiCount += 1
        dirChange += 1
print("HOG feature extraction done")



# IMG_DIR = "F:/data/IEEEVIS2020/test/Ehinger_vs/"
# file_list = os.listdir(IMG_DIR)

# OUT_DIR = "./out/"
# create_dir(OUT_DIR)

# count = 1
# for IMG_NAME in file_list:
#     print("HOG: %d/%d - %s"%(count, len(file_list), IMG_NAME))
#     IMG_FULL_PATH = IMG_DIR+IMG_NAME
#     img = cv2.imread(IMG_FULL_PATH, cv2.IMREAD_GRAYSCALE)
#     hog = Hog_descriptor(img, cell_size=8, bin_size=8)
#     vector, image = hog.extract()

#     OUT_FULL_PATH = OUT_DIR+IMG_NAME[:-4]+"_hog.csv"
#     csvWriter(image, OUT_FULL_PATH)
#     count += 1

# #plt.imshow(image, cmap=plt.cm.gray)
# #plt.show()