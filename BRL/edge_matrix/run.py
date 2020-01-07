# Sangbong Yoo. usangbong@gmail.com
# python version 3.5
import os
import fileLoader as fl
import dataToMat as dtm

if __name__=='__main__':
	fileName = "./static/1.input"
	numberOfMatrialType = 4
	dataLineLength = [115, 30, 20, 20]
	
	_fl = fl.FileLoader()
	_fl.setFileName(fileName)
	_fl.setDataParameters(dataLineLength, numberOfMatrialType)
	data = _fl.getDataFromInputFile()
