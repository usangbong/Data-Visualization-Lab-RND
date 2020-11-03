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
FEATURE_TYPES = []
FEATURE_SUB_TYPES = []
FEATURE_SUB = ""
STIMULUS_CLASSES = []
STIMULUS_NAMES = ["002", "004", "006", "008", "010", "012", "014", "016", "018", "020"]
UIDS = ["usb_02"]
PATHS = []
FEATURES = []
GAZE_DATA_LIST = []
FIXATIONS = []
meanValue = []
RANDOM_DATA_LIST = []
SPATIAL_VARIANCES = []
selectedIdx = 0

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
  
# def ivtFilter(_gazeData, _uid, _feat, _vt):
#   _fixation = []
#   if len(_gazeData) == 1:
#     _fixation.append([0, 0, -999])
#     return _fixation

#   v_threshold = _vt
  
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
#   # print(df)
#   _data = np.array(df)
#   _data_xs = np.unique(_data[:,gfilter.x])
#   _data_ys = np.unique(_data[:,gfilter.y])
#   _user_ids = np.unique(_data[:,gfilter.user_id])

#   for u in _user_ids:
#     for q in range(1,2):
#       sub_data = _data
#       sub2d = np.asarray(sub_data).reshape(len(sub_data),6)
#       centroidsX, centroidsY, time0, time1, fixList, fixations = gfilter.ivt(sub2d, v_threshold)

#   Tdata = {'X':centroidsX,'Y':centroidsY, 'Time':time0}
#   df_IVT = pd.DataFrame(Tdata)

#   n_clusters = len(fixations)
#   clusters = []

#   _fidxrclu = 0
#   for _fpi in range(0, n_clusters):
#     fpts = []
#     fpts.append(df_IVT['X'][_fpi])
#     fpts.append(df_IVT['Y'][_fpi])
#     fpts.append(df_IVT['Time'][_fpi])
#     clusters.append(fpts)
  
#   for _clu in clusters:
#     _x = int(_clu[0])
#     _y = int(_clu[1])
#     _f = float(_feat[_y][_x])
#     _fixation.append([_x, _y, _f])

#   return _fixation

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
  

# def makeRandomPos(_fixLen, _feat):
#   _random = []

#   while _fixLen != len(_random):
#     _rx = randint(0, 1919)
#     _ry = randint(0, 1079)
#     _rf = float(_feat[_ry][_rx])
#     _random.append([_rx, _ry, _rf])
#   return _random
  
# def calcSpatialVariation(_fixationData, _randomData, _meanValue):
#   if _fixationData[0][2] == -999:
#     return -999

#   _spatial_variance = 0
  
#   _deviation_squared_sum = 0
#   for _v in _fixationData:
#     _dev = _v[2]-_meanValue
#     _deviation_squared_sum += _dev*_dev
#   _variation_eye = _deviation_squared_sum/len(_fixationData)

#   _deviation_squared_sum = 0
#   for _v in _randomData:
#     _dev = _v[2]-_meanValue
#     _deviation_squared_sum += _dev*_dev
#   _variation_random = _deviation_squared_sum/len(_randomData)

#   spatial_variation = -1
#   if _variation_random != 0:
#     spatial_variation = _variation_eye/_variation_random

#   _spatial_variance = spatial_variation
#   return _spatial_variance



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
  # global DATASET
  # global FEATURE_TYPES
  # global STIMULUS_CLASSES
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
    # get dataset name, feature types, and stimulus type from submit function on data.js page
    # DATASET = request.form['data-origin']
    # _fl = request.form['feature-types']
    # div_fl = _fl.split(",")
    # for _f in div_fl:
    #   FEATURE_TYPES.append(_f)
    # print("FEATURE_TYPES LEN:%d"%len(FEATURE_TYPES))

    # _snl = request.form['stimulus-classes']
    

    response['status'] = 'success'
    
  except Exception as e:
    response['status'] = 'failed'
    response['reason'] = e
    print(e)

  return json.dumps(response)
