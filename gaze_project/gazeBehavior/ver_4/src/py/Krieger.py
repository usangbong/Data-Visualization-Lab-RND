import sys
import os
import csv
import math

from random import *

class Krieger:
    def __init__(self, _datasetType, _featureList, _stimulusType):
        self.datasetName = _datasetType
        self.featureList = _featureList
        self.stimulusType = _stimulusType

        self.featPath = ""
        self.gazePath = ""
        self.stimulusPath = ""
        self.featureArr = []
        self.meanValue = 0
        self.gazeData = []
        self.randomData = []
        self.gazeFeat = []
        self.randomFeat = []
        self.powerSpectraGazeLoc = []
        self.powerSpectraRndLoc = []
        self.powerSpectraGazeFeat = []
        self.powerSpectraRndFeat = []
    
    def setFeaturePath(self, _fType, _stiName):
        _fString = featureNameToFileStyle(_fType)
        self.featPath = "./static/data/"+self.datasetName+"/feature/"+_fString+"/"+self.stimulusType+"_"+_stiName+".csv"
    
    def setGazePath(self, _uid, _stiName):
        self.gazePath = "./static/data/"+self.datasetName+"/gaze/"+_uid+"/"+self.stimulusType+"_"+_stiName+".csv"

    def setStimulusPath(self, _stiName):
        self.stimulusPath = "./static/data/"+self.datasetName+"/stimulus/"+self.stimulusType+"/"+_stiName+".jpg"

    def featureNameToFileStyle(self, _fName):
        if _fName == "center-bias":
            return "center_bias"
        elif _fName == "contrast-intensity" or _fName == "contrast-color" or _fName == "contrast-orientation":
            return "contrast"
        elif _fName == "HOG":
            return "HOG"
        elif _fName == "horizontal line":
            return "horizontal_line"
        elif _fName == "LOG spectrum":
            return "log"
        elif _fName == "saliency-intensity" or _fName == "saliency-color" or _fName == "saliency-orientation" or _fName == "computed-saliency":
            return "saliency"
        else:
            print("*****----------------------------------*****")
            print("*****")
            print("*****")
            print("***** No feature information")
            print("*****")
            print("*****")
            print("*****----------------------------------*****")
            return "center_bias"

    def loadFeatureFile(self):
        rf = open(self.featPath, 'r', encoding='utf-8')
        rdr = csv.reader(rf)
        
        for _row in rdr:
            self.featureArr.append(_row)
        rf.close()

        sumVal = 0
        for i in range(0, 1080):
            for j in range(0, 1920):
                sumVal += float(self.featureArr[i][j])
        self.meanValue = sumVal/(1920*1080)

    def loadEyeMovementDataFile(self):
        rf = open(self.gazePath, 'r', encoding='utf-8')
        rdr = csv.reader(rf)

        for _row in rdr:
            self.gazeData.append(_row)
        rf.close()

        for _g in self.gazeData:
            # 0: t, 1: x, 2: y
            _gx = int(math.trunc(float(_g[1])))
            _gy = int(math.trunc(float(_g[2])))
            _gf = float(self.featureArr[_gy][_gx])
            self.gazeFeat.append(_gf)

    def makeRandomPos(self):
        while len(self.gazeData) != len(self.randomData):
            _rx = randint(0, 1919)
            _ry = randint(0, 1079)
            self.randomData.append([_rx, _ry])
            _rf = float(self.featureArr[_ry][_rx])
            self.randomFeat.append(_rf)

    def calcSpatialVariation(self, _stimulusName):
        _deviation_squared_sum = 0
        for _v in self.gazeFeat:
            _dev = _v-self.meanValue
            _deviation_squared_sum += _dev*_dev
        _variation_eye = _deviation_squared_sum/len(self.gazeFeat)

        _deviation_squared_sum = 0
        for _v in self.randomFeat:
            _dev = _v-self.meanValue
            _deviation_squared_sum += _dev*_dev
        _variation_random = _deviation_squared_sum/len(self.randomFeat)

        spatial_variation = -1
        if _variation_random != 0:
            spatial_variation = _variation_eye/_variation_random

        return spatial_variation
    
    def analysisStep_1(self):
        print("analysis step 1")

    def selectPowerSpectraData(self):
        degreePixel = 45
        foveaRange = 1
        degreePixel = degreePixel*foveaRange

        for _g in self.gazeData:
            _gx = int(math.trunc(float(_g[1])))
            _gy = int(math.trunc(float(_g[2])))

            if _gx - degreePixel > 0 and _gx + degreePixel < 1920 and _gy - degreePixel > 0 and _gy + degreePixel < 1080:
                self.powerSpectraGazeLoc = [_gx, _gy]
                break
        
        for _r in self.randomData:
            _rx = _r[0]
            _ry = _r[1]

            if _rx - degreePixel > 0 and _rx + degreePixel < 1920 and _ry - degreePixel > 0 and _ry + degreePixel < 1080:
                self.powerSpectraRndLoc = [_rx, _ry]
                break
        
        for i in range(0, 1080):
            if i - self.powerSpectraGazeLoc[1] < degreePixel and i - self.powerSpectraGazeLoc[1] >= 0:
                for j in range(0, 1980):
                    if j - self.powerSpectraGazeLoc[0] < degreePixel and j - self.powerSpectraGazeLoc[0] >= 0:
                        self.powerSpectraGazeFeat.append(float(self.featureArr[i][j])) 

            if i - self.powerSpectraRndLoc[1] < degreePixel and i - self.powerSpectraRndLoc[1] >= 0:
                for j in range(0, 1980):
                    if j - self.powerSpectraRndLoc[0] < degreePixel and i - self.powerSpectraRndLoc[0] >= 0:
                        self.powerSpectraRndFeat.append(float(self.featureArr[i][j]))

    def getFeaturePath(self):
        return self.featPath

    def getGazePath(self):
        return self.gazePath

    def getStimulusPath(self):
        return self.stimulusPath
    
    def getFeatureArr(self):
        return self.featureArr

    def getFeatureMeanValue(self):
        return self.meanValue
    
    def getGazeData(self):
        return self.gazeData
    
    def getRandomData(self):
        return self.randomData

    def getGazeFeature(self):
        return self.gazeFeat

    def getRandomFeature(self):
        return self.randomFeat

    def getPowerSpectraGazeLocaction(self):
        return self.powerSpectraGazeLoc

    def getPowerSpectraRandomLocation(self):
        return self.powerSpectraRndLoc

    def getPowerSpectraGazeFeature(self):
        return self.powerSpectraGazeFeat
    
    def getPowerSpectraRandomFeature(self):
        return self.powerSpectraRndFeat