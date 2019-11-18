# python version 3.5x
import os
import argparse
import dataToVis as dv

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
	arrColumn, arrData, pdDataset = _dv.csvReadToDatasets(datafilename)
	key = _dv.DM_KeyChecker(datafilename)
	d, m = _dv.dim_measure_permutations(key)
	_dv.visChecker(d, m, arrColumn, arrData, pdDataset)
	arrVisType = _dv.printOptimizer()
	
	_dv.visualizationToHTMLsAndPngs(arrVisType, baseHtmlPath+"/resource", arrColumn, arrData, pdDataset)
	file, vis = _dv.getFilename_Visfunc()
	_dv.GenTotalVisHtml(file, baseHtmlPath)
