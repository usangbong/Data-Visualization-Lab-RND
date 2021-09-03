# python version 3.5x
import os
import argparse
import dataToVis as dv
import numpy as np

if __name__=='__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('datafile', type=str, help="Location of DataFile")
	parser.add_argument('savePath', type=str, help="directory path to save html and visualizations")
	args = parser.parse_args()
	datafilename = args.datafile
	baseHtmlPath = args.savePath
	
	if not os.path.exists(baseHtmlPath):
		os.makedirs(baseHtmlPath)
	if not os.path.exists(baseHtmlPath+"/resource"):
		os.makedirs(baseHtmlPath+"/resource")
		
	_dv = dv.DataToVis()
	#print((datafilename))
	arrColumn, arrData, pdDataset = _dv.csvReadToDatasets(datafilename)
	key = _dv.DM_KeyChecker(datafilename)
	d, m, g = _dv.dim_measure_permutations(key)
	###################################################
	#print(d,m,g)
	_dv.visChecker(d, m, g, arrColumn, arrData, pdDataset)
	arrVisType = _dv.printOptimizer()
	
	_dv.visualizationToHTMLsAndPngs(arrVisType, baseHtmlPath+"/resource", arrColumn, arrData, pdDataset)
	file, vis = _dv.getFilename_Visfunc()
	#print(file)
	#print(_dv.VIS.dummyarray)
	
	newfile=[]
	for i in range(len(file)):
		diffflag = False
		for j in range(len(_dv.VIS.dummyarray)):
			if file[i]==_dv.VIS.dummyarray[j] :
				diffflag = True
		if diffflag==False:
			newfile.append(file[i])
	#print(newfile)
	_dv.GenTotalVisHtml(newfile, baseHtmlPath)