# python version 3.5x
import datetime
import numpy as np
import pandas as pd
import sys
import csv

visType = ["heat map", "bar chart", "line chart", "tree map"]
colTypes = ["<class 'str'>", "<class 'char'>", "<class 'int'>", "<class 'float'>", "<class 'double'>", "<class 'bool'>", "<class 'NoneType'>", "<class 'datetime.datetime'>"]

filename = "./test.csv"
dataSummary = []

KEYS = []
KEYS_COUNT = []
VIS = []
DIMENSION = "D"
MEASURE = "M"
