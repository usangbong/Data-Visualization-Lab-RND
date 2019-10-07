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

      
def _wrap_index__in_verbose(iterations):
    """Yields the values in iterations printing the status on the stdout."""
    m = len(iterations)
    digits = len(str(m))
    progress = '\r [ {s:{d}} / {m} ] {s:3.0f}% - ? it/s'
    progress = progress.format(m=m, d=digits, s=0)
    stdout.write(progress)
    beginning = time()
    for i, it in enumerate(iterations):
        yield it
        it_per_sec = (i+1) / ((time() - beginning) + float_info.min)
        sec_left = ((m-i) / float(it_per_sec))
        time_left = str(timedelta(seconds=sec_left))[:7]
        progress = '\r [ {i:{d}} / {m} ]'.format(i=i+1, d=digits, m=m)
        progress += ' {p:3.0f}%'.format(p=100*(i+1)/m)
        progress += ' - {it_per_sec:4.2f} it/s'.format(it_per_sec=it_per_sec)
        progress += ' - {time_left} left '.format(time_left=time_left)
        stdout.write(progress)
     
      
def fast_norm(x):
    """Returns norm-2 of a 1-D numpy array.
    * faster than linalg.norm in case of 1-D arrays (numpy 1.9.2rc1).
    """
    return sqrt(dot(x, x.T))
  
