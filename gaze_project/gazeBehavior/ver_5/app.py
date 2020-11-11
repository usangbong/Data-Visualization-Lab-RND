import sys
import os
import csv
import math
import json
from random import *

import numpy as np
import pandas as pd
from sklearn import preprocessing as sklearn_preprocessing
from flask import *
from flask_cors import CORS

import src.py.glodberg as gfilter

# init dataset name, feature types, and stimulus type
DATASET = "MIT300"
FILTER = "ivt"
PARTICIPANT = "usb_02"
DATAPROCESSING = "min_max"
CORRELATION_METHOD = "pearson"
STIMULUS_CLASSES = []
FEATURE_TYPES = []
REMOVE_CLASSES = []
REMOVE_FEATURES = []


# eye movement event filter threshold
FILTER_THRESHOLD = []
THRESHOLD_VELOCITY = 600
THRESHOLD_DISTRIBUTION = 100
THRESHOLD_DURATION = 200
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

def makeJSON(_path, _data):
  wf = open(_path, "w", newline='', encoding='utf-8')
  wf.write(json.dumps(_data))
  wf.close()

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


def makePath_Filter(_FILTER, _threshold, _path):
  _p = _path

  if _FILTER == "ivt":
    # ivt filter needs velocity threshold
    _p += _FILTER+"_"+str(_threshold[0])
  elif _FILTER == "idt":
    # idt filter needs distribution and duration threshold
    _p += _FILTER+"_"+str(_threshold[0])+"_"+str(_threshold[1])
  else:
    # default set: ivt filter
    _p += _FILTER+"_"+str(_threshold[0])

  return _p

# function for data preprocessing such as min-max normalization and z-score standardization
def dataPreProcessing(_method, _data):
  processedData = []
  _pd = []
  if _method == "min_max":
    print("Data processing: Min-Max Normalization")
    _pd = sklearn_preprocessing.MinMaxScaler().fit_transform(_data)
  elif _method == "z_score":
    print("Data processing: z-score Standardization")
    _pd = sklearn_preprocessing.StandardScaler().fit_transform(_data)
  else:
    print("Data processing: default (Min-Max Normalization)")
    _pd = sklearn_preprocessing.MinMaxScaler().fit_transform(_data)

  return _pd

# preProcessing_list = fixData.values.tolist()
# dataPreProcessing(DATAPROCESSING, preProcessing_list)

# from pages/Data.js
@app.route('/api/corr/process', methods=['POST'])
def corrProcess():
  global DATAPROCESSING
  global CORRELATION_METHOD
  response = {}
  try:
    print(request.form)
    DATAPROCESSING = request.form['processing']
    CORRELATION_METHOD = request.form['correlation']

    # load all fixation data
    allFixationDataPath = "./static/data/"+DATASET+"/"+PARTICIPANT+"/processedFixation/"
    allFixationDataPath = makePath_Filter(FILTER, FILTER_THRESHOLD, allFixationDataPath)
    allFixationDataPath += "/all_fix.csv"
    afDF = pd.read_csv(allFixationDataPath)
    # print(afDF)
    # drop stimulusName, x, and y coordinate columns
    print("drop stimulusName, x, and y coordinate columns")
    afDF = afDF.drop("stimulusName", axis=1)
    afDF = afDF.drop("x", axis=1)
    afDF = afDF.drop("y", axis=1)

    # print(afDF)
    # drop unselected stimulus classes
    print("drop unselected stimulus classes")
    for _dsc in REMOVE_CLASSES:
      _dropIdx = afDF[afDF["stimulusClass"]==str(_dsc)].index
      afDF = afDF.drop(_dropIdx)

    # drop unselected feature types
    print("drop unselected feature types")
    for _dft in REMOVE_FEATURES:
      afDF = afDF.drop(str(_dft), axis=1)
    print(afDF)

    afDF = afDF.drop("stimulusClass", axis=1)
    selectedFeature = []
    for _ft in FEATURE_TYPES:
      for _uft in REMOVE_FEATURES:
        if _ft != _uft:
          selectedFeature.append(_ft)

    # data pre-processing: min-max normalization or z-score standardization
    _pProData_list = afDF.values.tolist()
    _pProData_list = dataPreProcessing(DATAPROCESSING, _pProData_list)
    processed_afDF = pd.DataFrame(_pProData_list, columns=selectedFeature)


    filteredDataPath = "./static/access/filtered_data.csv"
    processed_afDF.to_csv(filteredDataPath, mode='w', index=False)

    filteredDataPathFP = "./static/access/filtered_data_path.json"
    makeJSON(filteredDataPathFP, filteredDataPath.split(".")[1]+".csv")

    afDFCorrMat = processed_afDF[selectedFeature].iloc[:,range(0,len(selectedFeature))].corr(method=CORRELATION_METHOD)
    afDFCorrMat_access = "./static/access/correlation_mat.csv"
    afDFCorrMat.to_csv(afDFCorrMat_access, mode='w', quoting=2)
    print("calculate and save correlation")
    print(afDFCorrMat)

    # generate short column name version
    afDF_list = _pProData_list
    colNameShort = []
    for i in range(0, len(selectedFeature)):
      colNameShort.append("f_"+str(i).zfill(2))
    afDF_short = pd.DataFrame(afDF_list, columns=colNameShort)
    afDFCorrMat_short = afDF_short[colNameShort].iloc[:,range(0,len(colNameShort))].corr(method=CORRELATION_METHOD)
    afDFCorrMat_short_access = "./static/access/correlation_mat_short.csv"
    afDFCorrMat_short.to_csv(afDFCorrMat_short_access, mode='w', quoting=2)
    print("save short column version correlation data")
    print(afDFCorrMat_short)
    
    response['status'] = 'success'
  except Exception as e:
    response['status'] = 'failed'
    response['reason'] = e
    print(e)
  
  return json.dumps(response)



@app.route('/api/data/removefilter', methods=['POST'])
def removefilter():
  global REMOVE_CLASSES
  global REMOVE_FEATURES

  response = {}
  try:
    print(request.form)
    getClasses = request.form['removeClass']
    getTypes = request.form['removeFeature']

    REMOVE_CLASSES = []
    getClassesList = []
    if len(getClasses) != 0:
      getClassesList = getClasses.split(",")
      for _c in getClassesList:
        REMOVE_CLASSES.append(_c)
      # print(getClassesList)
      
    REMOVE_FEATURES = []
    getTypeList = []
    if len(getTypes) != 0:
      getTypeList = getTypes.split(",")
      for _t in getTypeList:
        REMOVE_FEATURES.append(_t)
      # print(getTypeList)


    response['status'] = 'success'
  except Exception as e:
    response['status'] = 'failed'
    response['reason'] = e
    print(e)
  
  return json.dumps(response)


@app.route('/api/gaze_data/submit', methods=['POST'])
def gazeDataSubmit():
  global DATASET
  global FILTER
  global PARTICIPANT
  global FEATURE_TYPES
  global STIMULUS_CLASSE
  global FILTER_THRESHOLD
  
  print(request.form)
  # print(request.form['data-origin'])
  response = {}

  try:
    # get selected dataset, participant, and fixation filter from client
    DATASET = request.form['dataset']
    PARTICIPANT = request.form['participant']  
    FILTER = request.form['filter']

    # set filter threshold
    FILTER_THRESHOLD = []
    if FILTER == "ivt":
      FILTER_THRESHOLD.append(THRESHOLD_VELOCITY)
    elif FILTER == "idt":
      FILTER_THRESHOLD.append(THRESHOLD_DISTRIBUTION)
      FILTER_THRESHOLD.append(THRESHOLD_DURATION)
    else:
      # default set: ivt filter
      FILTER_THRESHOLD.append(THRESHOLD_VELOCITY)
    
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
    stimulusDir = "./static/data"+"/"+DATASET+"/stimulus"
    STIMULUS_CLASSES = os.listdir(stimulusDir)
    # write current stimulus class list
    stimulusClassFilePath = "./static/data/"+DATASET+"/stimulus_class.csv"
    wf = open(stimulusClassFilePath, "w", newline='', encoding='utf-8')
    writer = csv.writer(wf)
    for _r in STIMULUS_CLASSES:
      writer.writerow(_r)
    wf.close()
    
    # check fixation cache
    fixationDir = "./static/data/"+DATASET+"/"+PARTICIPANT+"/fixation/"
    psdFixDir = "./static/data/"+DATASET+"/"+PARTICIPANT+"/processedFixation/"
    randomDir = "./static/data/"+DATASET+"/"+PARTICIPANT+"/random/"
    spDir = "./static/data/"+DATASET+"/"+PARTICIPANT+"/sp_variance/"
    corrDir = "./static/data/"+DATASET+"/"+PARTICIPANT+"/correlation/"


    fixationDir = makePath_Filter(FILTER, FILTER_THRESHOLD, fixationDir)
    psdFixDir = makePath_Filter(FILTER, FILTER_THRESHOLD, psdFixDir)
    randomDir = makePath_Filter(FILTER, FILTER_THRESHOLD, randomDir)
    spDir = makePath_Filter(FILTER, FILTER_THRESHOLD, spDir)
    corrDir = makePath_Filter(FILTER, FILTER_THRESHOLD, corrDir)

    
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
    
    # if processed fixation cache file does not exist
    print("PFIX: generate processed fixation cache files")
    if not(os.path.exists(psdFixDir)):
      os.makedirs(os.path.join(psdFixDir))
      # get stimulusClass_stimulusName file list
      fixFileList = os.listdir(fixationDir)

      # make front and end column names
      # | stimulusClass | stimulusName | featType 1(ex. center_bias) | ... | featureType n |
      frontColNames = ["stimulusClass", "stimulusName"]
      endColNames = []
      fullColNames = []
      fullColNames.extend(frontColNames)
      fullColNames.extend(endColNames)

      # make empty pandas DataFrame to save all fixations of stimulus classes and names
      allFixDF = pd.DataFrame(index=range(0, 0), columns=fullColNames)
      for _ft in FEATURE_TYPES:
        endColNames.append(_ft)

      for _fFileName in fixFileList:
        _path = fixationDir+"/"+_fFileName
        _class = _fFileName.split("_")[0]
        _name = _fFileName.split(".")[0].split("_")[1]

        _fixDf = pd.read_csv(_path)

        # if any fixations in file, exception control works 'continue'
        if len(_fixDf.index) == 0:
          continue

        _gCandNData = []
        for i in range(0, len(_fixDf.index)):
          _gCandNData.append([_class, _name])
        _stiDf = pd.DataFrame(_gCandNData, columns=frontColNames)

        # merge two DataFrame
        _fDataFrame = pd.merge(_stiDf, _fixDf, left_index=True, right_index=True)

        # concat fixation data into dataframe for all fixations
        allFixDF = pd.concat([allFixDF, _fDataFrame], ignore_index=True)

      # save processed fixations cache file
      psdFixationPath_csv = psdFixDir+"/"+"all_fix.csv"
      allFixDF.to_csv(psdFixationPath_csv, mode='w', index=False)
      print("save processed fixation cache file")


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
      print("SP: All fixation data files loaded")

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
      print("SP: All random data files loaded")

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
      print("SP: spatial variance all data saved")

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
      print("SP: spatial variance mean data saved")
      
    # if fixation, random, and spatial variance cache file exist
    # Load spatial variance mean cache
    print("SP: Load spatial variance mean cache")
    spMeanCachePath = spDir+"/"+"sp_mean.csv"
    spMeanCache = pd.read_csv(spMeanCachePath)
    print(spMeanCache)

    spMeanCacheList = spMeanCache.values.tolist()
    spFormHeatmapData = []
    for i in range(0, len(spMeanCacheList)):
      _group = spMeanCacheList[i][0]
      for j in range(0, len(FEATURE_TYPES)):
        _variable = FEATURE_TYPES[j]
        _value = spMeanCacheList[i][j+1]
        spFormHeatmapData.append([_group, _variable, _value])

    spFormHeatmapColumnNames = ["group", "variable", "value"]
    spFHDF = pd.DataFrame(spFormHeatmapData, columns=spFormHeatmapColumnNames)
    print(spFHDF)
    spHeatmapDataPath = spDir+"/"+"sp_heatmap.csv"
    spFHDF.to_csv(spHeatmapDataPath, index=False)
    # save spatial variance mean data file path
    spHeatmapDataFilePath_filePath = "./static/access/sp_heatmap_path.json"
    makeJSON(spHeatmapDataFilePath_filePath, spHeatmapDataPath.split(".")[1]+".csv")
    print("save spatial variance mean data file path")
    
    
    _psdFixationFilePath = psdFixDir+"/"+"all_fix.csv"
    fixData = pd.read_csv(_psdFixationFilePath)
    fixData = fixData.drop("stimulusClass", axis=1)
    fixData = fixData.drop("stimulusName", axis=1)
    fixData = fixData.drop("x", axis=1)
    fixData = fixData.drop("y", axis=1)

    cols = []
    for _fType in FEATURE_TYPES:
      cols.append(_fType)

    # data pre-processing: Min-max normalization | z-score standardization
    processedData_list = fixData.values.tolist()
    processedData_list = dataPreProcessing(DATAPROCESSING, processedData_list)
    porcessedFixData = pd.DataFrame(processedData_list, columns=cols)    
    correlation_mat = porcessedFixData[cols].iloc[:,range(0,11)].corr(method=CORRELATION_METHOD)

    # save correlation matrix data file
    correlation_mat_csv = corrDir+"/"+"corr_matrix_all.csv"
    correlation_mat.to_csv(correlation_mat_csv, mode='w', quoting=2)
    correlation_mat_csv_access = "./static/access/corr_matrix_path.json"
    makeJSON(correlation_mat_csv_access, correlation_mat_csv.split(".")[1]+".csv")
    print("save correlation matrix data file")


    # generate shortcut version dataframe
    # fixData_list = fixData.values.tolist()
    fixData_list = processedData_list
    cols_short = []
    for i in range(0, len(cols)):
      cols_short.append("f_"+str(i).zfill(2))
    fixData_colName = pd.DataFrame(fixData_list, columns=cols_short)
    print(fixData_colName)
    correlation_shortCol = fixData_colName[cols_short].iloc[:,range(0,11)].corr(method=CORRELATION_METHOD)
    correlation_mat_short_csv = corrDir+"/"+"corr_matrix_all_short.csv"
    correlation_shortCol.to_csv(correlation_mat_short_csv, mode='w', quoting=2)
    correlation_mat_short_csv_access = "./static/access/corr_matrix_short_path.json"
    makeJSON(correlation_mat_short_csv_access, correlation_mat_short_csv.split(".")[1]+".csv")
    print("save correlation matrix short column version data file")


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
