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

"""
    Minimalistic implementation of the Self Organizing Maps (SOM).
"""

def _build_iteration_indexes(data_len, num_iterations,
                             verbose=False, random_order=False):
    """Returns an iterable with the indexes of the samples
    to pick at each iteration of the training."""
    iterations = arange(num_iterations) % data_len
    if random_order:
        random.shuffle(iterations)
    if verbose:
        return _wrap_index__in_verbose(iterations)
    else:
        return iterations
