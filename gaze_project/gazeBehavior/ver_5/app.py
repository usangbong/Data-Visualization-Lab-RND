import sys
import os
import shutil
import csv
import math
import json
from random import *

import numpy as np
import pandas as pd
import cv2
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import PowerTransformer
from sklearn.decomposition import PCA
from sklearn.decomposition import FastICA
from sklearn.manifold import MDS
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from skimage.metrics import structural_similarity as SSIM
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
STI_CLASS_DEFINE = []
FEATURE_TYPES = []
FEATURE_DEFINE = []
SELECTED_FEATURE_DEFINE = []
REMOVE_CLASSES = []
REMOVE_FEATURES = []
SCATTER_FEATURES = []
PATCH_SIZE = 50
PATCH_DICTIONARY = []
PATCH_INDEX_PATH = []
COLORS = ["#a6cee3", "#fb9a99", "#fdbf6f", "#cab2d6", "#b15928", "#b2df8a", "#ffff99", "#1f78b4", "#e31a1c", "#ff7f00", "#33a02c", "#6a3d9a"]


# eye movement event filter threshold
FILTER_NAME = ""
FILTER_THRESHOLD = []
THRESHOLD_VELOCITY = 600
THRESHOLD_DISTRIBUTION = 100
THRESHOLD_DURATION = 200

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
    _sRow.append("duration")
    _sRow.append("length")
    for _fType in FEATURE_TYPES:
      _sRow.append(_fType)
    _fixation.append(_sRow)

    _f = []
    _f.append(0)
    _f.append(0)
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
  prevCoordi = [-999, -999]
  for _clu in clusters:
    _x = int(_clu[0])
    _y = int(_clu[1])
    _t = int(_clu[2])
    _s = 0
    if prevCoordi[0] != -999 and prevCoordi[1] != -999:
      _s = math.dist([_x, _y], prevCoordi)
    
    _fs = []
    _fs.append(_x)
    _fs.append(_y)
    _fs.append(_t)
    _fs.append(_s)
    for _feat in _feats:
      _f = float(_feat[_y][_x])
      _fs.append(_f)
    
    if _firstRowFlag:
      _sRow = []
      _sRow.append("x")
      _sRow.append("y")
      _sRow.append("duration")
      _sRow.append("length")
      for _fType in FEATURE_TYPES:
        _sRow.append(_fType)
      _fixation.append(_sRow)
      _firstRowFlag = False
    
    prevCoordi = [_x, _y]
    _fixation.append(_fs)

  return _fixation

def idtFilter(_gazeData, _uid, _feats, _distributionThres, _durationThres):
  _fixation = []
  if len(_gazeData) == 1:
    _sRow = []
    _sRow.append("x")
    _sRow.append("y")
    for i in range(0, len(FEATURE_TYPES)):
      _sRow.append(FEATURE_DEFINE[i][2])
    _fixation.append(_sRow)

    _f = []
    _f.append(0)
    _f.append(0)
    for i in range(0, len(FEATURE_TYPES)):
      _f.append(-999)
    _fixation.append(_f)
    return _fixation
  
  dis_threshold = _distributionThres
  dur_threshold = _durationThres
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
  _data = np.array(df)
  _data_xs = np.unique(_data[:,gfilter.x])
  _data_ys = np.unique(_data[:,gfilter.y])
  _user_ids = np.unique(_data[:,gfilter.user_id])

  for u in _user_ids:
    for q in range(1,2):
      sub_data = _data
      sub2d = np.asarray(sub_data).reshape(len(sub_data),6) #this is a numpy array
      centroidsX, centroidsY, time0, tDif, fixList, fixations = gfilter.idt(sub2d, dis_threshold, dur_threshold)

  Tdata = {'X':centroidsX,'Y':centroidsY, 'Time':time0}
  df_IDT = pd.DataFrame(Tdata)

  n_clusters = len(fixations)
  clusters = []
  _fidxrclu = 0
  for _fpi in range(0, n_clusters):
    fpts = []
    fpts.append(df_IDT['X'][_fpi])
    fpts.append(df_IDT['Y'][_fpi])
    fpts.append(df_IDT['Time'][_fpi])
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
      for i in range(0, len(FEATURE_TYPES)):
        _sRow.append(FEATURE_DEFINE[i][2])
      _fixation.append(_sRow)
      _firstRowFlag = False
    
    _fixation.append(_fs)

  return _fixation

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
      for i in range(0, len(FEATURE_TYPES)):
        _frr.append(FEATURE_DEFINE[i][2])
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
  global FILTER_NAME
  _p = _path
  if _FILTER == "ivt":
    # ivt filter needs velocity threshold
    FILTER_NAME = _FILTER+"_"+str(_threshold[0])
    _p += _FILTER+"_"+str(_threshold[0])
  elif _FILTER == "idt":
    # idt filter needs distribution and duration threshold
    FILTER_NAME = _FILTER+"_"+str(_threshold[0])+"_"+str(_threshold[1])
    _p += _FILTER+"_"+str(_threshold[0])+"_"+str(_threshold[1])
  else:
    # default set: ivt filter
    FILTER_NAME = _FILTER+"_"+str(_threshold[0])
    _p += _FILTER+"_"+str(_threshold[0])
  return _p

# function for data preprocessing such as min-max normalization and z-score standardization
def dataPreProcessing(_method, _data):
  _pd = []
  if _method == "raw_data":
    print("Data processing: Raw data")
    _pd = _data
  elif _method == "min_max":
    print("Data processing: Min-Max Normalization")
    _pd = MinMaxScaler().fit_transform(_data)
  elif _method == "z_score":
    print("Data processing: z-score Standardization")
    _pd = StandardScaler().fit_transform(_data)
  else:
    print("Data processing: default (Min-Max Normalization)")
    _pd = MinMaxScaler().fit_transform(_data)
  return _pd

#
#
#
# remove this function after debugging
def generatePatch(_id, _fix, _patchSizse, _stiClass, _stiName, _idx):
  global PATCH_INDEX_PATH
  # print("generatePatch")
  _stiPath = "./static/data/"+DATASET+"/stimulus/"+_stiClass+"/"+_stiName+".jpg"
  # print(_stiPath)
  image = cv2.imread(_stiPath, cv2.IMREAD_COLOR)
  iWidth, iHeight = image.shape[:2]
  # print(image.size)
  _lenPatch = [_patchSizse, _patchSizse]
  _x = _fix[0]
  _y = _fix[1]
  _point = [_x-(_lenPatch[0]/2), _y-(_lenPatch[1]/2)]
  # top bottom left right
  _padding = [0, 0, 0, 0]
  if _point[0] < 0:
    _padding[2] = abs(_point[0])
    _point[0] = 0
    _lenPatch[0] = _lenPatch[0]-_padding[2]
  if _point[0]+_lenPatch[0] > iWidth:
    _padding[3] = (_point[0]+_lenPatch[0]) - iWidth
    _lenPatch[0] = _lenPatch[0] - _padding[3]
  if _point[1] <0:
    _padding[0] = abs(_point[1])
    _point[1] = 0
    _lenPatch[1] = _lenPatch[1]-_padding[0]
  if _point[1]+_lenPatch[1] > iHeight:
    _padding[4] = (_point[1]+_lenPatch[1]) - iHeight
    _lenPatch[1] = _lenPatch[1]-_padding[1]

  _left = int(_point[0])
  _top = int(_point[1])
  _right = int(_point[0]+_lenPatch[0])
  _bottom = int(_point[1]+_lenPatch[1])
  cropImg = image[_top:_bottom, _left:_right]
  color = [255, 255, 255]
  cropImg = cv2.copyMakeBorder(cropImg, int(_padding[0]), int(_padding[1]), int(_padding[2]), int(_padding[3]), cv2.BORDER_CONSTANT, value=color)

  _outPath = "./static/access/"+DATASET
  if not(os.path.exists(_outPath)):
    os.makedirs(os.path.join(_outPath))
  _outPath = _outPath+"/"+_stiClass
  if not(os.path.exists(_outPath)):
    os.makedirs(os.path.join(_outPath))
  _outPath = _outPath+"/"+_stiName
  if not(os.path.exists(_outPath)):
    os.makedirs(os.path.join(_outPath))
  _outPath = _outPath+"/"+str(_idx).zfill(3)+".png"
  cv2.imwrite(_outPath, cropImg)
  PATCH_INDEX_PATH.append([_id, _outPath.split(".")[1]+".png"])
# remove this function after debugging
#
#
#

def appendPatchImageIndexPath(_id, _fix, _patchSizse, _stiClass, _stiName, _idx):
  global PATCH_INDEX_PATH
  _outPath = "./static/data/"+DATASET+"/"+PARTICIPANT+"/patch/"
  _outPath = makePath_Filter(FILTER, FILTER_THRESHOLD, _outPath)
  _outPath = _outPath+"/images/"+_stiClass+"/"+_stiName+"/"+str(_idx).zfill(3)+".png"
  PATCH_INDEX_PATH.append([_id, _outPath.split(".")[1]+".png"])

def generatePatchCache(_id, _fix, _patchSizse, _stiClass, _stiName, _idx, _initFlag):
  print("patch id: %d"%_id)
  global PATCH_DICTIONARY
  global PATCH_INDEX_PATH
  color = [255, 255, 255]
  _appendColumns = ['id', 'stimulusClass','stimulusName', 'fixationIndex', 'type', 'path']
  
  _stiPath = "./static/data/"+DATASET+"/stimulus/"+_stiClass+"/"+_stiName+".jpg"
  if not(os.path.isfile(_stiPath)):
    _stiPath = "."+_stiPath.split(".")[1]+".png"
  
  image = cv2.imread(_stiPath, cv2.IMREAD_COLOR)
  iWidth, iHeight = image.shape[:2]
  _lenPatch = [_patchSizse, _patchSizse]
  _x = _fix[0]
  _y = _fix[1]
  _point = [_x-(_lenPatch[0]/2), _y-(_lenPatch[1]/2)]
  # top bottom left right
  _padding = [0, 0, 0, 0]
  if _point[0] < 0:
    _padding[2] = abs(_point[0])
    _point[0] = 0
    _lenPatch[0] = _lenPatch[0]-_padding[2]
  if _point[0]+_lenPatch[0] > iWidth:
    _padding[3] = (_point[0]+_lenPatch[0]) - iWidth
    _lenPatch[0] = _lenPatch[0] - _padding[3]
  if _point[1] <0:
    _padding[0] = abs(_point[1])
    _point[1] = 0
    _lenPatch[1] = _lenPatch[1]-_padding[0]
  if _point[1]+_lenPatch[1] > iHeight:
    _padding[4] = (_point[1]+_lenPatch[1]) - iHeight
    _lenPatch[1] = _lenPatch[1]-_padding[1]
  _left = int(_point[0])
  _top = int(_point[1])
  _right = int(_point[0]+_lenPatch[0])
  _bottom = int(_point[1]+_lenPatch[1])
  cropImg = image[_top:_bottom, _left:_right]
  cropImg = cv2.copyMakeBorder(cropImg, int(_padding[0]), int(_padding[1]), int(_padding[2]), int(_padding[3]), cv2.BORDER_CONSTANT, value=color)

  _outStandardDir = "./static/data/"+DATASET+"/"+PARTICIPANT+"/patch/"
  _outPath = ""
  if not(os.path.exists(_outStandardDir)):
    os.makedirs(os.path.join(_outStandardDir))
  _outStandardDir = makePath_Filter(FILTER, FILTER_THRESHOLD, _outStandardDir)
  if not(os.path.exists(_outStandardDir)):
    os.makedirs(os.path.join(_outStandardDir))
  _outPath = _outStandardDir+"/images"
  if not(os.path.exists(_outPath)):
    os.makedirs(os.path.join(_outPath))
  if not(os.path.exists(_outPath)):
    os.makedirs(os.path.join(_outPath))
  _outPath = _outPath+"/"+_stiClass
  if not(os.path.exists(_outPath)):
    os.makedirs(os.path.join(_outPath))
  _outPath = _outPath+"/"+_stiName
  if not(os.path.exists(_outPath)):
    os.makedirs(os.path.join(_outPath))
  _outPath = _outPath+"/"+str(_idx).zfill(3)+".png"
  cv2.imwrite(_outPath, cropImg)
  PATCH_INDEX_PATH.append([_id, _outPath.split(".")[1]+".png"])
  if _initFlag:
    _appendData = []
    _appendData.append([_id, _stiClass, _stiName, _idx, "image", _outPath.split(".")[1]+".png"])
    _appendDF = pd.DataFrame(_appendData, columns=_appendColumns)
    PATCH_DICTIONARY = PATCH_DICTIONARY.append(_appendDF, ignore_index=True)
  _featOutPath = _outStandardDir+"/features"
  if not(os.path.exists(_featOutPath)):
    os.makedirs(os.path.join(_featOutPath))
  _matrixOutPath = _outStandardDir+"/matrix"
  if not(os.path.exists(_matrixOutPath)):
    os.makedirs(os.path.join(_matrixOutPath))

  _featOutPathSaved = _featOutPath
  _matrixOutPathSave = _matrixOutPath
  # genearte feature images
  for i in range(len(FEATURE_DEFINE)):
    _featureType = FEATURE_DEFINE[i][1]
    _featPath = "./static/data/"+DATASET+"/feature/"+_featureType+"/"+_stiClass+"_"+_stiName+".csv"
    featDF = pd.read_csv(_featPath, header=None)
    featNP = featDF.to_numpy()
    # featTrain = MinMaxScaler().fit_transform(featNP)
    minmaxNP = (featNP-featNP.min(axis=0)) / (featNP.max(axis=0) - featNP.min(axis=0))
    featTrain = np.abs(featTrain*255-255)
    _savePath = "./static/access/feature.png"
    cv2.imwrite(_savePath, featTrain)
    featureImage = cv2.imread(_savePath, cv2.IMREAD_COLOR)
    _left = int(_point[0])
    _top = int(_point[1])
    _right = int(_point[0]+_lenPatch[0])
    _bottom = int(_point[1]+_lenPatch[1])
    featureCropImg = featureImage[_top:_bottom, _left:_right]
    featureCropImg = cv2.copyMakeBorder(featureCropImg, int(_padding[0]), int(_padding[1]), int(_padding[2]), int(_padding[3]), cv2.BORDER_CONSTANT, value=color)
    featureCropImgGray = cv2.cvtColor(featureCropImg, cv2.COLOR_BGR2GRAY)
    _featOutPath = _featOutPathSaved+"/"+str(_id)
    if not(os.path.exists(_featOutPath)):
      os.makedirs(os.path.join(_featOutPath))
    _fTypeShort = FEATURE_DEFINE[i][2]
    _featOutPath = _featOutPath+"/"+_fTypeShort+".png"
    cv2.imwrite(_featOutPath, featureCropImgGray)
    if _initFlag:
      _appendData = []
      _appendData.append([_id, _stiClass, _stiName, _idx, "feature", _featOutPath.split(".")[1]+".png"])
      _appendDF =pd.DataFrame(_appendData, columns=_appendColumns)
      PATCH_DICTIONARY = PATCH_DICTIONARY.append(_appendDF, ignore_index=True)
    _matrixOutPath = _matrixOutPathSave+"/"+str(_id)
    if not(os.path.exists(_matrixOutPath)):
      os.makedirs(os.path.join(_matrixOutPath))
    _fTypeShort = FEATURE_DEFINE[i][2]
    _matrixOutPath = _matrixOutPath+"/"+_fTypeShort+".json"
    makeJSON(_matrixOutPath, featureCropImgGray.tolist())
    _matrixOutPath = "."+_matrixOutPath.split(".")[1]+".csv"
    ciDF = pd.DataFrame(featureCropImgGray)
    ciDF.to_csv(_matrixOutPath, mode='w', index=False, header=False)
    if _initFlag:
      _appendData = []
      _appendData.append([_id, _stiClass, _stiName, _idx, "matrix", _matrixOutPath.split(".")[1]+".png"])
      _appendDF = pd.DataFrame(_appendData, columns=_appendColumns)
      PATCH_DICTIONARY = PATCH_DICTIONARY.append(_appendDF, ignore_index=True)

#
#
#
# remove this function after debugging
def generateFeatureImage(_featPath, _outDirPath, _featureType, _patchSizse, _fix, color):
  # print("generateFeatureImage")
  featDF = pd.read_csv(_featPath, header=None)
  featNP = featDF.to_numpy()
  featTrain = MinMaxScaler().fit_transform(featNP)
  featTrain = np.abs(featTrain*255-255)
  _savePath = _outDirPath+"feature.png"
  cv2.imwrite(_savePath, featTrain)
  image = cv2.imread(_savePath, cv2.IMREAD_COLOR)
  iWidth, iHeight = image.shape[:2]
  
  _lenPatch = [_patchSizse, _patchSizse]
  _x = _fix[0]
  _y = _fix[1]
  _point = [_x-(_lenPatch[0]/2), _y-(_lenPatch[1]/2)]
  # top bottom left right
  _padding = [0, 0, 0, 0]
  if _point[0] < 0:
    _padding[2] = abs(_point[0])
    _point[0] = 0
    _lenPatch[0] = _lenPatch[0]-_padding[2]
  if _point[0]+_lenPatch[0] > iWidth:
    _padding[3] = (_point[0]+_lenPatch[0]) - iWidth
    _lenPatch[0] = _lenPatch[0] - _padding[3]
  if _point[1] <0:
    _padding[0] = abs(_point[1])
    _point[1] = 0
    _lenPatch[1] = _lenPatch[1]-_padding[0]
  if _point[1]+_lenPatch[1] > iHeight:
    _padding[4] = (_point[1]+_lenPatch[1]) - iHeight
    _lenPatch[1] = _lenPatch[1]-_padding[1]

  _left = int(_point[0])
  _top = int(_point[1])
  _right = int(_point[0]+_lenPatch[0])
  _bottom = int(_point[1]+_lenPatch[1])
  cropImg = image[_top:_bottom, _left:_right]
  cropImg = cv2.copyMakeBorder(cropImg, int(_padding[0]), int(_padding[1]), int(_padding[2]), int(_padding[3]), cv2.BORDER_CONSTANT, value=color)

  _patchFeatSavePath = _outDirPath+_featureType+".png"
  cv2.imwrite(_patchFeatSavePath, cropImg)
  return _patchFeatSavePath
# remove this function after debugging
#
#
#

def appendPatchFeatureImageIndexPath(_featPath, _outDirPath, _featureType, _patchSizse, _fix, color):
  featDF = pd.read_csv(_featPath, header=None)
  featNP = featDF.to_numpy()
  featTrain = MinMaxScaler().fit_transform(featNP)
  featTrain = np.abs(featTrain*255-255)
  _savePath = _outDirPath+"feature.png"
  cv2.imwrite(_savePath, featTrain)
  image = cv2.imread(_savePath, cv2.IMREAD_COLOR)
  iWidth, iHeight = image.shape[:2]
  
  _lenPatch = [_patchSizse, _patchSizse]
  _x = _fix[0]
  _y = _fix[1]
  _point = [_x-(_lenPatch[0]/2), _y-(_lenPatch[1]/2)]
  # top bottom left right
  _padding = [0, 0, 0, 0]
  if _point[0] < 0:
    _padding[2] = abs(_point[0])
    _point[0] = 0
    _lenPatch[0] = _lenPatch[0]-_padding[2]
  if _point[0]+_lenPatch[0] > iWidth:
    _padding[3] = (_point[0]+_lenPatch[0]) - iWidth
    _lenPatch[0] = _lenPatch[0] - _padding[3]
  if _point[1] <0:
    _padding[0] = abs(_point[1])
    _point[1] = 0
    _lenPatch[1] = _lenPatch[1]-_padding[0]
  if _point[1]+_lenPatch[1] > iHeight:
    _padding[4] = (_point[1]+_lenPatch[1]) - iHeight
    _lenPatch[1] = _lenPatch[1]-_padding[1]

  _left = int(_point[0])
  _top = int(_point[1])
  _right = int(_point[0]+_lenPatch[0])
  _bottom = int(_point[1]+_lenPatch[1])
  cropImg = image[_top:_bottom, _left:_right]
  cropImg = cv2.copyMakeBorder(cropImg, int(_padding[0]), int(_padding[1]), int(_padding[2]), int(_padding[3]), cv2.BORDER_CONSTANT, value=color)

  _patchFeatSavePath = _outDirPath+_featureType+".png"
  cv2.imwrite(_patchFeatSavePath, cropImg)
  return _patchFeatSavePath

def analysisPCA(_components, _df, _featuresColumns):
  pca = PCA(n_components=_components)
  pcaTransform = pca.fit_transform(_df[_featuresColumns])
  return pcaTransform

def analysisICA(_components, _df, _featuresColumns):
  ica = FastICA(n_components=_components)
  icaTransform = ica.fit_transform(_df[_featuresColumns])
  return icaTransform

def analysisMDS(_components, _df, _featuresColumns):
  mds = MDS(n_components=_components)
  mdsTranform = mds.fit_transform(_df[_featuresColumns])
  return mdsTranform

def analysisTSNE(_learningRate, _df, _featuresColumns):
  tsne = TSNE(learning_rate=_learningRate)
  tsneTransform = tsne.fit_transform(_df[_featuresColumns])
  return tsneTransform

def transformYeoJohnson(_df, _selectedFeature):
  yeoJohson = PowerTransformer(method='yeo-johnson')
  yeoJohson.fit(_df)
  npTransform = yeoJohson.transform(_df)
  yjDf = pd.DataFrame(npTransform, columns=_selectedFeature)
  return yjDf

def hex_to_rgb(hex):
  hex = hex.lstrip('#')
  hlen = len(hex)
  return tuple(int(hex[i:i + hlen // 3], 16) for i in range(0, hlen, hlen // 3))

def calcPatchFeatureMeanValue(_matrixPath):
  df = pd.read_csv(_matrixPath, header=None)
  sumList = df.sum().values.tolist()
  dataCount = PATCH_SIZE*PATCH_SIZE
  _sum = sum(sumList)
  _mean = _sum/dataCount
  return _mean

# from Data.js
@app.route('/api/data/stimulus', methods=['POST'])
def patchAnalysisStiFix():
  response = {}
  try:
    print(request.form)
    getPatchId = request.form['patchId']
    getStiClass = request.form['stimulusClass']
    getStiName = request.form['stimulusName']
    # getFixOrder = int(request.form['fixationOrder'])
    # getPatchClu = int(request.form['patchCluster'])
    _stimulusPath = "./static/data/"+DATASET+"/stimulus/"+getStiClass+"/"+getStiName+".jpg"
    _accessStiPathJson = "./static/access/stimulus_path.json"
    makeJSON(_accessStiPathJson, _stimulusPath.split(".")[1]+".jpg")

    _fixationPath = "./static/data/"+DATASET+"/"+PARTICIPANT+"/fixation/"+FILTER_NAME+"/"+getStiClass+"_"+getStiName+".csv"
    _fixDF = pd.read_csv(_fixationPath)
    # print("_fixDF")
    # print(_fixDF)
    _orderDF = pd.DataFrame(_fixDF.index.values.tolist(), columns=['order'])
    _mDF = pd.merge(_orderDF, _fixDF[['x','y']], left_index=True, right_index=True)
    # print("_mDF")
    # print(_mDF)

    _allFixPath = "./static/data/"+DATASET+"/"+PARTICIPANT+"/processedFixation/"+FILTER_NAME+"/all_fix.csv"
    _allFixDF = pd.read_csv(_allFixPath)
    is_class = _allFixDF['stimulusClass'] == getStiClass
    is_name = _allFixDF['stimulusName'] == int(getStiName)
    _cnDF = _allFixDF[is_class & is_name]
    # print("_cnDF")
    # print(_cnDF)
    # print("_cnDF[['id']]")
    # print(_cnDF[['id']])
    _leftDF = pd.DataFrame(_cnDF[['id']].values.tolist(), columns=['id'])
    # print("_mDF[['x','y']]")
    # print(_mDF[['x','y']])
    _rightDF = pd.DataFrame(_mDF[['x','y']].values.tolist(), columns=['x','y'])
    _mmDF = pd.merge(_leftDF, _rightDF, left_index=True, right_index=True)
    # print("_mmDF")
    # print(_mmDF)
    print("patch id and location (x,y) data save")
    _patchLocationPath = "./static/access/stimulus_fixations.csv"
    _mmDF.to_csv(_patchLocationPath, mode='w', index=False)

    # _patchDirPath = "./static/access/PATCH_FEATURES/"
    # if os.path.isdir(_patchDirPath):
    #   try:
    #     shutil.rmtree(_patchDirPath)
    #   except Exception as e:
    #     print(e)
    # os.makedirs(os.path.join(_patchDirPath))
    # _featureDirPath = "./static/data/"+DATASET+"/feature/"
    # _featDirList = os.listdir(_featureDirPath)
    # print("_featDirList")
    # print(_featDirList)
    # _mmDF_list = _mmDF.values.tolist()

    patchFeatureImagePath = []
    _patchFeatureImageDirPath = "./static/data/"+DATASET+"/"+PARTICIPANT+"/patch/"
    _patchFeatureImageDirPath = makePath_Filter(FILTER, FILTER_THRESHOLD, _patchFeatureImageDirPath)
    _patchFeatureImageDirPath = _patchFeatureImageDirPath+"/features/"+getPatchId+"/"
    for i in range(0, len(FEATURE_DEFINE)):
      _fType = FEATURE_DEFINE[i][2]
      _path = _patchFeatureImageDirPath+_fType+".png"
      patchFeatureImagePath.append(_path.split('.')[1]+".png")
    # for _feat in _featDirList:
    #   _featPath = "./static/data/"+DATASET+"/feature/"+_feat+"/"+getStiClass+"_"+getStiName+".csv"
    #   _featType = ""
    #   for i in range(0, len(FEATURE_DEFINE)):
    #     if _feat == FEATURE_DEFINE[i][1]:
    #       _featType = FEATURE_DEFINE[i][2]
    #       break
    #   _fixPoint = [_mmDF_list[getFixOrder][1], _mmDF_list[getFixOrder][2]]
    #   _colorBGR = hex_to_rgb(COLORS[getPatchClu])
    #   _colorRGB = [_colorBGR[2], _colorBGR[1], _colorBGR[0]]
    #   # _path = generateFeatureImage(_featPath, _patchDirPath, _featType, PATCH_SIZE, _fixPoint, _colorRGB)
    #   patchFeatureImagePath.append(_path.split('.')[1]+".png")
    # patch feature image path save
    # print("patch feature image path save")
    _patchFeatureImageAccessPath = "./static/access/patch_feature_image.json"
    makeJSON(_patchFeatureImageAccessPath, patchFeatureImagePath)

    response['status'] = 'success'
  except Exception as e:
    response['status'] = 'failed'
    response['reason'] = e
    print(e)
  return json.dumps(response)

# from components/PatchTable.js
@app.route('/api/patchTable/selectedPatchesUpdate', methods=['POST'])
def selectedPatchesUpdate():
  response = {}
  try:
    print(request.form)
    getPatchString = request.form['selectedPatches']
    # split and transfer type 
    _getPatches = getPatchString.split(",")
    selectedPatches = []
    for i in range(0, int(len(_getPatches)/3)):
      selectedPatches.append([int(_getPatches[i*3]), int(_getPatches[i*3+1]), int(_getPatches[i*3+2])])
    _accessPathSelectedPatch = "./static/access/selected_patch_table_index.json"
    makeJSON(_accessPathSelectedPatch, selectedPatches)
    selectedPatchesDF = pd.DataFrame(selectedPatches, columns=['cluster', 'order', 'id'])
    _selectedPatchesAccessPath = "./static/access/selected_patch_table_index.csv"
    selectedPatchesDF.to_csv(_selectedPatchesAccessPath, mode='w', index=False)
    
    response['status'] = 'success'
  except Exception as e:
    response['status'] = 'failed'
    response['reason'] = e
    print(e)
  return json.dumps(response)

# from components/PatchTable.js
@app.route('/api/patchTable/selectFeature', methods=['POST'])
def patchSelectFeature():
  response = {}
  try:
    print(request.form)
    selectedFeature = request.form['selectedFeature']
    _accessPath = "./static/access/patch_selected_feature.json"
    makeJSON(_accessPath, selectedFeature)

    # get patches id data from client and make string data to list
    patchesId = request.form['patchesId']
    patchesIdList = []
    for _pid in patchesId.split(","):
      patchesIdList.append(int(_pid))
    # get patches clu data from client and make string data to list
    patchesClu = request.form['patchesClu']
    patchesCluList = []
    for _pclu in patchesClu.split(","):
      patchesCluList.append(int(_pclu))
    _cluSet = set(patchesCluList)
    cluSetList = list(_cluSet)
    cluSetList.sort()
    # calculate patch features mean value and make list
    patchesFeatureMeanValue = []
    for _id in patchesIdList:
      _matrixPath = "./static/data/"+DATASET+"/"+PARTICIPANT+"/patch/"+FILTER_NAME+"/matrix/"+str(_id)+"/"+FEATURE_DEFINE[int(selectedFeature)][2]+".csv"
      _mVal = calcPatchFeatureMeanValue(_matrixPath)
      patchesFeatureMeanValue.append(_mVal)
    # merge patches clu, id, and feature mean value data
    patchesMergeList = []
    for i in range(0, len(patchesCluList)):
      patchesMergeList.append([patchesCluList[i], patchesIdList[i], patchesFeatureMeanValue[i]])
    patchesDF = pd.DataFrame(patchesMergeList, columns=["clu", "id", "feature"])

    # make list divided by cluster
    # print("make list divided by cluster")
    patchDivByClu = []
    for _clu in cluSetList:
      _isclu = patchesDF['clu'] == _clu
      _ids = patchesDF[_isclu]
      patchDivByClu.append(_ids.values.tolist())
    # append patchTable rendering order index
    for i in range(0, len(patchDivByClu)):
      renderingIndex = 0
      for j in range(0, len(patchDivByClu[i])):
        patchDivByClu[i][j].append(renderingIndex)
        renderingIndex+=1
    # make list sorted by feature mean value
    # print("make list sorted by feature mean value")
    patchDivByCluSorting = []
    for _arr in patchDivByClu:
      _arr.sort(reverse=True, key=lambda x:x[2])
      patchDivByCluSorting.append(_arr)
    # append updated order index
    for i in range(0, len(patchDivByCluSorting)):
      updateIndex = 0
      for j in range(0, len(patchDivByCluSorting[i])):
        patchDivByCluSorting[i][j].append(updateIndex)
        updateIndex+=1
    
    _accessUpdatedPatchDataPath = "./static/access/patchTable_sorting_update.json"
    makeJSON(_accessUpdatedPatchDataPath, patchDivByCluSorting)

    # make list for saving csv
    patchDivByCluSortingCSV = []
    for _clu in patchDivByCluSorting:
      for _p in _clu:
        patchDivByCluSortingCSV.append(_p)
    patchDivByCluSortingDF = pd.DataFrame(patchDivByCluSortingCSV, columns=['cluster', 'id', 'value', 'old', 'current'])
    print("patchDivByCluSortingDF")
    _patchDivByCluSortingAccessPath = "./static/access/patchTable_sorting_update.csv"
    patchDivByCluSortingDF.to_csv(_patchDivByCluSortingAccessPath, mode='w', index=False)

    response['status'] = 'success'
  except Exception as e:
    response['status'] = 'failed'
    response['reason'] = e
    print(e)
  
  return json.dumps(response)

# Structural Similarity Index
# https://scikit-image.org/docs/stable/auto_examples/transform/plot_ssim.html
def similaritySSIM(_select, _target):
  score = SSIM(_select, _target, data_range=_target.max()-_target.min())
  return score

# Mean Square Error
# https://scikit-image.org/docs/stable/auto_examples/transform/plot_ssim.html
def similarityMSE(_select, _target):
  score = np.linalg.norm(_select-_target)
  return score

# Peak Signal-to-Noise Ratio
def similarityPSNR(_select, _target):
  return 0

def similarityCalculation(_method, _matSelected, _matTarget):
  res = 0
  if _method == "SSIM":
    print(_method)
    res = similaritySSIM(_matSelected, _matTarget)
  elif _method == "MSE":
    print(_method)
    res = similarityMSE(_matSelected, _matTarget)
  elif _method == "PSNR":
    print(_method)
    res = similarityPSNR(_matSelected, _matTarget)
  else:
    print("Wrong similarity calculation method")
  return res

def splitDataset(_datasetPath, _splitRatio):
  df = pd.read_csv(_datasetPath)
  fixationCount = len(df.index)
  splitCount = int(fixationCount*_splitRatio)
  IDsDF = df[['id']]
  IDsList = IDsDF.values.tolist() 
  trainList = random.sample(IDsList, splitCount)
  trainList.sort()
  testList = []
  for _id in IDsList:
    _duplicateFlag = False
    for _tid in trainList:
      if _id == _tid:
        _duplicateFlag = True
        break
    if _duplicateFlag:
      continue
    else:
      testList.append(_id)
  return trainList, testList

# from pages/Data.js - Interaction: components/Heatmap.js
@app.route('/api/data/dataRecord', methods=['POST'])
def updateDataRecord():
  response = {}
  try:
    # print(request.form)
    # getSelectedFeature = int(request.form['selectedFeature'])
    selected_stimulus_class_idx = []
    for i in range(0, len(STI_CLASS_DEFINE)):
      _dupFlag = True
      _c = STI_CLASS_DEFINE[i][2]
      for _rmStiClass in REMOVE_CLASSES:
        if _c == _rmStiClass:
          _dupFlag = False
          break
      if _dupFlag:
        selected_stimulus_class_idx.append(i)
    # print("/api/data/dataRecord selected stimulus")
    # print(selected_stimulus_class_idx)
    _all_fix_path = "./static/data/"+DATASET+"/"+PARTICIPANT+"/processedFixation/"+FILTER_NAME+"/"+"all_fix.csv"
    _afDF = pd.read_csv(_all_fix_path)
    
    selectedFixCount = 0
    if len(selected_stimulus_class_idx) == len(STI_CLASS_DEFINE):
      selectedFixCount = len(_afDF)
      # print("if: selectedFixCount: %d"%selectedFixCount)
    else:
      for _cIdx in selected_stimulus_class_idx:
        # print(STI_CLASS_DEFINE[_cIdx][2])
        is_class = _afDF['stimulusClass'] == STI_CLASS_DEFINE[_cIdx][1]
        _cDF = _afDF[is_class]
        selectedFixCount += len(_cDF)
      # print("else: selectedFixCount: %d"%selectedFixCount)
    record_train = int(selectedFixCount*0.7)
    record_test = int(selectedFixCount-record_train)
    if record_train == 0:
      record_test = 0
    
    response['status'] = 'success'
    response['datarecord'] = {
      'train': str(record_train),
      'test': str(record_test)
    }
  except Exception as e:
    response['status'] = 'failed'
    response['reason'] = e
    print(e)
  
  return json.dumps(response)

# from pages/Data.js
@app.route('/api/data/similarity', methods=['POST'])
def similarityProcess():
  response = {}
  try:
    print(request.form)
    getSelectedFeature = int(request.form['selectedFeature'])
    selectedFeatureType = FEATURE_DEFINE[getSelectedFeature][2]
    similarityMethod = request.form['selectedSimilarityOption']
    # get selected pathces
    _selectedPatchesAccessPath = "./static/access/selected_patch_table_index.csv"
    selectedPatchesDF = pd.read_csv(_selectedPatchesAccessPath)
    # get selected pacthes id
    selectedPatchIDList = selectedPatchesDF[['id']].values.tolist()
    # get last selected patch id
    selectedPatchID = selectedPatchIDList[len(selectedPatchIDList)-1][0]
    
    # read patch data on patchTable
    _patchOnTablePath = "./static/access/patchTable_sorting_update.csv"
    patchOnTableDF = pd.read_csv(_patchOnTablePath)
    patchIdsOnTableDF = patchOnTableDF[['id']]
    patchIdsOnTableList = []
    for _v in patchIdsOnTableDF.values.tolist():
      patchIdsOnTableList.append(_v[0])
    
    patchFeatureMatrixPathList = []
    selectedPatchIndexInDF = 0
    _idx = 0
    for _id in patchIdsOnTableList:
      _path = "./static/data/"+DATASET+"/"+PARTICIPANT+"/patch/"+FILTER_NAME+"/features/"+str(int(_id))+"/"+selectedFeatureType+".png"
      _lastSelectedPatchFlag = False
      if int(_id) == int(selectedPatchID):
        selectedPatchIndexInDF = _idx
        _lastSelectedPatchFlag = True
      patchFeatureMatrixPathList.append([_path, int(_id), _lastSelectedPatchFlag])
      _idx+=1
    
    similarityScores = []
    selectedPatchFeature = cv2.imread(patchFeatureMatrixPathList[selectedPatchIndexInDF][0], cv2.IMREAD_GRAYSCALE)
    for _row in patchFeatureMatrixPathList:
      _selectedPatchFlag = _row[2]
      # if target patch equals selected patch, continue the roop
      if _selectedPatchFlag:
        continue
      _targetPath = _row[0]
      targetPatchFeature = cv2.imread(_targetPath, cv2.IMREAD_GRAYSCALE)
      # [id, score]
      _score = similarityCalculation(similarityMethod, selectedPatchFeature, targetPatchFeature)
      similarityScores.append([_row[1], _score])
    similarityScoresDF = pd.DataFrame(similarityScores, columns=['id', 'score'])
    _similarityScoresAccessPath = "./static/access/similarity_scores.csv"
    similarityScoresDF.to_csv(_similarityScoresAccessPath, mode='w', index=False)
    _similarityScoresAccessPath = "./static/access/similarity_scores.json"
    makeJSON(_similarityScoresAccessPath, similarityScores)
    
    _list = similarityScoresDF.values.tolist()
    _list.sort(reverse=True, key=lambda x:x[1])
    _sortingDF = pd.DataFrame(_list, columns=['id', 'score'])
    _sortingDF.dropna(inplace=True)
    _similarityScoresAccessPath = "./static/access/similarity_scores_sorting.csv"
    _sortingDF.to_csv(_similarityScoresAccessPath, mode='w', index=False)

    response['status'] = 'success'
  except Exception as e:
    response['status'] = 'failed'
    response['reason'] = e
    print(e)
  
  return json.dumps(response)

# from pages/Data.js
@app.route('/api/data/process', methods=['POST'])
def corrProcess():
  global DATAPROCESSING
  global CORRELATION_METHOD
  global PATCH_INDEX_PATH
  
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
    # drop unselected stimulus classes
    print("drop unselected stimulus classes")
    print(REMOVE_CLASSES)
    print(STI_CLASS_DEFINE)
    for i in range(0, len(REMOVE_CLASSES)):
      _dsc = REMOVE_CLASSES[i]
      print(_dsc)
      for j in range(0, len(STI_CLASS_DEFINE)):
        if _dsc == STI_CLASS_DEFINE[j][2]:
          _dsc = STI_CLASS_DEFINE[j][1]
          # print(_dsc)
          break
      _dropIdx = afDF[afDF["stimulusClass"]==str(_dsc)].index
      print(_dropIdx)
      afDF = afDF.drop(_dropIdx)
    print(afDF)

    # drop unselected feature types
    print("drop unselected feature types")
    for _dft in REMOVE_FEATURES:
      _del = ""
      for i in range(0, len(FEATURE_DEFINE)):
        if _dft == FEATURE_DEFINE[i][2]:
          _del = FEATURE_DEFINE[i][1]
      afDF = afDF.drop(str(_del), axis=1)
    print(afDF)

    print(REMOVE_FEATURES)
    # selectedFeature = FEATURE_TYPES
    selectedFeature = []
    for i in range(0, len(FEATURE_TYPES)):
      selectedFeature.append(FEATURE_DEFINE[i][2])
    
    for i in range(0, len(FEATURE_TYPES)):
      _ft = FEATURE_DEFINE[i][2]
      for _uft in REMOVE_FEATURES:
        if _ft == _uft:
          selectedFeature.remove(_ft)
    print(selectedFeature)
    # selectedFeature = list(set(selectedFeature))
    # print(selectedFeature)
    
    SELECTED_FEATURE_DEFINE = []
    for i in range(0, len(selectedFeature)):
      for j in range(0, len(FEATURE_DEFINE)):
        if selectedFeature[i] == FEATURE_DEFINE[j][2]:
          SELECTED_FEATURE_DEFINE.append(FEATURE_DEFINE[j])
          break
    print(SELECTED_FEATURE_DEFINE)
    _selectedFeatureDefineAccessPath = "./static/access/selected_feature_define.json"
    makeJSON(_selectedFeatureDefineAccessPath, SELECTED_FEATURE_DEFINE)

    # append patch images path on memory
    PATCH_INDEX_PATH = []
    _outPath = "./static/access/"+DATASET
    if os.path.isdir(_outPath):
      try:
        shutil.rmtree(_outPath)
      except Exception as e:
        print(e)
    print(afDF)
    _fixAllDf = afDF[['id','stimulusClass','stimulusName','x','y']]
    _fixList = _fixAllDf.values.tolist()
    _prev = ""
    _patchIdx = 0
    for _fix in _fixList:
      _id = _fix[0]
      _sc = _fix[1]
      _sn = str(_fix[2]).zfill(3)
      _f = [int(_fix[3]), int(_fix[4])]
      _cur = _sc+"_"+_sn
      if _prev != _cur:
        _patchIdx = 0
      # generatePatch(_id, _f, PATCH_SIZE, _sc, _sn, _patchIdx)
      appendPatchImageIndexPath(_id, _f, PATCH_SIZE, _sc, _sn, _patchIdx)
      _patchIdx+=1
      _prev = _cur
    print("filtered patches are appended")
    _accessPath_patches = "./static/access/index_patches.json"
    makeJSON(_accessPath_patches, PATCH_INDEX_PATH)

    # make dataframe comlumn array
    comlumns_id_features = []
    comlumns_id_features.append("id")
    for _f in selectedFeature:
      comlumns_id_features.append(_f)

    # drop stimulusName, x, and y coordinate columns
    print("drop stimulusClass, stimulusName, x, and y coordinate columns")
    afDF = afDF.drop("stimulusClass", axis=1)
    afDF = afDF.drop("stimulusName", axis=1)
    afDF = afDF.drop("x", axis=1)
    afDF = afDF.drop("y", axis=1)
    # save values where column name == id
    _idSaveList = afDF[['id', 'duration', 'length']].values.tolist()
    _idSaveDF = pd.DataFrame(_idSaveList, columns=['id', 'duration', 'length'])
    print(_idSaveDF)
    # drop id column
    print("drop id column")
    afDF = afDF.drop("id", axis=1)
    afDF = afDF.drop("duration", axis=1)
    afDF = afDF.drop("length", axis=1)
    # data pre-processing: min-max normalization or z-score standardization
    _pProData_list = afDF.values.tolist()
    _pProData_list = dataPreProcessing(DATAPROCESSING, _pProData_list)
    processed_afDF = pd.DataFrame(_pProData_list, columns=selectedFeature)
    sum_id_prcessed_afDF = pd.merge(_idSaveDF, processed_afDF, left_index=True, right_index=True)
    filteredDataPath = "./static/access/filtered_data.csv"
    sum_id_prcessed_afDF.to_csv(filteredDataPath, mode='w', index=False)
    filteredDataPathFP = "./static/access/filtered_data_path.json"
    makeJSON(filteredDataPathFP, filteredDataPath.split(".")[1]+".csv")
    # correlation
    afDFCorrMat = processed_afDF[selectedFeature].iloc[:,range(0,len(selectedFeature))].corr(method=CORRELATION_METHOD)
    afDFCorrMat_access = "./static/access/correlation_mat.csv"
    afDFCorrMat.to_csv(afDFCorrMat_access, mode='w', quoting=2)
    corrMatrix_access_path = "./static/access/corr_matrix_path.json"
    makeJSON(corrMatrix_access_path, afDFCorrMat_access.split(".")[1]+".csv")
    print("calculate and save correlation")
    print(afDFCorrMat)
    
    # generate MDS, PCA, ICA, t-SNE scatter plot data
    # load fixation-feature data
    filteredDataPath = "./static/access/filtered_data.csv"
    filteredFeatDf = pd.read_csv(filteredDataPath)
    filteredIdList = filteredFeatDf[['id', 'duration', 'length']].values.tolist()
    filteredIdDf = pd.DataFrame(filteredIdList, columns=['id', 'duration', 'length'])
    print(filteredIdDf)
    filteredFeatDf = filteredFeatDf.drop("id", axis=1)
    filteredFeatDf = filteredFeatDf.drop("duration", axis=1)
    filteredFeatDf = filteredFeatDf.drop("length", axis=1)
    # raw data
    # Min-max
    # z-score
    # Yeo-Johnson
    transformData = transformYeoJohnson(filteredFeatDf, selectedFeature)
    print("Yeo-Johnson")
    # print(transformData)
    # MDS
    # PCA
    # ICA
    # t-SNE
    tsneAnalysis = analysisTSNE(100, transformData, selectedFeature)
    print("Yeo-Johnosn, t-SNE result: numpy")
    # print(tsneAnalysis)
    yj_tsne_df_coordinates = pd.DataFrame(tsneAnalysis, columns=["x","y"])
    yj_tsne_df = pd.merge(filteredIdDf, yj_tsne_df_coordinates, left_index=True, right_index=True)
    print("Yeo-Johnosn, t-SNE result: DataFrame")
    # print(yj_tsne_df)
    accessPath_YJ_TSNE = "./static/access/yeo_tsne_scatter.csv"
    yj_tsne_df.to_csv(accessPath_YJ_TSNE, mode='w', index=False)
    accessPath_YJ_TSNE_json = "./static/access/yeo_tsne_scatter_path.json"
    makeJSON(accessPath_YJ_TSNE_json, accessPath_YJ_TSNE.split(".")[1]+".csv")
    # k-means
    kmeans = KMeans(n_clusters=5)
    kmeans.fit(transformData[transformData.columns.difference(['id'])])
    kmeans_labels = kmeans.labels_
    kmeans_lebels_df = pd.DataFrame(kmeans_labels, columns=['clu'])
    scatterWithLabel = pd.merge(yj_tsne_df, kmeans_lebels_df, left_index=True, right_index=True)
    accessPath_kmeans = "./static/access/scatter_kmeans.csv"
    scatterWithLabel.to_csv(accessPath_kmeans, mode='w', index=False)
    accessPath_kmeans_json = "./static/access/scatter_kmeans_path.json"
    makeJSON(accessPath_kmeans_json, accessPath_kmeans.split(".")[1]+".csv")
    print("save scatter plot data labeled by k-means clustering")
    
    response['status'] = 'success'
  except Exception as e:
    response['status'] = 'failed'
    response['reason'] = e
    print(e)
  
  return json.dumps(response)

@app.route('/api/correlationMatrix/selectedAxis', methods=['POST'])
def selectedAxis():
  global SCATTER_FEATURES

  response = {}
  try:
    print(request.form)
    x_axis = request.form['feature_1']
    y_axis = request.form['feature_2']
    SCATTER_FEATURES = []
    SCATTER_FEATURES = [x_axis, y_axis]
    
    # generate access file for sharing selected axis
    _path = "./static/access/scatter_axis.json"
    makeJSON(_path, SCATTER_FEATURES)
    print("generate access file for sharing selected axis")

    # generate 2d data for scatter plot
    # 1. all feature data load
    # _featurePath = "./static/data/"+PARTICIPANT+"/processedFixation/"+FILTER_NAME+"/all_fix.csv"
    _featurePath = "./static/access/filtered_data.csv"
    featDF = pd.read_csv(_featurePath)
    print(featDF)
    print("all feature data loaded")
    # 2. select x-axis (feature_1) and y-axis (feature_2) data
    scatterDF = featDF[[SCATTER_FEATURES[0], SCATTER_FEATURES[1]]]
    print(scatterDF)
    print("select x-axis (feature_1) and y-axis (feature_2) data")
    # 3. generate json file for saving 2d data
    _accessPathScatterData = "./static/access/scatter_data.csv"
    scatterDF.to_csv(_accessPathScatterData, mode='w', index=False)
    print("generate json file for saving 2d data")

    response['status'] = 'success'
  except Exception as e:
    response['status'] = 'failed'
    response['reason'] = e
    print(e)
  
  return json.dumps(response)

@app.route('/api/heatmap/removefilter', methods=['POST'])
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
  global FEATURE_DEFINE
  global STIMULUS_CLASSES
  global STI_CLASS_DEFINE
  global FILTER_THRESHOLD
  global PATCH_INDEX_PATH
  global PATCH_DICTIONARY
  
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
    # generate access file
    FEATURE_DEFINE = []
    for i in range(0, len(FEATURE_TYPES)):
      FEATURE_DEFINE.append([i, FEATURE_TYPES[i], "f_"+str(i).zfill(2)])
    _accessFeatureDefine = "./static/access/feature_define.json"
    makeJSON(_accessFeatureDefine, FEATURE_DEFINE)
    # get stimulus classes from server static directory
    STIMULUS_CLASSES = []
    stimulusDir = "./static/data"+"/"+DATASET+"/stimulus"
    STIMULUS_CLASSES = os.listdir(stimulusDir)
    # write current stimulus class list
    stimulusClassFilePath = "./static/data/"+DATASET+"/stimulus_class.csv"
    wf = open(stimulusClassFilePath, "w", newline='', encoding='utf-8')
    writer = csv.writer(wf)
    for _r in STIMULUS_CLASSES:
      # print(_r)
      writer.writerow(_r)
    wf.close()
    # generate access file
    STI_CLASS_DEFINE = []
    for i in range(0, len(STIMULUS_CLASSES)):
      STI_CLASS_DEFINE.append([i, STIMULUS_CLASSES[i], "s_"+str(i).zfill(2)])
    _accessStiClassDataPath = "./static/access/sti_class_define.json"
    makeJSON(_accessStiClassDataPath, STI_CLASS_DEFINE)
    
    # make cache directories path
    fixationDir = "./static/data/"+DATASET+"/"+PARTICIPANT+"/fixation/"
    psdFixDir = "./static/data/"+DATASET+"/"+PARTICIPANT+"/processedFixation/"
    randomDir = "./static/data/"+DATASET+"/"+PARTICIPANT+"/random/"
    spDir = "./static/data/"+DATASET+"/"+PARTICIPANT+"/sp_variance/"
    corrDir = "./static/data/"+DATASET+"/"+PARTICIPANT+"/correlation/"
    patchDir = "./static/data/"+DATASET+"/"+PARTICIPANT+"/patch/"
    # directory exist check
    if not(os.path.exists(fixationDir)):
      os.makedirs(os.path.join(fixationDir))
    if not(os.path.exists(psdFixDir)):
      os.makedirs(os.path.join(psdFixDir))
    if not(os.path.exists(randomDir)):
      os.makedirs(os.path.join(randomDir))
    if not(os.path.exists(spDir)):
      os.makedirs(os.path.join(spDir))
    if not(os.path.exists(corrDir)):
      os.makedirs(os.path.join(corrDir))
    if not(os.path.exists(patchDir)):
      os.makedirs(os.path.join(patchDir))
    fixationDir = makePath_Filter(FILTER, FILTER_THRESHOLD, fixationDir)
    psdFixDir = makePath_Filter(FILTER, FILTER_THRESHOLD, psdFixDir)
    randomDir = makePath_Filter(FILTER, FILTER_THRESHOLD, randomDir)
    spDir = makePath_Filter(FILTER, FILTER_THRESHOLD, spDir)
    corrDir = makePath_Filter(FILTER, FILTER_THRESHOLD, corrDir)
    patchDir = makePath_Filter(FILTER, FILTER_THRESHOLD, patchDir)
    
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
          _fixation = ivtFilter(_rawGaze, PARTICIPANT, _features, FILTER_THRESHOLD[0])
          _random = makeRandomPos(len(_fixation), _features)
        elif FILTER == "idt":
          print("idt filter")
        else:
          print("default: ivt filter")
          _fixation = ivtFilter(_rawGaze, PARTICIPANT, _features, FILTER_THRESHOLD[0])
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
    print("Processed fixation cache works: generate processed fixation cache files")
    if not(os.path.exists(psdFixDir)):
      os.makedirs(os.path.join(psdFixDir))
      # get stimulusClass_stimulusName file list
      fixFileList = os.listdir(fixationDir)

      # make front and end column names
      # | stimulusClass | stimulusName | featType 1(ex. center_bias) | ... | featureType n |
      frontColNames = ["id", "stimulusClass", "stimulusName"]
      endColNames = []
      fullColNames = []
      fullColNames.extend(frontColNames)
      fullColNames.extend(endColNames)

      # make empty pandas DataFrame to save all fixations of stimulus classes and names
      allFixDF = pd.DataFrame(index=range(0, 0), columns=fullColNames)
      for i in range(0, len(FEATURE_TYPES)):
        endColNames.append(FEATURE_DEFINE[i][2])

      _fixId = 0
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
          _gCandNData.append([_fixId, _class, _name])
          _fixId += 1
        _stiDf = pd.DataFrame(_gCandNData, columns=frontColNames)

        # merge two DataFrame
        _fDataFrame = pd.merge(_stiDf, _fixDf, left_index=True, right_index=True)
        # concat fixation data into dataframe for all fixations
        allFixDF = pd.concat([allFixDF, _fDataFrame], ignore_index=True)

      # remove rows include -999 value
      allFixDF = allFixDF.replace(-999, np.nan)
      allFixDF.dropna(inplace=True)
      # save processed fixations cache file
      psdFixationPath_csv = psdFixDir+"/"+"all_fix.csv"
      allFixDF.to_csv(psdFixationPath_csv, mode='w', index=False)
      print("Processed fixation cache works: save processed fixation cache file")

    # if patch images, patch feature images, and patch feature matrix files does not exist
    if not(os.path.exists(patchDir)):
      print("Patch cache works: generate patch images, patch feature images, and patch feature matrix cache files")
      os.makedirs(os.path.join(patchDir))
      # generate patch images
      PATCH_DICTIONARY = []
      PATCH_DICTIONARY = pd.DataFrame(index=range(0,0), columns=['id', 'stimulusClass','stimulusName', 'type', 'path'])
      PATCH_INDEX_PATH = []
      psdFixationPath_csv = psdFixDir+"/"+"all_fix.csv"
      allFixDF = pd.read_csv(psdFixationPath_csv)
      print(allFixDF)
      _fixAllDf = allFixDF[['id', 'stimulusClass','stimulusName','x','y']]
      _fixList = _fixAllDf.values.tolist()
      _prev = ""
      _patchIdx = 0
      for _fix in _fixList:
        _id = _fix[0]
        _sc = _fix[1]
        _sn = str(_fix[2]).zfill(3)
        _f = [int(_fix[3]), int(_fix[4])]
        _cur = _sc+"_"+_sn
        if _prev != _cur:
          _patchIdx = 0
        # generatePatch(_id, _f, PATCH_SIZE, _sc, _sn, _patchIdx)
        generatePatchCache(_id, _f, PATCH_SIZE, _sc, _sn, _patchIdx, True)
        _patchIdx+=1
        _prev = _cur
      print("all patche cache are generated")
      _accessPath_patches = "./static/access/index_patches.json"
      makeJSON(_accessPath_patches, PATCH_INDEX_PATH)
      print(PATCH_DICTIONARY)
      print(PATCH_INDEX_PATH)

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
          # print(_writeMeanPath_csv)

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
          _fixClass.append(_row[4:])
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
        for i in range(0, len(FEATURE_TYPES)):
          featColName.append(FEATURE_DEFINE[i][2])
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
        _sClass = STI_CLASS_DEFINE[i][2]
        _cInNames = fileNameInClass[i]
        for _n in _cInNames:
          spClassNameData.append([_sClass, _n])
      
      spCNDF = pd.DataFrame(spClassNameData, columns=spClassColNames)
      
      spFeatColNames = []
      for i in range(0, len(FEATURE_TYPES)):
        spFeatColNames.append(FEATURE_DEFINE[i][2])
      
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
      for sci in range(0, len(STIMULUS_CLASSES)):
        _sp = []
        _className = STI_CLASS_DEFINE[sci][2]
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
    
    # if correlation/filter directory does not exist
    if not(os.path.exists(corrDir)):
      print("generate correlation/filter directory")
      os.makedirs(os.path.join(corrDir))

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
        _variable = FEATURE_DEFINE[j][2]
        _value = spMeanCacheList[i][j+1]
        spFormHeatmapData.append([_group, _variable, _value])

    spFormHeatmapColumnNames = ["group", "variable", "value"]
    spFHDF = pd.DataFrame(spFormHeatmapData, columns=spFormHeatmapColumnNames)
    print(spFHDF)
    spHeatmapDataPath = spDir+"/"+"sp_heatmap.csv"
    spFHDF.to_csv(spHeatmapDataPath, mode='w', index=False)
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

    # save initial filtered data for scatter plot
    initToList = fixData.values.tolist()
    ifdColumns = []
    ifdColumns.append("id")
    ifdColumns.append("duration")
    ifdColumns.append("length")
    for i in range(0, len(FEATURE_DEFINE)):
      ifdColumns.append(FEATURE_DEFINE[i][2])
    initFdfChanged = pd.DataFrame(initToList, columns=ifdColumns)
    _accessInitDataPath = "./static/access/filtered_data.csv"
    initFdfChanged.to_csv(_accessInitDataPath, mode='w', index=False)
    print("save initial filtered data for scatter plot")

    cols = []
    for i in range(0, len(FEATURE_TYPES)):
      cols.append(FEATURE_DEFINE[i][2])

    # data pre-processing: Raw data | Min-max normalization | z-score standardization
    fixData = fixData.drop("id", axis=1)
    fixData = fixData.drop("duration", axis=1)
    _drop_id_df = fixData.drop("length", axis=1)
    processedData_list_without_id = _drop_id_df.values.tolist()
    processedData_list_without_id = dataPreProcessing(DATAPROCESSING, processedData_list_without_id)
    porcessedFixData = pd.DataFrame(processedData_list_without_id, columns=cols)    
    correlation_mat = porcessedFixData[cols].iloc[:,range(0,len(FEATURE_TYPES))].corr(method=CORRELATION_METHOD)
    # save correlation matrix data file
    correlation_mat_csv = corrDir+"/"+"corr_matrix_all.csv"
    correlation_mat.to_csv(correlation_mat_csv, mode='w', quoting=2)
    correlation_mat_access = "./static/access/correlation_mat.csv"
    correlation_mat.to_csv(correlation_mat_access, mode='w', quoting=2)
    correlation_mat_csv_access = "./static/access/corr_matrix_path.json"
    makeJSON(correlation_mat_csv_access, correlation_mat_access.split(".")[1]+".csv")
    # makeJSON(correlation_mat_csv_access, correlation_mat_csv.split(".")[1]+".csv")
    print("save correlation matrix data file")

    response['status'] = 'success'
    # response['data'] = {
    #   'dataset': DATASET,
    #   'participant': PARTICIPANT,
    #   'filter': FILTER,
    #   'filterName': FILTER_NAME
    # }
    response['filterName'] = FILTER_NAME

    
  except Exception as e:
    response['status'] = 'failed'
    response['reason'] = e
    print(e)

  return json.dumps(response)
