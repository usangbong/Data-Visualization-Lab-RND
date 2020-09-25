from flask import *
from flask_cors import CORS
import sys
import os
import csv
import numpy as np
import math
import json

from random import *

#from src.py import Krieger

# init dataset name, feature types, and stimulus type
DATASET = ""
FEATURE_TYPES = []
FEATURE_SUB = ""
STIMULUS_TYPE = ""
STIMULUS_NAMES = ["002", "004"]

#data_krieger = Krieger(DATASET, FEATURE_TYPES, STIMULUS_TYPE)

datasetName = "MIT300"
featureList = "center-bias"
stimulusType = "Action"

featPath = ""
gazePath = ""
stimulusPath = ""
featureArr = []
meanValue = 0
gazeData = []
randomData = []
gazeFeat = []
randomFeat = []
powerSpectraGazeLoc = []
powerSpectraRndLoc = []
powerSpectraGazeFeat = []
powerSpectraRndFeat = []
powerSpectraResGaze = []
powerSpectraResRnd = []
gazeFoveaRegionMean = []
rndFoveaRegionMean = []

spatial_variance = 0

def setFeaturePath(_fType, _stiName):
  global featPath
  _fString = featureNameToFileStyle(_fType)
  if FEATURE_SUB == "":
    featPath = "./static/data/"+datasetName+"/feature/"+_fString+"/"+STIMULUS_TYPE+"_"+_stiName+".csv"
  else:
    featPath = "./static/data/"+datasetName+"/feature/"+_fString+"/"+STIMULUS_TYPE+"_"+_stiName+"_"+FEATURE_SUB+".csv"

def setGazePath(_uid, _stiName):
  global gazePath
  gazePath = "./static/data/"+datasetName+"/gaze/"+_uid+"/"+STIMULUS_TYPE+"_"+_stiName+".csv"

def setStimulusPath(_stiName):
  global stimulusPath
  stimulusPath = "./static/data/"+datasetName+"/stimulus/"+STIMULUS_TYPE+"/"+_stiName+".jpg"
  
  wf = open("./static/output/stimulus_path.json", "w", newline='', encoding='utf-8')
  wf.write(json.dumps(stimulusPath[1:]))
  wf.close()

def featureNameToFileStyle(_fName):
  global FEATURE_SUB
  if _fName == "center-bias":
    FEATURE_SUB = ""
    return "center_bias"
  elif _fName == "contrast-intensity" or _fName == "contrast-color" or _fName == "contrast-orientation":
    FEATURE_SUB = _fName.split("-")[1]
    return "contrast"
  elif _fName == "HOG":
    FEATURE_SUB = ""
    return "HOG"
  elif _fName == "horizontal line":
    FEATURE_SUB = ""
    return "horizontal_line"
  elif _fName == "LOG spectrum":
    FEATURE_SUB = ""
    return "log"
  elif _fName == "saliency-intensity" or _fName == "saliency-color" or _fName == "saliency-orientation" or _fName == "computed-saliency":
    FEATURE_SUB = _fName.split("-")[1]
    if FEATURE_SUB == "saliency":
      FEATURE_SUB = "sm"
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

def loadFeatureFile():
  global meanValue
  rf = open(featPath, 'r', encoding='utf-8')
  rdr = csv.reader(rf)
  
  for _row in rdr:
    featureArr.append(_row)
  rf.close()

  sumVal = 0
  for i in range(0, 1080):
    for j in range(0, 1920):
      sumVal += float(featureArr[i][j])
  meanValue = sumVal/(1920*1080)

def loadEyeMovementDataFile():
  global gazeData
  global gazeFeat
  rf = open(gazePath, 'r', encoding='utf-8')
  rdr = csv.reader(rf)

  for _row in rdr:
    # 0: t, 1: x, 2: y
    if _row[1] == "x":
      continue
    else:
      gazeData.append(_row)
  rf.close()

  wf = open("./static/output/raw_gaze.json", "w", newline='', encoding='utf-8')
  wf.write(json.dumps(gazeData))
  wf.close()

  for _g in gazeData:
    if _g[1] == "x":
      continue
    _gx = int(math.trunc(float(_g[1])))
    _gy = int(math.trunc(float(_g[2])))
    _gf = float(featureArr[_gy][_gx])
    gazeFeat.append(_gf)


def makeRandomPos():
  global randomData
  global randomFeat
  while len(gazeData) != len(randomData):
    _rx = randint(0, 1919)
    _ry = randint(0, 1079)
    randomData.append([_rx, _ry])
    _rf = float(featureArr[_ry][_rx])
    randomFeat.append(_rf)

  wf = open("./static/output/raw_random.json", "w", newline='', encoding='utf-8')
  wf.write(json.dumps(randomData))
  wf.close()

def calcSpatialVariation():
  global spatial_variance
  _deviation_squared_sum = 0
  for _v in gazeFeat:
    _dev = _v-meanValue
    _deviation_squared_sum += _dev*_dev
  _variation_eye = _deviation_squared_sum/len(gazeFeat)

  _deviation_squared_sum = 0
  for _v in randomFeat:
    _dev = _v-meanValue
    _deviation_squared_sum += _dev*_dev
  _variation_random = _deviation_squared_sum/len(randomFeat)

  spatial_variation = -1
  if _variation_random != 0:
    spatial_variation = _variation_eye/_variation_random

  spatial_variance = spatial_variation

def selectPowerSpectraData():
  global powerSpectraGazeLoc
  global powerSpectraRndLoc
  global powerSpectraGazeFeat
  global powerSpectraRndFeat
  global gazeFoveaRegionMean
  global rndFoveaRegionMean
  degreePixel = 40
  foveaRange = 1
  degreePixel = degreePixel*foveaRange

  # append gaze point list of fovea region
  for _g in gazeData:
    if _g[1] == "x":
      continue
    _gx = int(math.trunc(float(_g[1])))
    _gy = int(math.trunc(float(_g[2])))

    if _gx - degreePixel > 0 and _gx + degreePixel < 1920 and _gy - degreePixel > 0 and _gy + degreePixel < 1080:
      powerSpectraGazeLoc.append([_gx, _gy])
  
  # append random point list of fovea region
  for _r in randomData:
    if _g[1] == "x":
      continue
    _rx = _r[0]
    _ry = _r[1]

    if _rx - degreePixel > 0 and _rx + degreePixel < 1920 and _ry - degreePixel > 0 and _ry + degreePixel < 1080:
      powerSpectraRndLoc.append([_rx, _ry])
  
  gazeFoveaRegionMean = []
  for _pgl in powerSpectraGazeLoc:
    _gFoveaRegion = []
    _gfrSum = 0
    for i in range(0, 1080):
      if i - _pgl[1] < degreePixel and i - _pgl[1] >= 0:
        for j in range(0, 1980):
          if j - _pgl[0] < degreePixel and j - _pgl[0] >= 0:
            _gFoveaRegion.append(float(featureArr[i][j]))
            _gfrSum += float(featureArr[i][j])
    powerSpectraGazeFeat.append(_gFoveaRegion)
    gazeFoveaRegionMean.append(_gfrSum/len(_gFoveaRegion))

  rndFoveaRegionMean = []
  for _prl in powerSpectraRndLoc:
    _rFoveaRegion = []
    _rfrSum = 0
    for i in range(0, 1080):
      if i - _prl[1] < degreePixel and i - _prl[1] >= 0:
        for j in range(0, 1980):
          if j - _prl[0] < degreePixel and j - _prl[0] >= 0:
            _rFoveaRegion.append(float(featureArr[i][j]))
            _rfrSum += float(featureArr[i][j])
    powerSpectraRndFeat.append(_rFoveaRegion)
    rndFoveaRegionMean.append(_rfrSum/len(_rFoveaRegion))

  # for i in range(0, 1080):
  #   if i - powerSpectraGazeLoc[1] < degreePixel and i - powerSpectraGazeLoc[1] >= 0:
  #     for j in range(0, 1980):
  #       if j - powerSpectraGazeLoc[0] < degreePixel and j - powerSpectraGazeLoc[0] >= 0:
  #         powerSpectraGazeFeat.append(float(featureArr[i][j])) 

  #   if i - powerSpectraRndLoc[1] < degreePixel and i - powerSpectraRndLoc[1] >= 0:
  #     for j in range(0, 1980):
  #       if j - powerSpectraRndLoc[0] < degreePixel and i - powerSpectraRndLoc[0] >= 0:
  #         powerSpectraRndFeat.append(float(featureArr[i][j]))

def makePowerSpectra():
  global powerSpectraResGaze
  global powerSpectraResRnd
  # print(len(powerSpectraGazeFeat[0]))
  # print(len(powerSpectraRndFeat))

  powerSpectraResGaze = []
  powerSpectraResRnd = []

  _gfrCount = 0
  for _gfr in powerSpectraGazeFeat:
    _gCount = 0
    for _f in _gfr:
      if _gfrCount == 0:
        powerSpectraResGaze.append(_f)
      elif _gfrCount == 10:
        powerSpectraResGaze[_gCount] = (powerSpectraResGaze[_gCount]-gazeFoveaRegionMean[0])*(_f-gazeFoveaRegionMean[10])
      _gCount += 1
    _gfrCount += 1
    if _gfrCount == 11:
      break

  for _pixel in powerSpectraResGaze:
    if _pixel < 0:
      _pixel = 0
    _pixel = math.sqrt(_pixel)
    
    _pixel = _pixel/2

  wf = open("./static/output/power_gaze.json", "w", newline='', encoding='utf-8')
  wf.write(json.dumps(powerSpectraResGaze))
  wf.close()


app = Flask(__name__)
if __name__ == '__main__':  
  app.run(debug=True)
CORS(app)

@app.route('/api/gaze_data/submit', methods=['POST'])
def gazeDataSubmit():
  global DATASET
  global STIMULUS_TYPE
  global FEATURE_TYPES
  print(request.form)
  # print(request.form['data-origin'])

  response = {}

  try:
    # get dataset name, feature types, and stimulus type from submit function on data.js page
    DATASET = request.form['data-origin']
    _fl = request.form['feature-types']
    for _f in _fl:
      FEATURE_TYPES.append(_f)
    STIMULUS_TYPE = request.form['stimulus-type']
    
    setFeaturePath(_fl, "002")
    setGazePath("t_sb_1", "002")
    setStimulusPath("002")

    loadFeatureFile()
    loadEyeMovementDataFile()
    makeRandomPos()
    calcSpatialVariation()

    selectPowerSpectraData()
    makePowerSpectra()

    response['status'] = 'success'
    response['data'] = {
      'powerSpectra': powerSpectraResGaze
    }
  except Exception as e:
    response['status'] = 'failed'
    response['reason'] = e
    print(e)

  return json.dumps(response)
