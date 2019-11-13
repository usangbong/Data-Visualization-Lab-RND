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

def possibleVis(_keysCount):
	_pv = []

	for i in range(_keysCount[0]+1):
		for j in range(_keysCount[1]+1):
			if i==0 and j <2:
				continue
			_v = visType(i, j)
			
			for v in range(len(_v)):
				_pv.append("%dd%dm-%s" %(i,j,_v[v]))
	return _pv

dataSummary = decompositionDataset(filename)

for c in range(dataSummary[2]):
	if dataSummary[3][c] == colTypes[0]:
		KEYS.append(DIMENSION)
	elif dataSummary[3][c] == colTypes[2]:
		_cols = []
		for r in range(dataSummary[1]):
			_cols.append(dataSummary[0][r][c])
		_k = typeDeterminant(dataSummary[1], _cols)
		KEYS.append(_k)
	else:
		KEYS.append(MEASURE)
		
print("-----DATASET-----")
print("dataset:")
print(dataSummary[0])
print("row len:")
print(dataSummary[1])
print("col len:")
print(dataSummary[2])
print("col data classes:")
print(dataSummary[3])
print("col data types:")
print(KEYS)
