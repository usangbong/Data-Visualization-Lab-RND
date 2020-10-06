from flask import *
from flask_cors import CORS
import sys
import os
import csv
import numpy as np
import math
import json
import pandas as pd
from random import *

#from src.py import Krieger

# init dataset name, feature types, and stimulus type
DATASET = "MIT300"
FEATURE_TYPES = []
FEATURE_SUB_TYPES = []
FEATURE_SUB = ""
STIMULUS_CLASSES = []
STIMULUS_NAMES = ["002", "004"]
UIDS = ["t_sb_1"]
PATHS = []
FEATURES = []
GAZE_DATA_LIST = []
FIXATIONS = []
meanValue = []
RANDOM_DATA_LIST = []
SPATIAL_VARIANCES = []

#data_krieger = Krieger(DATASET, FEATURE_TYPES, STIMULUS_CLASSES)

# gazeData = []
# randomData = []
# gazeFeat = []
# randomFeat = []
# powerSpectraGazeLoc = []
# powerSpectraRndLoc = []
# powerSpectraGazeFeat = []
# powerSpectraRndFeat = []
# powerSpectraResGaze = []
# powerSpectraResRnd = []
# gazeFoveaRegionMean = []
# rndFoveaRegionMean = []


def setFeaturePath(_fType, _stiClass, _stiName):
  _featPath = ""
  _fString = featureNameToFileStyle(_fType)
  if FEATURE_SUB == "":
    _featPath = "./static/data/"+DATASET+"/feature/"+_fString+"/"+_stiClass+"_"+_stiName+".csv"
  else:
    _featPath = "./static/data/"+DATASET+"/feature/"+_fString+"/"+_stiClass+"_"+_stiName+"_"+FEATURE_SUB+".csv"
  return _featPath

def setGazePath(_uid, _stiClass, _stiName):
  _gazePath = ""
  _gazePath = "./static/data/"+DATASET+"/gaze/"+_uid+"/"+_stiClass+"_"+_stiName+".csv"
  return _gazePath

def setStimulusPath(_stiClass, _stiName):
  _stimulusPath = ""
  _stimulusPath = "/static/data/"+DATASET+"/stimulus/"+_stiClass+"/"+_stiName+".jpg"
  return _stimulusPath

def featureNameToFileStyle(_fName):
  global FEATURE_SUB
  global FEATURE_SUB_TYPES
  if _fName == "center-bias":
    FEATURE_SUB = ""
    FEATURE_SUB_TYPES.append(FEATURE_SUB)
    return "center_bias"
  elif _fName == "contrast-intensity" or _fName == "contrast-color" or _fName == "contrast-orientation":
    FEATURE_SUB = _fName.split("-")[1]
    FEATURE_SUB_TYPES.append(FEATURE_SUB)
    return "contrast"
  elif _fName == "HOG":
    FEATURE_SUB = ""
    FEATURE_SUB_TYPES.append(FEATURE_SUB)
    return "HOG"
  elif _fName == "horizontal line":
    FEATURE_SUB = ""
    FEATURE_SUB_TYPES.append(FEATURE_SUB)
    return "horizontal_line"
  elif _fName == "LOG spectrum":
    FEATURE_SUB = ""
    FEATURE_SUB_TYPES.append(FEATURE_SUB)
    return "log"
  elif _fName == "saliency-intensity" or _fName == "saliency-color" or _fName == "saliency-orientation" or _fName == "computed-saliency":
    FEATURE_SUB = _fName.split("-")[1]
    if FEATURE_SUB == "saliency":
      FEATURE_SUB = "sm"
      FEATURE_SUB_TYPES.append(FEATURE_SUB)
    return "saliency"
  else:
    print("*****----------------------------------*****")
    print("*****")
    print("*****")
    print("***** No feature information")
    print("*****")
    print("*****")
    print("*****----------------------------------*****")
    FEATURE_SUB = ""
    KFEATURE_SUB_TYPES.append(FEATURE_SUB)
    return "center_bias"

def loadFeatureFile(_path):
  global meanValue
  
  rf = open(_path, 'r', encoding='utf-8')
  rdr = csv.reader(rf)
  _featArr = []
  for _row in rdr:
    _featArr.append(_row)
  rf.close()
  
  sumVal = 0
  for i in range(0, 1080):
    for j in range(0, 1920):
      sumVal += float(_featArr[i][j])
  meanValue.append(sumVal/(1920*1080))
  
  return _featArr

def loadEyeMovementDataFile(_path, _feat):
  _gazeData = []
  _gaze = []

  rf = open(_path, 'r', encoding='utf-8')
  rdr = csv.reader(rf)
  
  for _row in rdr:
    # 0: t, 1: x, 2: y
    if _row[1] == "x":
      continue
    else:
      if float(_row[1]) >= 1920 or float(_row[2]) >= 1080:
        continue
      _gazeData.append(_row)
  rf.close()
  
  for _g in _gazeData:
    _gx = int(math.trunc(float(_g[1])))
    _gy = int(math.trunc(float(_g[2])))
    # print("x: %d"%_gx)
    # print("y: %d"%_gy)
    _gf = float(_feat[_gy][_gx])
    _gx = float(_g[1])
    _gy = float(_g[2])
    _gaze.append([_gx, _gy, _gf])
  return _gaze
  
def fixationFilter(_gazeData, _feat):
  _fixation = []

  prev_t = -1
  fixPts = []
  pts = []
  for _p in _gazeData:
    cur_t = int(_p[0])
    if prev_t == -1:
      prev_t = cur_t
    if prev_t != cur_t:
      fixPts.append(pts)
      pts = []

    pts.append([float(_p[1]), float(_p[2])])
    prev_t = cur_t
  fixPts.append(pts)
  pts = []

  for _fix in fixPts:
    sum_x = 0
    sum_y = 0
    for _p in _fix:
      sum_x += _p[0]
      sum_y += _p[1]
    sum_x = int(sum_x/len(_fix))
    sum_y = int(sum_y/len(_fix))
    fx_feat = _feat[sum_y][sum_x]
    _fixation.append([sum_x, sum_y, fx_feat])
  return _fixation

def makeRandomPos(_fixLen, _feat):
  _random = []

  while _fixLen != len(_random):
    _rx = randint(0, 1919)
    _ry = randint(0, 1079)
    _rf = float(_feat[_ry][_rx])
    _random.append([_rx, _ry, _rf])
  return _random
  
def calcSpatialVariation(_fixationData, _randomData, _meanValue):
  _spatial_variance = 0

  _deviation_squared_sum = 0
  for _v in _fixationData:
    _dev = _v[2]-_meanValue
    _deviation_squared_sum += _dev*_dev
  _variation_eye = _deviation_squared_sum/len(_fixationData)

  _deviation_squared_sum = 0
  for _v in _randomData:
    _dev = _v[2]-_meanValue
    _deviation_squared_sum += _dev*_dev
  _variation_random = _deviation_squared_sum/len(_randomData)

  spatial_variation = -1
  if _variation_random != 0:
    spatial_variation = _variation_eye/_variation_random

  _spatial_variance = spatial_variation
  return _spatial_variance

# def selectPowerSpectraData():
#   global powerSpectraGazeLoc
#   global powerSpectraRndLoc
#   global powerSpectraGazeFeat
#   global powerSpectraRndFeat
#   global gazeFoveaRegionMean
#   global rndFoveaRegionMean
#   degreePixel = 40
#   foveaRange = 1
#   degreePixel = degreePixel*foveaRange

#   # append gaze point list of fovea region
#   for _g in gazeData:
#     if _g[1] == "x":
#       continue
#     _gx = int(math.trunc(float(_g[1])))
#     _gy = int(math.trunc(float(_g[2])))

#     if _gx - degreePixel > 0 and _gx + degreePixel < 1920 and _gy - degreePixel > 0 and _gy + degreePixel < 1080:
#       powerSpectraGazeLoc.append([_gx, _gy])
  
#   # append random point list of fovea region
#   for _r in randomData:
#     if _g[1] == "x":
#       continue
#     _rx = _r[0]
#     _ry = _r[1]

#     if _rx - degreePixel > 0 and _rx + degreePixel < 1920 and _ry - degreePixel > 0 and _ry + degreePixel < 1080:
#       powerSpectraRndLoc.append([_rx, _ry])
  
#   gazeFoveaRegionMean = []
#   for _pgl in powerSpectraGazeLoc:
#     _gFoveaRegion = []
#     _gfrSum = 0
#     for i in range(0, 1080):
#       if i - _pgl[1] < degreePixel and i - _pgl[1] >= 0:
#         for j in range(0, 1980):
#           if j - _pgl[0] < degreePixel and j - _pgl[0] >= 0:
#             _gFoveaRegion.append(float(featureArr[i][j]))
#             _gfrSum += float(featureArr[i][j])
#     powerSpectraGazeFeat.append(_gFoveaRegion)
#     gazeFoveaRegionMean.append(_gfrSum/len(_gFoveaRegion))

#   rndFoveaRegionMean = []
#   for _prl in powerSpectraRndLoc:
#     _rFoveaRegion = []
#     _rfrSum = 0
#     for i in range(0, 1080):
#       if i - _prl[1] < degreePixel and i - _prl[1] >= 0:
#         for j in range(0, 1980):
#           if j - _prl[0] < degreePixel and j - _prl[0] >= 0:
#             _rFoveaRegion.append(float(featureArr[i][j]))
#             _rfrSum += float(featureArr[i][j])
#     powerSpectraRndFeat.append(_rFoveaRegion)
#     rndFoveaRegionMean.append(_rfrSum/len(_rFoveaRegion))

#   # for i in range(0, 1080):
#   #   if i - powerSpectraGazeLoc[1] < degreePixel and i - powerSpectraGazeLoc[1] >= 0:
#   #     for j in range(0, 1980):
#   #       if j - powerSpectraGazeLoc[0] < degreePixel and j - powerSpectraGazeLoc[0] >= 0:
#   #         powerSpectraGazeFeat.append(float(featureArr[i][j])) 

#   #   if i - powerSpectraRndLoc[1] < degreePixel and i - powerSpectraRndLoc[1] >= 0:
#   #     for j in range(0, 1980):
#   #       if j - powerSpectraRndLoc[0] < degreePixel and i - powerSpectraRndLoc[0] >= 0:
#   #         powerSpectraRndFeat.append(float(featureArr[i][j]))

# def makePowerSpectra():
#   global powerSpectraResGaze
#   global powerSpectraResRnd
#   # print(len(powerSpectraGazeFeat[0]))
#   # print(len(powerSpectraRndFeat))

#   powerSpectraResGaze = []
#   powerSpectraResRnd = []

#   _gfrCount = 0
#   for _gfr in powerSpectraGazeFeat:
#     _gCount = 0
#     for _f in _gfr:
#       if _gfrCount == 0:
#         powerSpectraResGaze.append(_f)
#       elif _gfrCount == 10:
#         powerSpectraResGaze[_gCount] = (powerSpectraResGaze[_gCount]-gazeFoveaRegionMean[0])*(_f-gazeFoveaRegionMean[10])
#       _gCount += 1
#     _gfrCount += 1
#     if _gfrCount == 11:
#       break

#   for _pixel in powerSpectraResGaze:
#     if _pixel < 0:
#       _pixel = 0
#     _pixel = math.sqrt(_pixel)
    
#     _pixel = _pixel/2

#   wf = open("./static/output/power_gaze.json", "w", newline='', encoding='utf-8')
#   wf.write(json.dumps(powerSpectraResGaze))
#   wf.close()

app = Flask(__name__)
if __name__ == '__main__':  
  app.run(debug=True)
CORS(app)

@app.route('/api/gaze_data/submit', methods=['POST'])
def gazeDataSubmit():
  global DATASET
  global FEATURE_TYPES
  global STIMULUS_CLASSES
  global PATHS
  global FEATURES
  global GAZE_DATA_LIST
  global FIXATIONS
  global RANDOM_DATA_LIST
  global SPATIAL_VARIANCES

  
  # print(request.form)
  # print(request.form['data-origin'])
  response = {}

  try:
    # get dataset name, feature types, and stimulus type from submit function on data.js page
    DATASET = request.form['data-origin']
    _fl = request.form['feature-types']
    div_fl = _fl.split(",")
    for _f in div_fl:
      FEATURE_TYPES.append(_f)
    print("FEATURE_TYPES LEN:%d"%len(FEATURE_TYPES))

    _snl = request.form['stimulus-classes']
    div_snl = _snl.split(",")
    for _sn in div_snl:
      STIMULUS_CLASSES.append(_sn)
    print("STIMULUS_CLASSES LEN:%d"%len(STIMULUS_CLASSES))
    
    for _f in FEATURE_TYPES:
      for _sc in STIMULUS_CLASSES:
        for _sn in STIMULUS_NAMES:
          PATHS.append([setFeaturePath(_f, _sc, _sn), setGazePath(UIDS[0], _sc, _sn), setStimulusPath(_sc, _sn)])
    print("PATHS LEN:%d"%len(PATHS))
    print("FEATURE_SUB_TYPES LEN:%d"%len(FEATURE_SUB_TYPES))

    _sti_paths = []
    for _sc in STIMULUS_CLASSES:
      for _sn in STIMULUS_NAMES:
        _sti_paths.append(setStimulusPath(_sc, _sn))
    wf = open("./static/output/stimulus_path.json", "w", newline='', encoding='utf-8')
    wf.write(json.dumps(_sti_paths))
    wf.close()
    
    for _p in PATHS:
      _f = loadFeatureFile(_p[0])
      FEATURES.append(_f)
      # print(_p[0])
      # print(_p[1])
      GAZE_DATA_LIST.append(loadEyeMovementDataFile(_p[1], _f))
    wf = open("./static/output/raw_gaze.json", "w", newline='', encoding='utf-8')
    wf.write(json.dumps(GAZE_DATA_LIST))
    wf.close()
    print("GAZE_DATA_LIST LEN:%d"%len(GAZE_DATA_LIST))

    _gIdx = 0
    for _g in GAZE_DATA_LIST:
      FIXATIONS.append(fixationFilter(_g, FEATURES[_gIdx]))
      _gIdx += 1
    print("FIXATIONS LEN:%d"%len(FIXATIONS))
    wf = open("./static/output/fixation.json", "w", newline='', encoding='utf-8')
    wf.write(json.dumps(FIXATIONS))
    wf.close()

    _fxIdx = 0
    for _fx in FIXATIONS:
      RANDOM_DATA_LIST.append(makeRandomPos(len(_fx), FEATURES[_fxIdx]))
      _fxIdx += 1
    print("RANDOM_DATA_LIST LEN:%d"%len(RANDOM_DATA_LIST))
    wf = open("./static/output/raw_random.json", "w", newline='', encoding='utf-8')
    wf.write(json.dumps(RANDOM_DATA_LIST))
    wf.close()

    for i in range(0, len(GAZE_DATA_LIST)):
      SPATIAL_VARIANCES.append(calcSpatialVariation(GAZE_DATA_LIST[i], RANDOM_DATA_LIST[i], meanValue[i]))
    print("SPATIAL_VARIANCES LEN:%d"%len(RANDOM_DATA_LIST))

    analysis_result = []
    for i in range(len(SPATIAL_VARIANCES)):
      _id = UIDS[0]
      _feat = PATHS[i][0].split("/")[5]
      if FEATURE_SUB_TYPES[i] != "":
        _feat = _feat + "-" + FEATURE_SUB_TYPES[i]
      _class = PATHS[i][1].split("/")[6].split("_")[0]
      _name = PATHS[i][1].split("/")[6].split("_")[1].split(".")[0]+".jpg"
      _sp = SPATIAL_VARIANCES[i]
      analysis_result.append([_id, _feat, _class, _name, _sp])
    print("analysis_result LEN:%d"%len(analysis_result))
    wf = open("./static/output/spatial_variance.json", "w", newline='', encoding='utf-8')
    wf.write(json.dumps(analysis_result))
    wf.close()
    
    # setFeaturePath("center-bias", "002")
    # setGazePath("t_sb_1", "002")
    # setStimulusPath("002")

    # loadFeatureFile()
    # loadEyeMovementDataFile()
    # makeRandomPos()

    # calcSpatialVariation()
    # analysis_result = []
    # # analysis_result.append(_fl)
    # analysis_result.append("center-bias")
    # #analysis_result.append(STIMULUS_TYPE[0])
    # analysis_result.append("Action")
    # analysis_result.append("002")
    # analysis_result.append(str(spatial_variance))
    # wf = open("./static/output/spatial_variance.json", "w", newline='', encoding='utf-8')
    # wf.write(json.dumps(analysis_result))
    # wf.close()

    # # selectPowerSpectraData()
    # # makePowerSpectra()

    response['status'] = 'success'
    # response['data'] = {
    #   'powerSpectra': powerSpectraResGaze
    # }
  except Exception as e:
    response['status'] = 'failed'
    response['reason'] = e
    print(e)

  return json.dumps(response)
