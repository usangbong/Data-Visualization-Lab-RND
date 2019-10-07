#https://github.com/JustGlowing/minisom/blob/master/minisom.py

from math import sqrt

from numpy import (array, unravel_index, nditer, linalg, random, subtract,
                   power, exp, pi, zeros, arange, outer, meshgrid, dot,
                   logical_and, mean, std, cov, argsort, linspace, transpose,
                   einsum, prod, where, nan)
from numpy import sum as npsum
from collections import defaultdict, Counter
from warnings import warn
from sys import stdout, float_info
from time import time
from datetime import timedelta
import pickle
import os

# for unit tests
from numpy.testing import assert_almost_equal, assert_array_almost_equal
from numpy.testing import assert_array_equal
import unittest
