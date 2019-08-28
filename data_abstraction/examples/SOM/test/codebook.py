import numpy as np
import scipy as sp

from sklearn.decomposition import PCA
#from sklearn.decomposition import RandomizedPCA# (randomizedpca is deprecated)
from .decorators import timeit

class InvalidNodeIndexError(Exception):
    pass


class InvalidMapsizeError(Exception):
    pass

def generate_hex_lattice(n_rows, n_columns):
    x_coord = []
    y_coord = []
    for i in range(n_rows):
        for j in range(n_columns):
            x_coord.append(i*1.5)
            y_coord.append(np.sqrt(2/3)*(2*j+(1+i)%2))
    coordinates = np.column_stack([x_coord, y_coord])
    return coordinates
