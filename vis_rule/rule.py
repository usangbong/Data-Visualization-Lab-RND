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

def decompositionDataset(_filename):
	_summary = []

	# read csv file
	csv_reader = pd.read_csv(_filename)
	# get numbers of row & col
	numberOfRow = csv_reader.shape[0]
	numberOfCol = csv_reader.shape[1]
	dataset = np.array(csv_reader)

	_summary.append(dataset)
	_summary.append(numberOfRow)
	_summary.append(numberOfCol)

	_types = []
	for i in range(0, numberOfCol):
		_types.append(str(type(dataset[0][i])))

	_summary.append(_types)
	return _summary

def typeDeterminant(_rowNum, _val):
	remove_dup = list(set(_val))
	if _rowNum == len(remove_dup) or len(remove_dup) > 30:
		return MEASURE
	else:
		return DIMENSION

def countingType(_keys):
	# 0: Dimension, 1: Measure
	_counting = [0, 0]
	for i in range(len(_keys)):
		if _keys[i] == DIMENSION:
			_counting[0] += 1
		else:
			_counting[1] += 1
	return _counting

def visType(_d, _m):
	_vis = []
	if _d == 0 and _m == 2:
		_vis.append("scatter")
		_vis.append("heatmap")
	elif _d == 1 and _m == 1:
		_vis.append("bar")
		_vis.append("line")
		_vis.append("pie")
	elif _d == 1 and _m == 2:
		_vis.append("bar")
		_vis.append("line")
	elif _d == 1 and _m == 3:
		_vis.append("bar")
		_vis.append("line")
	elif _d == 2 and _m == 0:
		_vis.append("scatter")
		_vis.append("heatmap")
	elif _d == 2 and _m == 1:
		_vis.append("scatter")
	else:
		_vis.append("scatter")
	return _vis
