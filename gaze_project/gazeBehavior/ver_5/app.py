import sys
import os
import csv
import math
import json
from random import *

import numpy as np
import pandas as pd
from flask import *
from flask_cors import CORS

import src.py.glodberg as gfilter

# init dataset name, feature types, and stimulus type
DATASET = "MIT300"
FILTER = "ivt"
PARTICIPANT = "usb_02"
STIMULUS_CLASSES = []
FEATURE_TYPES = []
# FEATURE_SUB_TYPES = []
# FEATURE_SUB = ""
# STIMULUS_CLASSES = []
# STIMULUS_NAMES = ["002", "004", "006", "008", "010", "012", "014", "016", "018", "020"]
# UIDS = ["usb_02"]
# PATHS = []
# FEATURES = []
# GAZE_DATA_LIST = []
# FIXATIONS = []
# meanValue = []
# RANDOM_DATA_LIST = []
# SPATIAL_VARIANCES = []
# selectedIdx = 0

app = Flask(__name__)
if __name__ == '__main__':
  app.jinja_env.auto_reload = True
  app.config['TEMPLATES_AUTO_RELOAD'] = True
  app.run(debug=True)
CORS(app)

# def setFeaturePath(_fType, _stiClass, _stiName):
#   _featPath = ""
#   _fString = featureNameToFileStyle(_fType)
#   if FEATURE_SUB == "":
#     _featPath = "./static/data/"+DATASET+"/feature/"+_fString+"/"+_stiClass+"_"+_stiName+".csv"
#   else:
#     _featPath = "./static/data/"+DATASET+"/feature/"+_fString+"/"+_stiClass+"_"+_stiName+"_"+FEATURE_SUB+".csv"
#   return _featPath

# def setGazePath(_uid, _stiClass, _stiName):
#   _gazePath = ""
#   _gazePath = "./static/data/"+DATASET+"/gaze/"+_uid+"/"+_stiClass+"_"+_stiName+".csv"
#   return _gazePath

# def setStimulusPath(_stiClass, _stiName):
#   _stimulusPath = ""
#   _stimulusPath = "/static/data/"+DATASET+"/stimulus/"+_stiClass+"/"+_stiName+".jpg"
#   return _stimulusPath

# def featureNameToFileStyle(_fName):
#   global FEATURE_SUB
#   global FEATURE_SUB_TYPES
#   if _fName == "center-bias":
#     FEATURE_SUB = ""
#     FEATURE_SUB_TYPES.append(FEATURE_SUB)
#     return "center_bias"
#   elif _fName == "contrast-intensity" or _fName == "contrast-color" or _fName == "contrast-orientation":
#     FEATURE_SUB = _fName.split("-")[1]
#     FEATURE_SUB_TYPES.append(FEATURE_SUB)
#     return "contrast"
#   elif _fName == "HOG":
#     FEATURE_SUB = ""
#     FEATURE_SUB_TYPES.append(FEATURE_SUB)
#     return "HOG"
#   elif _fName == "horizontal line":
#     FEATURE_SUB = ""
#     FEATURE_SUB_TYPES.append(FEATURE_SUB)
#     return "horizontal_line"
#   elif _fName == "LOG spectrum":
#     FEATURE_SUB = ""
#     FEATURE_SUB_TYPES.append(FEATURE_SUB)
#     return "log"
#   elif _fName == "saliency-intensity" or _fName == "saliency-color" or _fName == "saliency-orientation" or _fName == "computed-saliency":
#     FEATURE_SUB = _fName.split("-")[1]
#     if FEATURE_SUB == "saliency":
#       FEATURE_SUB = "sm"
#       FEATURE_SUB_TYPES.append(FEATURE_SUB)
#     return "saliency"
#   else:
#     print("*****----------------------------------*****")
#     print("*****")
#     print("*****")
#     print("***** No feature information")
#     print("*****")
#     print("*****")
#     print("*****----------------------------------*****")
#     FEATURE_SUB = ""
#     KFEATURE_SUB_TYPES.append(FEATURE_SUB)
#     return "center_bias"

def calcFeatureMean(_path):
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
  _meanValue = sumVal/(1920*1080)
  
  return _meanValue

# def loadFeatureFile(_path):
#   global meanValue
  
#   rf = open(_path, 'r', encoding='utf-8')
#   rdr = csv.reader(rf)
#   _featArr = []
#   for _row in rdr:
#     _featArr.append(_row)
#   rf.close()
  
#   sumVal = 0
#   for i in range(0, 1080):
#     for j in range(0, 1920):
#       sumVal += float(_featArr[i][j])
#   meanValue.append(sumVal/(1920*1080))
  
#   return _featArr

# def loadEyeMovementDataFile(_path, _feat):
#   _gazeData = []
#   _gaze = []

#   rf = open(_path, 'r', encoding='utf-8')
#   rdr = csv.reader(rf)
  
#   for _row in rdr:
#     # 0: t, 1: x, 2: y
#     if _row[1] == "x":
#       continue
#     elif _row[1] == "NaN":
#       _gazeData.append([0, 0, 0])
#       break
#     else:
#       if float(_row[1]) >= 1920 or float(_row[2]) >= 1080:
#         continue
#       _gazeData.append(_row)
#   rf.close()
  
#   for _g in _gazeData:
#     _t = int(_g[0])
#     _gx = int(math.trunc(float(_g[1])))
#     _gy = int(math.trunc(float(_g[2])))
#     # print("x: %d"%_gx)
#     # print("y: %d"%_gy)
#     _gf = float(_feat[_gy][_gx])
#     _gx = float(_g[1])
#     _gy = float(_g[2])
#     _gaze.append([_t, _gx, _gy, _gf])
#   return _gaze
  
def ivtFilter(_gazeData, _uid, _feats, _vt):
  _fixation = []
  # print(_gazeData[0])
  if len(_gazeData) == 1:
    _sRow = []
    _sRow.append("x")
    _sRow.append("y")
    for _fType in FEATURE_TYPES:
      _sRow.append(_fType)
    _fixation.append(_sRow)

    _f = []
    _f.append(0)
    _f.append(0)
    for i in range(0, len(FEATURE_TYPES)):
      _f.append(-999)

    _fixation.append(_f)
    return _fixation

  v_threshold = _vt
  
  _tempData = []
  _idCount = 0
  _tStamp = 0
  _tCount = 0.0
  for _p in _gazeData:
    _no = _idCount
    _id = _uid
    _timestamp = _tStamp
    _timecount = _tCount
    _x = float(_p[1])
    _y = float(_p[2])
    _tempData.append([_no, _id, _timestamp, _timecount, _x, _y])
    _idCount += 1
    _tCount += 0.1
    if _idCount%9 == 0:
      _tStamp += 1
      _tCount += 0.0
  df = pd.DataFrame(_tempData, columns = ['no', 'userid', 'timestamp', 'timecount', 'x','y'])
  # print(df)
  _data = np.array(df)
  _data_xs = np.unique(_data[:,gfilter.x])
  _data_ys = np.unique(_data[:,gfilter.y])
  _user_ids = np.unique(_data[:,gfilter.user_id])

  for u in _user_ids:
    for q in range(1,2):
      sub_data = _data
      sub2d = np.asarray(sub_data).reshape(len(sub_data),6)
      centroidsX, centroidsY, time0, time1, fixList, fixations = gfilter.ivt(sub2d, v_threshold)

  Tdata = {'X':centroidsX,'Y':centroidsY, 'Time':time0}
  df_IVT = pd.DataFrame(Tdata)

  n_clusters = len(fixations)
  clusters = []

  _fidxrclu = 0
  for _fpi in range(0, n_clusters):
    fpts = []
    fpts.append(df_IVT['X'][_fpi])
    fpts.append(df_IVT['Y'][_fpi])
    fpts.append(df_IVT['Time'][_fpi])
    clusters.append(fpts)
  
  _firstRowFlag = True
  for _clu in clusters:
    _x = int(_clu[0])
    _y = int(_clu[1])
    _fs = []
    _fs.append(_x)
    _fs.append(_y)
    for _feat in _feats:
      _f = float(_feat[_y][_x])
      _fs.append(_f)
    
    if _firstRowFlag:
      _sRow = []
      _sRow.append("x")
      _sRow.append("y")
      for _fType in FEATURE_TYPES:
        _sRow.append(_fType)
      _fixation.append(_sRow)
      _firstRowFlag = False
    
    _fixation.append(_fs)

  return _fixation

# def idtFilter(_gazeData, _uid, _feat, _distributionThres, _durationThres):
#   _fixation = []
#   if len(_gazeData) == 1:
#     _fixation.append([0, 0, -999])
#     return _fixation
  
#   dur_threshold = _durationThres
#   dis_threshold = _distributionThres

#   _tempData = []
#   _idCount = 0
#   _tStamp = 0
#   _tCount = 0.0
#   for _p in _gazeData:
#     _no = _idCount
#     _id = _uid
#     _timestamp = _tStamp
#     _timecount = _tCount
#     _x = float(_p[1])
#     _y = float(_p[2])
#     _tempData.append([_no, _id, _timestamp, _timecount, _x, _y])
#     _idCount += 1
#     _tCount += 0.1
#     if _idCount%9 == 0:
#       _tStamp += 1
#       _tCount += 0.0
#   df = pd.DataFrame(_tempData, columns = ['no', 'userid', 'timestamp', 'timecount', 'x','y'])
#   _data = np.array(df)
#   _data_xs = np.unique(_data[:,gfilter.x])
#   _data_ys = np.unique(_data[:,gfilter.y])
#   _user_ids = np.unique(_data[:,gfilter.user_id])

#   for u in user_ids:
#     for q in range(1,2):
#       sub_data = _data
#       sub2d = np.asarray(sub_data).reshape(len(sub_data),6) #this is a numpy array
#       centroidsX, centroidsY, time0, tDif, fixList, fixations = gfilter.idt(sub2d, dis_threshold, dur_threshold)
  
#   for _clu in clusters:
#     _x = int(_clu[0])
#     _y = int(_clu[1])
#     _f = float(_feat[_y][_x])
#     _fixation.append([_x, _y, _f])

#   return _fixation
  

def makeRandomPos(_fixLen, _feats):
  _random = []

  _firstRowFlag = True
  while _fixLen != len(_random):
    _rx = randint(0, 1919)
    _ry = randint(0, 1079)
    _rfs = []
    _rfs.append(_rx)
    _rfs.append(_ry)
    for _feat in _feats:
      _rf = float(_feat[_ry][_rx])
      _rfs.append(_rf)
    
    if _firstRowFlag:
      _frr = []
      _frr.append("x")
      _frr.append("y")
      for _fType in FEATURE_TYPES:
        _frr.append(_fType)
      _random.append(_frr)
      _firstRowFlag = False

    _random.append(_rfs)
  
  return _random
  
def calcSpatialVariation(_fixations, _randoms, _fType, _sClass, _sName):
  _meanPath = "./static/data/"+DATASET+"/feature_mean/"+_fType+"/"+_sClass+"_"+_sName+".txt"
  rf = open(_meanPath, 'r', encoding='utf-8')
  rdr = csv.reader(rf)
  _meanValue = 0
  for _m in rdr:
    _meanValue = float(_m[0])
  rf.close()
  # print(_meanValue)

  _fixFeat_sum = 0
  for _ff in _fixations:
    _fixFeat_sum += float(_ff)
  
  _rndFeat_sum = 0
  for _rf in _randoms:
    _rndFeat_sum += float(_rf)

  if len(_fixations) == 1 or _fixFeat_sum == 0 or _rndFeat_sum == 0:
    return -999

  _deviation_squared_sum = 0
  for _ff in _fixations:
    _dev = float(_ff)-_meanValue
    _deviation_squared_sum += _dev*_dev
  _variation_eye = _deviation_squared_sum/len(_fixations)

  _deviation_squared_sum = 0
  for _rf in _randoms:
    _dev = float(_rf)-_meanValue
    _deviation_squared_sum += _dev*_dev
  _variation_random = _deviation_squared_sum/len(_randoms)

  if _variation_random == 0:
    return -999
  else:
    spatial_variation = _variation_eye/_variation_random
    return spatial_variation


# def initGlobal():
#   global DATASET
#   global FEATURE_TYPES
#   global FEATURE_SUB_TYPES
#   global FEATURE_SUB
#   global STIMULUS_CLASSES
#   global STIMULUS_NAMES
#   global UIDS
#   global PATHS
#   global FEATURES
#   global GAZE_DATA_LIST
#   global FIXATIONS
#   global meanValue
#   global RANDOM_DATA_LIST
#   global SPATIAL_VARIANCES

#   DATASET = "MIT300"
#   FEATURE_TYPES = []
#   FEATURE_SUB_TYPES = []
#   FEATURE_SUB = ""
#   STIMULUS_CLASSES = []
#   STIMULUS_NAMES = ["002", "004", "006", "008", "010", "012", "014", "016", "018", "020"]
#   UIDS = ["usb_02"]
#   PATHS = []
#   FEATURES = []
#   GAZE_DATA_LIST = []
#   FIXATIONS = []
#   meanValue = []
#   RANDOM_DATA_LIST = []
#   SPATIAL_VARIANCES = []


# def makeJSON(_path, _data):
#   wf = open(_path, "w", newline='', encoding='utf-8')
#   wf.write(json.dumps(_data))
#   wf.close()

# app = Flask(__name__)
# if __name__ == '__main__':
#   app.jinja_env.auto_reload = True
#   app.config['TEMPLATES_AUTO_RELOAD'] = True
#   app.run(debug=True)
# CORS(app)

# @app.route('/api/analysis/velocity', methods=['POST'])
# def changeVelocity():
#   response = {}
  
#   try:
#     _velocity = float(request.form['velocity'])
#     changedFixation = ivtFilter(GAZE_DATA_LIST[selectedIdx], UIDS[0], FEATURES[selectedIdx], _velocity)
#     FIXATIONS.pop(selectedIdx)
#     FIXATIONS.insert(selectedIdx, changedFixation)
#     makeJSON("./static/output/selected_fixation.json", FIXATIONS[selectedIdx])

#     rndFixations = makeRandomPos(len(FIXATIONS[selectedIdx]), FEATURES[selectedIdx])
#     RANDOM_DATA_LIST.pop(selectedIdx)
#     RANDOM_DATA_LIST.insert(selectedIdx, rndFixations)
#     makeJSON("./static/output/selected_raw_random.json", RANDOM_DATA_LIST[selectedIdx])
    
    
#     response['status'] = 'success'
#   except Exception as e:
#     response['status'] = 'failed'
#     response['reason'] = e
#     print(e)
  
#   return json.dumps(response)

# @app.route('/api/sp_variance/select', methods=['POST'])
# def selectedDataSubmit():
#   global selectedIdx
#   response = {}

#   try:
#     _id = request.form['userID']
#     _fType = request.form['featureType']
#     _sClass = request.form['stimulusClass']
#     _sName = request.form['stimulusName']
#     _val = request.form['spValue']
#     # print(request.form)
    
#     # set selected user id & make JSON file
#     makeJSON("./static/output/selected_userid.json", _id)
#     # make selected stimulus path JSON file
#     selected_sPath = setStimulusPath(_sClass, _sName.split(".")[0])
#     print(selected_sPath)
#     # find selected data index
#     selectedIdx = 0
#     for _fp in PATHS:
#       if _fp[2] == selected_sPath:
#         break
#       selectedIdx += 1
#     makeJSON("./static/output/selected_stimulus_path.json", selected_sPath)
#     # make selected raw gaze data JSON file
#     makeJSON("./static/output/selected_raw_gaze.json", GAZE_DATA_LIST[selectedIdx])
#     # make selected fixation data JSON file
#     makeJSON("./static/output/selected_fixation.json", FIXATIONS[selectedIdx])
#     # make random data JSON file
#     makeJSON("./static/output/selected_raw_random.json", RANDOM_DATA_LIST[selectedIdx])
#     # make bispectra image files

#     response['status'] = 'success'
#   except Exception as e:
#     response['status'] = 'failed'
#     response['reason'] = e
#     print(e)
  
#   return json.dumps(response)

@app.route('/api/gaze_data/submit', methods=['POST'])
def gazeDataSubmit():
  global DATASET
  global FILTER
  global PARTICIPANT
  global FEATURE_TYPES
  global STIMULUS_CLASSES
  # global PATHS
  # global FEATURES
  # global GAZE_DATA_LIST
  # global FIXATIONS
  # global RANDOM_DATA_LIST
  # global SPATIAL_VARIANCES

  # initGlobal()
  
  print(request.form)
  # print(request.form['data-origin'])
  response = {}

  try:
    # get selected dataset, participant, and fixation filter from client
    DATASET = request.form['dataset']
    PARTICIPANT = request.form['participant']
    FILTER = request.form['filter']
    
    # get feature types from server static directory
    FEATURE_TYPES = []
    featureFilePath = "./static/features.csv"
    rf = open(featureFilePath, 'r', encoding='utf-8')
    rdr = csv.reader(rf)
    for _featType in rdr:
      # print(_featType[0])
      FEATURE_TYPES.append(_featType[0])
    rf.close()

    # get stimulus classes from server static directory
    STIMULUS_CLASSES = []
    # stimulusClassFilePath = "./static/data/"+DATASET+"/stimulus_class.csv"
    # rf = open(stimulusClassFilePath, 'r', encoding='utf-8')
    # rdr = csv.reader(rf)
    # for _stiClass in rdr:
    #   STIMULUS_CLASSES.append(_stiClass[0])
    # rf.close()
    stimulusDir = "./static/data"+"/"+DATASET+"/stimulus"
    STIMULUS_CLASSES = os.listdir(stimulusDir)
    
    # check fixation cache
    fixationDir = "./static/data/"+DATASET+"/"+PARTICIPANT+"/fixation/"
    randomDir = "./static/data/"+DATASET+"/"+PARTICIPANT+"/random/"
    spDir = "./static/data/"+DATASET+"/"+PARTICIPANT+"/sp_variance/"

    filter_threshold = []
    if FILTER == "ivt":
      filter_threshold.append(600)
      fixationDir += "ivt_"+str(filter_threshold[0])
      randomDir += "ivt_"+str(filter_threshold[0])
      spDir += "ivt_"+str(filter_threshold[0])
    elif FILTER == "idt":
      filter_threshold.append(100)
      filter_threshold.append(200)
      fixationDir += "idt_"+str(filter_threshold[0])+"_"+str(filter_threshold[1])
      randomDir += "idt_"+str(filter_threshold[0])+"_"+str(filter_threshold[1])
      spDir += "idt_"+str(filter_threshold[0])+"_"+str(filter_threshold[1])
    else:
      # default set: ivt filter
      filter_threshold.append(1000)
      fixationDir += "ivt_"+str(filter_threshold[0])
      randomDir += "ivt_"+str(filter_threshold[0])
      spDir += "ivt_"+str(filter_threshold[0])
    
    # if fixation and random cache files does not exist
    print("generate fixation and random cache files")
    _fixExistFlag = True
    _rndExistFlag = True
    if not(os.path.exists(fixationDir)) or not(os.path.exists(randomDir)):
      if not(os.path.exists(fixationDir)):
        os.makedirs(os.path.join(fixationDir))
        _fixExistFlag = False
      if not(os.path.exists(randomDir)):
        os.makedirs(os.path.join(randomDir))
        _rndExistFlag = False
      
      _rawGazeDirPath = "./static/data/"+DATASET+"/"+PARTICIPANT+"/gaze/"
      _rawGazeFileList = os.listdir(_rawGazeDirPath)
      
      for _fName in _rawGazeFileList:
        _rawGaze = []
        _dataFilePath = _rawGazeDirPath+_fName
        rf = open(_dataFilePath, 'r', encoding='utf-8')
        rdr = csv.reader(rf)
        for _row in rdr:
          if _row[0] == "t":
            continue
          _t = _row[0]
          _x = _row[1]
          _y = _row[2]
          _rawGaze.append([_t, _x, _y])
        rf.close()

        _features = []
        for _fType in FEATURE_TYPES:
          _featFilePath = "./static/data/"+DATASET+"/feature/"+_fType+"/"+_fName
          rf = open(_featFilePath, 'r', encoding='utf-8')
          rdr = csv.reader(rf)
          _feat = []
          for _row in rdr:
            _feat.append(_row)
          _features.append(_feat)
          rf.close()
        _fixation = []
        _random = []
        if FILTER == "ivt":
          _fixation = ivtFilter(_rawGaze, PARTICIPANT, _features, filter_threshold[0])
          _random = makeRandomPos(len(_fixation), _features)
        elif FILTER == "idt":
          print("idt filter")
        else:
          print("default: ivt filter")
          _fixation = ivtFilter(_rawGaze, PARTICIPANT, _features, filter_threshold[0])
          _random = makeRandomPos(len(_fixation), _features)
        
        if not(_fixExistFlag):
          writeFixationPath_csv = fixationDir+"/"+_fName.split(".")[0]+".csv"
          wf = open(writeFixationPath_csv, "w", newline='', encoding='utf-8')
          writer = csv.writer(wf)
          for _r in _fixation:
            writer.writerow(_r)
          wf.close()
          print(writeFixationPath_csv)

        if not(_rndExistFlag):
          writeRandomPath_csv = randomDir+"/"+_fName.split(".")[0]+".csv"
          wf = open(writeRandomPath_csv, "w", newline='', encoding='utf-8')
          writer = csv.writer(wf)
          for _r in _random:
            writer.writerow(_r)
          wf.close()
          print(writeRandomPath_csv)

    # if feature mean cache files does not exist
    print("generate feature mean cache files")
    meanDir = './static/data/'+DATASET+"/feature_mean"
    if not(os.path.exists(meanDir)):
      os.makedirs(os.path.join(meanDir))
      _featureDir = './static/data/'+DATASET+"/feature"
      for _fType in FEATURE_TYPES:
        _featureDirPath = _featureDir+"/"+_fType
        _featureFileList = os.listdir(_featureDirPath)
        for _fName in _featureFileList:
          _path = _featureDirPath+"/"+_fName
          _mean = calcFeatureMean(_path)
          _writeMeanDir = meanDir+"/"+_fType
          if not(os.path.exists(_writeMeanDir)):
            os.makedirs(os.path.join(_writeMeanDir))
          _writeMeanPath_csv = _writeMeanDir+"/"+_fName.split(".")[0]+".txt"
          wf = open(_writeMeanPath_csv, "w", newline='', encoding='utf-8')
          wf.write(str(_mean))
          wf.close()
          print(_writeMeanPath_csv)

    # if spatial variance cache files does not exist
    print("generate spatial variance cache files")
    if not(os.path.exists(spDir)):
      os.makedirs(os.path.join(spDir))

      _sFixations = []
      _sRandoms = []
      _sLogs = []
      
      # load fixation files
      _fixFileList = os.listdir(fixationDir)
      _fixClass = []
      _logClass = []
      _prevClass = ""
      for _fixFileName in _fixFileList:
        _fixFilePath = fixationDir+"/"+_fixFileName
        _stiClass = _fixFileName.split("_")[0]
        _stiName = _fixFileName.split(".")[0].split("_")[1]
        if _stiClass != _prevClass:
          if _prevClass != "":
            _sFixations.append(_fixClass)
            _sLogs.append(_logClass)
          _prevClass = _stiClass
          _fixClass = []
          _logClass = []

        rf = open(_fixFilePath, 'r', encoding='utf-8')
        rdr = csv.reader(rf)
        _fRowFlag = True
        for _row in rdr:
          if _fRowFlag:
            _fRowFlag = False
            continue
          _fixClass.append(_row[2:])
          _logClass.append([_stiClass, _stiName])
        rf.close()
        _prevClass = _stiClass
      _sFixations.append(_fixClass)
      _sLogs.append(_logClass)
      _fixClass = []
      _logClass = []
      print("All fixation data files loaded")

      # load random files
      _rndFileList = os.listdir(randomDir)
      _rndClass = []
      _prevClass = ""
      for _rndFileName in _rndFileList:
        _rndFilePath = randomDir+"/"+_rndFileName
        _stiClass = _rndFileName.split("_")[0]
        if _stiClass != _prevClass:
          if _prevClass != "":
            _sRandoms.append(_rndClass)
          _prevClass = _stiClass
          _rndClass = []
        
        rf = open(_rndFilePath, 'r', encoding='utf-8')
        rdr = csv.reader(rf)
        _fRowFlag = True
        for _row in rdr:
          if _fRowFlag:
            _fRowFlag = False
            continue
          _rndClass.append(_row[2:])
        rf.close()
        _prevClass = _stiClass
      _sRandoms.append(_rndClass)
      _rndClass = []
      print("All random data files loaded")

      print(_sLogs)

      # calculate spatial variance
      spatialVariance = []
      fileNameInClass = []
      for i in range(0, len(STIMULUS_CLASSES)):
        # print("------------------------------------------------------------------------")
        # print(STIMULUS_CLASSES[i])
        logColName = ["stimulusClass", "stimulusName"]
        logDf = pd.DataFrame(_sLogs[i], columns=logColName)
        
        featColName = []
        for _fType in FEATURE_TYPES:
          featColName.append(_fType)
        fixDf = pd.DataFrame(_sFixations[i], columns=featColName)
        rndDf = pd.DataFrame(_sRandoms[i], columns=featColName)
        
        fixCsDF = pd.merge(logDf, fixDf, left_index=True, right_index=True)
        rndCsDF = pd.merge(logDf, rndDf, left_index=True, right_index=True)

        _stiNameSet = logDf.drop_duplicates(["stimulusName"]).iloc[:,1]
        _stiNames_list = _stiNameSet.values.tolist()
        fileNameInClass.append(_stiNames_list)
        
        _spNameVals = []
        for j in range(0, len(_stiNames_list)):
          _name = _stiNames_list[j]
          # print(_name)
          _spVals = []
          for k in range(0, len(FEATURE_TYPES)):
            _feat = FEATURE_TYPES[k]
            # print(_feat)
            _sample_fix_feat = fixCsDF[fixCsDF['stimulusName'].isin([_name])].iloc[:,k+2]
            _sample_rnd_faet = rndCsDF[rndCsDF['stimulusName'].isin([_name])].iloc[:,k+2]
            
            _sample_fix_feat_list = _sample_fix_feat.values.tolist()
            _sample_rnd_feat_list = _sample_rnd_faet.values.tolist()
            
            _spVals.append(calcSpatialVariation(_sample_fix_feat_list, _sample_rnd_feat_list, _feat, STIMULUS_CLASSES[i], _name))
          _spNameVals.append(_spVals)
        spatialVariance.append(_spNameVals)
        # print("------------------------------------------------------------------------")
      
      spClassColNames = ["stimulusClass", "stimulusName"]
      spClassNameData = []
      for i in range(0, len(STIMULUS_CLASSES)):
        _sClass = STIMULUS_CLASSES[i]
        _cInNames = fileNameInClass[i]
        for _n in _cInNames:
          spClassNameData.append([_sClass, _n])
      
      spCNDF = pd.DataFrame(spClassNameData, columns=spClassColNames)
      
      spFeatColNames = []
      for _fType in FEATURE_TYPES:
        spFeatColNames.append(_fType)
      
      spData = []
      for _classData in spatialVariance:
        for _r in _classData:
          spData.append(_r)
      
      spFVDF = pd.DataFrame(spData, columns=spFeatColNames)
      
      spJoinData = pd.merge(spCNDF, spFVDF, left_index=True, right_index=True)
      print(spJoinData)

      spAllPath = spDir+"/"+"sp_all.csv"
      spJoinData.to_csv(spAllPath, mode='w', index=False)
      print("spatial variance all data saved")

      spMeanValsData = []
      spMClass = []
      for _className in STIMULUS_CLASSES:
        _sp = []
        spMClass.append(_className)
        for i in range(0, len(FEATURE_TYPES)):
          _dataSample = spJoinData[spJoinData['stimulusClass'].isin([_className])].iloc[:,i+2]
          _listSample = _dataSample.values.tolist()

          _count = 0
          _sumVals = 0
          for _v in _listSample:
            if _v == -999:
              continue
            _sumVals += _v
            _count += 1
          _spMeanVal = -999
          if _count != 0:
            _spMeanVal = _sumVals/_count
          
          _sp.append(_spMeanVal)
        spMeanValsData.append(_sp)
      
      spMClassColName = ["stimulusClass"]
      spMCDF = pd.DataFrame(spMClass, columns=spMClassColName)
      print(spMCDF)

      spMDF = pd.DataFrame(spMeanValsData, columns=spFeatColNames)
      print(spMDF)

      spMJoinData = pd.merge(spMCDF, spMDF, left_index=True, right_index=True)
      print(spMJoinData)

      spMeanPath = spDir+"/"+"sp_mean.csv"
      spMJoinData.to_csv(spMeanPath, mode='w', index=False)
      print("spatial variance mean data saved")
      
    # if fixation, random, and spatial variance cache file exist
    # Load spatial variance mean cache
    print("Load spatial variance mean cache")
    spMeanCachePath = spDir+"/"+"sp_mean.csv"
    spMeanCache = pd.read_csv(spMeanCachePath)
    print(spMeanCache)





      

    response['status'] = 'success'
    response['data'] = {
      'dataset': DATASET,
      'participant': PARTICIPANT,
      'filter': FILTER
    }
    
  except Exception as e:
    response['status'] = 'failed'
    response['reason'] = e
    print(e)

  return json.dumps(response)
