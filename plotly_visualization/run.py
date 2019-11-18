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
