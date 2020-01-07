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

	matrix = []
	matrial_type_1 = dtm.DataToMat()
	_m = []
	_m = matrial_type_1.makeMatrix(data[0])
	matrix.append(_m)
	
	matrial_type_2 = dtm.DataToMat()
	_m = []
	_m = matrial_type_2.makeMatrix(data[1])
	matrix.append(_m)

	matrial_type_3 = dtm.DataToMat()
	_m = []
	_m = matrial_type_3.makeMatrix(data[2])
	matrix.append(_m)

	matrial_type_4 = dtm.DataToMat()
	_m = []
	_m = matrial_type_4.makeMatrix(data[3])
	matrix.append(_m)
