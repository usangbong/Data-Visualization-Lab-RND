import vis
import datetime
import numpy as np
import pandas as pd
import sys
import csv
import itertools
import plotly.graph_objects as go
import plotly.express as px

class DataToVis :
	def __init__(self):
		self.DIMENSION = "D"
		self.MEASURE = "M"
		self.GEO = "G"
		self.colTypes = ["<class 'str'>", "<class 'char'>", "<class 'int'>", "<class 'float'>", "<class 'double'>", "<class 'bool'>", "<class 'NoneType'>", "<class 'datetime.datetime'>"]
		self.latStrlist = ["lat", "latitude"]
		self.lonStrlist = ["lon","long","longitude"]
		self.VIS = vis.VisFunctions()
		self.htmlFileIndex = 0
		self.htmlFileNames = []
		self.arrDMIdx = []
		self.visCallArr = []
		self.visTypeArr= []
		self.optflag = True
		self.visflag = True
		
	def getFilename_Visfunc(self) :
		return self.htmlFileNames, self.visTypeArr
		
	def decompositionDataset(self,_filename):
		_summary = []
		# read csv file
		csv_reader = pd.read_csv(_filename)
		
		columnsLabels = np.array(csv_reader.columns)
		# get numbers of row & col
		numberOfRow = csv_reader.shape[0]
		numberOfCol = csv_reader.shape[1]
		dataset = np.array(csv_reader)
		_summary.append(dataset)
		_summary.append(numberOfRow)
		_summary.append(numberOfCol)
		_types = []
		for i in range(0, numberOfCol):
			if str(type(dataset[0][i])) == "<class 'float'>" :
				latflag = False
				lonflag = False
				for _str in self.latStrlist:
					if columnsLabels[i].lower() == _str.lower():
						latflag=True
						break
						
				for _str in self.lonStrlist:
					if columnsLabels[i].lower() == _str.lower():
						lonflag=True
						break
				
				if latflag==True : 
					_types.append("latitude")
				elif lonflag==True:
					_types.append("longitude")
				else :
					_types.append(str(type(dataset[0][i])))
			else :
				_types.append(str(type(dataset[0][i])))
		_summary.append(_types)
		
		return _summary
		
	def typeDeterminant(self,_rowNum, _val):
		#remove_dup = list(set(_val))
		#if _rowNum ==( len(remove_dup) or len(remove_dup) ) > 30:
		#	return self.MEASURE
		#else:
		#	return self.DIMENSION
		return self.MEASURE
		
	def dim_measure_combinations(self,keys):
		idx_dim = []
		idx_measure = []
		t=[]
		for idx in range(len(keys)):
			if keys[idx]=="D" :
				idx_dim.append(idx)
			else :
				idx_measure.append(idx)
		d = []
		m = []
		d.append(list(map(''.join, itertools.combinations(idx_dim, 1))))
		d.append(list(map(''.join, itertools.combinations(idx_dim, 2))))
		m.append(list(map(''.join, itertools.combinations(idx_measure, 1))))
		m.append(list(map(''.join, itertools.combinations(idx_measure, 2))))
		m.append(list(map(''.join, itertools.combinations(idx_measure, 3))))
		return d, m
		
	def dim_measure_permutations(self,keys):
		idx_dim = []
		idx_measure = []
		idx_geo = []
		t=[]
		for idx in range(len(keys)):
			if keys[idx]==self.DIMENSION :
				idx_dim.append(idx)
			elif  keys[idx]==self.MEASURE :
				idx_measure.append(idx)
			elif  keys[idx]==self.GEO :
				idx_geo.append(idx)
		d = []
		d.append([])
		d.append(list( itertools.permutations(idx_dim, 1)))
		d.append(list( itertools.permutations(idx_dim, 2)))
		m=[]
		m.append([])
		m.append(list( itertools.permutations(idx_measure, 1)) )
		m.append(list( itertools.permutations(idx_measure, 2)) )
		m.append(list( itertools.permutations(idx_measure, 3)) )
		
		g = []
		g.append(idx_geo)
		return d, m, g
		
	def check_vis(self,_idx_d, _idx_m, dimIdxArr, meaIdxArr, _arrColumn, _arrData, _pdDataset) :
		#def check_vis(i, j, _d, _idx_m, _arrColumn, _arrData, _pdDataset) :
		#def check_vis(i, j, _d, _m, _arrColumn, _arrData, _pdDataset) :
		vistype = []
		if _idx_d == 0 and _idx_m == 2:
			vistype.append("scatter")
			vistype.append("heatmap")
			vistype.append("1dhistogram")
			vistype.append("cumulate_histogram")
		elif _idx_d == 1 and _idx_m == 1:
			vistype.append("bar")
			vistype.append("pie")
		elif _idx_d == 1 and _idx_m == 2:
			vistype.append("bar")
			vistype.append("overlay_histogram")
		elif _idx_d == 1 and _idx_m == 3:
			vistype.append("bar_line")	
			vistype.append("md_histogram")
		elif _idx_d == 2 and _idx_m == 0:
			vistype.append("scatter")
			vistype.append("heatmap")
		else:
			return
		for _type in vistype :
			self.visFuncCall(_type, _idx_d, _idx_m, dimIdxArr[_idx_d], meaIdxArr[_idx_m], _arrColumn, _arrData, _pdDataset)

	def check_staticVis(self, dimIdxArr, meaIdxArr, _arrColumn, _arrData, _pdDataset) :
		self.visStaticsFuncCall("rangeAndAverage", dimIdxArr, meaIdxArr, _arrColumn, _arrData, _pdDataset)
		self.visStaticsFuncCall("statisticalViolin", dimIdxArr, meaIdxArr, _arrColumn, _arrData, _pdDataset)
		self.visStaticsFuncCall("statisticalSplitViolin", dimIdxArr, meaIdxArr, _arrColumn, _arrData, _pdDataset)
		self.visStaticsFuncCall("parrallelCoord", dimIdxArr, meaIdxArr, _arrColumn, _arrData, _pdDataset)
		self.visStaticsFuncCall("pcaView", dimIdxArr, meaIdxArr, _arrColumn, _arrData, _pdDataset)
		self.visStaticsFuncCall("tsneView", dimIdxArr, meaIdxArr, _arrColumn, _arrData, _pdDataset)
		self.visStaticsFuncCall("3DtsneView", dimIdxArr, meaIdxArr, _arrColumn, _arrData, _pdDataset)
		
	def visStaticsFuncCall(self, _vistype, _dimIdxArr, _meaIdxArr, _arrColumn, _arrData, _pdDataset) :
		self.htmlFileNames.append("vis%d"%(self.htmlFileIndex))
		self.arrDMIdx.append([-3,1])
		self.visTypeArr.append(_vistype)
		self.visCallArr.append([ _dimIdxArr, _meaIdxArr ])
		self.htmlFileIndex+=1
		
	def check_geovis(self, geoArr, _pdDataset) :
		self.geovisFuncCall("basicGeo", geoArr, _pdDataset)
		self.geovisFuncCall("densityMap", geoArr, _pdDataset)
		self.geovisFuncCall("geoHexBin", geoArr, _pdDataset)
		
	def check_geovis_with_measure(self, len_index, m_idx, geoArr, _arrColumn, _pdDataset) :
		if len_index == 1:
			self.geovisFuncCallwithMeasure("geoBubbleMapWorld", len_index, m_idx, geoArr, _arrColumn, _pdDataset)
			self.geovisFuncCallwithMeasure("geoMapLoc", len_index, m_idx, geoArr, _arrColumn, _pdDataset)
	
	def geovisFuncCallwithMeasure(self, _vistype, len_index, m_idx, geoArr, _arrColumn, _pdDataset) :
		for k in range(len(m_idx[len_index])):
			_measureIdx = m_idx[len_index][k][0]
			self.htmlFileNames.append("vis%d"%(self.htmlFileIndex))
			self.arrDMIdx.append([-2,_measureIdx])
			self.visTypeArr.append(_vistype)
			self.visCallArr.append(geoArr)
			self.htmlFileIndex+=1
			
	def geovisFuncCall(self, _vistype, geoArr, _pdDataset) :
		self.htmlFileNames.append("vis%d"%(self.htmlFileIndex))
		self.arrDMIdx.append([-1,-1])
		self.visTypeArr.append(_vistype)
		self.visCallArr.append(geoArr)
		
		self.htmlFileIndex+=1
		
		return
	def visFuncCall(self, _vistype, _idx_d, _idx_m, _dimIdxArr, _meaIdxArr, _arrColumn, _arrData, _pdDataset) :
		#print(_vistype, _idx_d, _idx_m, _dimIdxArr, _meaIdxArr)
		if _idx_d == 0 :
			for j in range(len(_meaIdxArr)) :
				tm = []
				for k in range(len(_meaIdxArr[j])):
					tm.append(_arrColumn[_meaIdxArr[j][k]])
				#print("%dd%dm_%s: " %(0,_idx_m, _vistype),tm)
				#self.VIS.vistypeDetection(_filename, _idx_d,_idx_m, _vistype, [], _meaIdxArr[j], _arrColumn, _arrData, _pdDataset)
				self.htmlFileNames.append("vis%d"%(self.htmlFileIndex))
				self.arrDMIdx.append([_idx_d,_idx_m])
				self.visTypeArr.append(_vistype)
				self.visCallArr.append([ [], _meaIdxArr[j] ])
				self.htmlFileIndex+=1
		elif _idx_m == 0 :
			for i in range(len(_dimIdxArr)) :
				td = []
				for k in range(len(_dimIdxArr[i])):
					td.append(_arrColumn[_dimIdxArr[i][k]])
				#print("%dd%dm_%s: " %(_idx_d, 0, _vistype),td)
				#self.VIS.vistypeDetection(_filename, _idx_d,_idx_m, _vistype, _dimIdxArr[i], [], _arrColumn, _arrData, _pdDataset)
				self.htmlFileNames.append("vis%d"%(self.htmlFileIndex))
				self.arrDMIdx.append([_idx_d,_idx_m])
				self.visTypeArr.append(_vistype)
				self.visCallArr.append([ _dimIdxArr[i], [] ])
				self.htmlFileIndex+=1
				
		for i in range(len(_dimIdxArr)) :
			for j in range(len(_meaIdxArr)) :
				td = []
				tm = []
				for k in range(len(_dimIdxArr[i])):
					td.append(_arrColumn[_dimIdxArr[i][k]])
				for k in range(len(_meaIdxArr[j])):
					tm.append(_arrColumn[_meaIdxArr[j][k]])
				#print("%dd%dm_%s: " %(_idx_d,_idx_m, _vistype),td, tm)
				#self.VIS.vistypeDetection(_filename, _idx_d,_idx_m, _vistype, _dimIdxArr[i], _meaIdxArr[j], _arrColumn, _arrData, _pdDataset)
				self.htmlFileNames.append("vis%d"%(self.htmlFileIndex))
				self.arrDMIdx.append([_idx_d,_idx_m])
				self.visTypeArr.append(_vistype)
				self.visCallArr.append([ _dimIdxArr[i], _meaIdxArr[j] ])
				self.htmlFileIndex+=1
		#print(self.htmlFileNames)
		
	def csvReadToDatasets(self,_filename) :
		f = open(_filename, 'r', encoding='utf-8')
		rdr = csv.reader(f)
		lineNum = 0
		_arrColumn = []
		_arrData =[]
		for line in rdr:
			if lineNum==0 :
				for i in line:
					_arrColumn.append(i)
					_arrData.append([])
			else :
				for i in range(len(line)):
					_arrData[i].append(line[i])
			lineNum+=1
		f.close()
		_pdDataset = pd.read_csv(_filename, index_col=0)
		return _arrColumn, _arrData, _pdDataset
		
	def DM_KeyChecker(self,_filename) :
		_key = []
		dataSummary = self.decompositionDataset(_filename)
		
		for c in range(dataSummary[2]):
			#print(dataSummary[3])
			if dataSummary[3][c] == self.colTypes[0]:
				_key.append(self.DIMENSION)
			elif dataSummary[3][c] =="latitude" or dataSummary[3][c] =="longitude" :
				_key.append(self.GEO)
			else:
				#print("!!!")
				_key.append(self.MEASURE)
		return _key
		
	def visChecker(self,_d, _m, _g, _arrColumn, _arrData, _pdDataset) :
		self.check_staticVis(_d, _m, _arrColumn, _arrData, _pdDataset)
		for i in range(len(_d)) :
			for j in range(len(_m)) :
				self.check_vis(i, j, _d, _m, _arrColumn, _arrData, _pdDataset)
				#print(_d, _m)
				
		if len(_g[0])==2 :
			self.check_geovis(_g[0], _pdDataset)
			for j in range(len(_m)) :
				self.check_geovis_with_measure(j, _m, _g[0], _arrColumn, _pdDataset)
		else :
			print("error!!!")
		
		
	def visualizationToHTMLsAndPngs(self, _arrVisType, _baseHtmlPath, _arrColumn, _arrData, _pdDataset) :
		#print(self.htmlFileNames)
		for _visType in _arrVisType :
			for i in range(len(self.htmlFileNames)):
				if self.visTypeArr[i]==_visType :
					tempFilename = _baseHtmlPath+"/"+self.htmlFileNames[i]
					#print(tempFilename, self.arrDMIdx[i][0], self.arrDMIdx[i][1], self.visTypeArr[i], self.visCallArr[i][0], self.visCallArr[i][1], _arrColumn, _arrData, _pdDataset)
					#print("test!!, ", self.visTypeArr[i])
					self.VIS.vistypeDetection(tempFilename, self.arrDMIdx[i][0], self.arrDMIdx[i][1], self.visTypeArr[i], self.visCallArr[i][0], self.visCallArr[i][1], _arrColumn, _arrData, _pdDataset)
					
			
	def printOptimizer(self) :
		temp = list(set(self.visTypeArr))
		print_str = "[1][optimizer]["+("success" if self.optflag else "fail")+"]"+str(temp)
		#print(self.visTypeArr)
		print(print_str)
		return temp
		
	def GenTotalVisHtml(self, file, baseHtmlPath):
		htmlArr_htmltype = ["<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"UTF-8\"><title>test</title></head><body>","<div id=\"include", "\"style=\"border: 1px solid gold; float: left; width: 16%;\"></div>","<script type=\"text/javascript\" src=\"http://code.jquery.com/jquery-1.11.0.min.js\"></script><script type=\"text/javascript\">$(document).ready(function(){", "$(\"#include","\").load(\"resource/", "\"); ","});</script></body></html>"]

		htmlArr_pngtype = ["<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"UTF-8\"><title>test</title></head><body>","<div id=\"include", "\"style=\"border: 1px solid gold; float: left; width: 33%;height:30%;\"></div>","<script type=\"text/javascript\" src=\"http://code.jquery.com/jquery-1.11.0.min.js\"></script><script type=\"text/javascript\">$(document).ready(function(){", "document.getElementById('include","').innerHTML = '<img src=\"./resource/",".png\">';","});</script></body></html>"]

		html_str=""
		html_str += htmlArr_pngtype[0]
		for i in range(len(file)):
			if i%3 == 0  :
				html_str+="<br>"
			html_str+=htmlArr_pngtype[1]
			html_str+=str(i)
			html_str+=htmlArr_pngtype[2]
		html_str += htmlArr_pngtype[3]
		for i in range(len(file)):
			html_str+=htmlArr_pngtype[4]
			html_str+=str(i)
			html_str+=htmlArr_pngtype[5]
			html_str+=file[i]
			html_str+=htmlArr_pngtype[6]
		html_str+=htmlArr_pngtype[7]
		
		try:
			html_file= open(baseHtmlPath+"/index.html","w")
			html_file.write(html_str)
		except OSError:
			self.visflag=False
		
		print_str = "[3][total visualization]["+("success" if self.visflag else "fail")+"]["+baseHtmlPath+"/index.html]"
		print(print_str)
		