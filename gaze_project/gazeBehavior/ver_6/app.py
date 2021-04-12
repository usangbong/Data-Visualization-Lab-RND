import sys
import os
import csv
import math
import json

import numpy as np
import pandas as pd
import cv2

from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
from collections import OrderedDict

from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import PowerTransformer
from sklearn.manifold import MDS
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans

from flask import *
from flask_cors import CORS

# init dataset name, feature types, and stimulus type
STI_DATASET = ""
STI_CLASS = []
PARTICIPANT = []
FEATURE = []
FEATURE_ordered = ["intensity", "color", "orientation", "curvature", "center_bias", "entropy_rate", "log_spectrum", "HOG"]
COLORS = ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00", "#ffff33", "#a65628", "#f781bf", "#999999"]
PATCH_SIZE = 20

app = Flask(__name__)
if __name__ == '__main__':
  app.jinja_env.auto_reload = True
  app.config['TEMPLATES_AUTO_RELOAD'] = True
  app.run(debug=True)
CORS(app)

######################
# general funcations #
######################
def makeJSON(_path, _data):
  wf = open(_path, "w", newline='', encoding='utf-8')
  wf.write(json.dumps(_data))
  wf.close()

################################
# clustering related functions #
################################
def label_groundTruthFixationMap(_gt, _x, _y):
  if np.array_equal(_gt[_y][_x], np.array([0, 0, 0])):
    return 0
  else:
    return 1

def getFeatureMeanVal(_featDF, _x, _y, _stiWidth, _stiHeight, _patchSize):
  meanVal = 0
  min_x = int(_x - _patchSize/2)
  max_x = int(_x + _patchSize/2)
  if min_x < 0:
    min_x = 0
  if max_x > _stiWidth-1:
    max_x = int(_stiWidth-1)
  min_y = int(_y - _patchSize/2)
  max_y = int(_y + _patchSize/2)
  if min_y < 0:
    min_y = 0
  if max_y > _stiHeight-1:
    max_y = int(_stiHeight-1)
  featNP = _featDF.to_numpy()
  # print("top: %d, bottom: %d, left: %d, right: %d"%(min_y, max_y, min_x, max_x))
  patch = featNP[min_y:max_y, min_x:max_x]
  # print(patch.shape)
  meanVal = patch.mean()
  return meanVal

def dataTransformation(tMethod, df, featureList):
  print("Data transformation method: "+tMethod)
  if tMethod == "raw":
    return df
  elif tMethod == "min_max":
    return dt_minMax(df, featureList)
  elif tMethod == "z_score":
    return dt_zScore(df, featureList)
  elif tMethod == "yeo_johonson":
    return dt_yeoJohnson(df, featureList)
  elif tMethod == "yeo_johonson_min_max":
    return dt_yeoJohnson_minMax(df, featureList)
  else:
    print("ERROR: unavailable data transformation method selected")
    return df

def dt_minMax(df, featureList):
  getColNames = df.columns
  tfDF = df[[getColNames[0], getColNames[1], getColNames[2], getColNames[3]]]
  for featureName in featureList:
    colFeatDF = df[featureName]
    scaler = MinMaxScaler()
    _tf = scaler.fit_transform(colFeatDF.values.reshape(-1, 1))
    # tfDF.loc[:, featureName] = _tf
    tfDF[featureName] = _tf
  return tfDF

def dt_zScore(df, featureList):
  getColNames = df.columns
  tfDF = df[[getColNames[0], getColNames[1], getColNames[2], getColNames[3]]]
  for featureName in featureList:
    colFeatDF = df[featureName]
    scaler = StandardScaler()
    _tf = scaler.fit_transform(colFeatDF.values.reshape(-1, 1))
    tfDF[featureName] = _tf
  return tfDF

def dt_yeoJohnson(df, featureList):
  getColNames = df.columns
  tfDF = df[[getColNames[0], getColNames[1], getColNames[2], getColNames[3]]]
  for featureName in featureList:
    colFeatDF = df[featureName]
    scaler = PowerTransformer(method='yeo-johnson')
    _tf = scaler.fit_transform(colFeatDF.values.reshape(-1, 1))
    tfDF[featureName] = _tf
  return tfDF

def dt_yeoJohnson_minMax(df, featureList):
  _df_1 = dt_yeoJohnson(df, featureList)
  _df_2 = dt_minMax(_df_1, featureList)
  return _df_2

def dataClustering(cMethod):
  print("Data clustering method: "+cMethod)
  if cMethod == "random_forest":
    return dc_randomForest()
  elif cMethod == "dbscan":
    return dc_dbscan()
  elif cMethod == "hdbscan":
    return dc_hdbscan()
  elif cMethod == "k_means":
    return dc_kMeans()
  else:
    print("ERROR: unavailable data clustering method selected")

def dc_randomForest():
  return 0

def dc_dbscan():
  return 0

def dc_hdbscan():
  return 0

def dc_kMeans():
  return 0

################################
# processing related functions #
################################
def featureNameConverter(featName):
  cName = ""
  if featName == "intensity":
    cName = "f0"
  elif featName == "color":
    cName = "f1"
  elif featName == "orientation":
    cName = "f2"
  elif featName == "curvature":
    cName = "f3"
  elif featName == "center_bias":
    cName = "f4"
  elif featName == "entropy_rate":
    cName = "f5"
  elif featName == "log_spectrum":
    cName = "f6"
  elif featName == "HOG":
    cName = "f7"
  else:
    cName = "f8"
  return cName

def featureNameConverter_short(featName):
  cName = ""
  if featName == "center_bias":
    cName = "center_b"
  elif featName == "entropy_rate":
    cName = "entropy_r"
  elif featName == "log_spectrum":
    cName = "log_s"
  else:
    cName = featName
  return cName

#######################################
# scanpath analysis related functions #
#######################################
def gridBasedTransform_style1(_scanpath, _stiWidth, _stiHeight):
  s = ''
  width = _stiWidth
  height = _stiHeight
  _mat = [['a', 'b', 'c', 'd', 'e'], ['f', 'g', 'h', 'i', 'j'], ['k', 'l', 'm', 'n', 'o'], ['p', 'q', 'r', 's', 't'], ['u', 'v', 'w', 'x', 'y']]
  wFactor = width/5
  hFactor = height/5
  for _fix in _scanpath:
    colIdx = int(_fix[0]/wFactor)
    rowIdx = int(_fix[1]/hFactor)
    s = s+_mat[rowIdx][colIdx]
  return s

def _c(ca,i,j,P,Q):
  if ca[i,j] > -1:
    return ca[i,j]
  elif i == 0 and j == 0:
    ca[i,j] = euc_dist(P[0],Q[0])
  elif i > 0 and j == 0:
    ca[i,j] = max(_c(ca,i-1,0,P,Q),euc_dist(P[i],Q[0]))
  elif i == 0 and j > 0:
    ca[i,j] = max(_c(ca,0,j-1,P,Q),euc_dist(P[0],Q[j]))
  elif i > 0 and j > 0:
    ca[i,j] = max(min(_c(ca,i-1,j,P,Q),_c(ca,i-1,j-1,P,Q),_c(ca,i,j-1,P,Q)),euc_dist(P[i],Q[j]))
  else:
    ca[i,j] = float("inf")
  return ca[i,j]

def euc_dist(pt1, pt2):
  return math.sqrt((pt2[0]-pt1[0])*(pt2[0]-pt1[0])+(pt2[1]-pt1[1])*(pt2[1]-pt1[1]))

def makeFixationRange(_fixs, _rad, _stiWidth, _stiHeight):
  _WIDTH = _stiWidth-1
  _HEIGHT = _stiHeight-1
  _rFixs = []
  for _f in _fixs:
    _x = int(_f[0])
    _y = int(_f[1])
    _xMin = int(_x - _rad)
    _xMax = int(_x + _rad)
    _yMin = int(_y - _rad)
    _yMax = int(_y + _rad)
    if _xMin < 0:
      _xMin = 0
    if _xMax > _WIDTH:
      _xMax = _WIDTH
    if _yMin < 0:
      _yMin = 0
    if _yMax > _HEIGHT:
      _yMax = _HEIGHT
    for i in range(_xMin, _xMax):
      for j in range(_yMin, _yMax):
        _rFixs.append([i, j])
  tuplist = [tuple(x) for x in _rFixs]
  ans = list(OrderedDict.fromkeys(tuplist))
  return ans

def getIntersection(_f1, _f2):
  _iCount = 0
  for _p in _f1:
    _xp = _p[0]
    _yp = _p[1]
    for _f in _f2:
      _xf = _f[0]
      _yf = _f[1]
      if _xp == _xf and _yp == _yf:
        _iCount += 1
  return _iCount

def lcs(X, Y, m, n):
  if m == 0 or n == 0:
    return 0
  elif X[m-1] == Y[n-1]:
    return 1 + lcs(X, Y, m-1, n-1)
  else:
    return max(lcs(X, Y, m, n-1), lcs(X, Y, m-1, n))
    
def JaccardCoefficientDistance(_path1, _path2, radius, _stiWidth, _stiHeight):
  _fSet1 = makeFixationRange(_path1, radius, _stiWidth, _stiHeight)
  _fSet2 = makeFixationRange(_path2, radius, _stiWidth, _stiHeight)
  setIntersection = getIntersection(_fSet1, _fSet2)
  # print(len(_fSet1))
  # print(len(_fSet2))
  # print(setIntersection)
  ji = setIntersection/(len(_fSet1)+len(_fSet2)-setIntersection)
  return ji

def BoundingBodx():
  return 0

def DynamicTimeWarping(_path1, _path2):
  distance, path = fastdtw(_path1, _path2, dist=euclidean)
  return distance

def LongestCommonSubsequence(_path1, _path2, _stiWidth, _stiHeight):
  s1 = gridBasedTransform_style1(_path1, _stiWidth, _stiHeight)
  s2 = gridBasedTransform_style1(_path2, _stiWidth, _stiHeight)
  _v = lcs(s1, s2, len(s1), len(s2))
  return _v

def FreechetDistance(_path1, _path2):
  ca = np.ones((len(_path1), len(_path2)))
  ca = np.multiply(ca ,-1)
  dist = _c(ca, len(_path1)-1, len(_path2)-1, _path1, _path2)
  return dist

def EditDistance(_path1, _path2, _stiWidth, _stiHeight, debug=False):
  s1 = gridBasedTransform_style1(_path1, _stiWidth, _stiHeight)
  s2 = gridBasedTransform_style1(_path2, _stiWidth, _stiHeight)
  
  if len(s1) < len(s2):
    return EditDistance(_path2, _path1, _stiWidth, _stiHeight, debug)
  if len(s2) == 0:
    return len(s1)
  previous_row = range(len(s2) + 1)
  for i, c1 in enumerate(s1):
    current_row = [i + 1]
    for j, c2 in enumerate(s2):
      insertions = previous_row[j + 1] + 1
      deletions = current_row[j] + 1
      substitutions = previous_row[j] + (c1 != c2)
      current_row.append(min(insertions, deletions, substitutions))
    if debug:
      print(current_row[1:])
    previous_row = current_row
  return previous_row[-1]

def computeScanpathSimilarity(_method, _path1, _path2, _stiImg):
  stiHeight, stiWidth = _stiImg.shape[:2]
  simVal = 0
  if _method == 'jd':
    simVal = JaccardCoefficientDistance(_path1, _path2, PATCH_SIZE/2, stiWidth, stiHeight)
  elif _method == 'dtw':
    simVal = DynamicTimeWarping(_path1, _path2)
  elif _method == 'lcs':
    simVal = LongestCommonSubsequence(_path1, _path2, stiWidth, stiHeight)
  elif _method == 'fd':
    simVal = FreechetDistance(_path1, _path2)
  elif _method == 'ed':
    # simVal = EditDistance(_path1, _path2, True)
    simVal = EditDistance(_path1, _path2, stiWidth, stiHeight)
  elif _method == 'bb':
    print(_method)
  else:
    print("ERROR: wrong scanpath similarity calculation method selected")
  return simVal

def IQRclusteringRange(Q1, Q3, val):
  clu = 0
  IQR = Q3 - Q1
  minimum = Q1-(1.5*IQR)
  maxmum = Q3+(1.5*IQR)

  if val < minimum:
    clu = 2
  elif val >= minimum and val < Q1:
    clu = 3
  elif val >= Q1 and val < Q3:
    clu = 4
  elif val >= Q3 and val < maxmum:
    clu = 5
  else:
    clu = 6
  return clu

##################################
# patch clustering analysis APIs #
##################################
@app.route('/api/clustering/loadCacheList', methods=['POST'])
def clustering_loadCacheList():
  print("clustering_loadCacheList")
  print(request.form)
  response = {}
  try:
    cacheDirPath = "./static/__cache__/"
    filesInDir = os.listdir(cacheDirPath)
    cacheFileList = []
    for fileName in filesInDir:
      fileType = fileName.split("_")[0]
      if fileType == "cache":
        cacheFileList.append(fileName)

    response['status'] = 'success'
    response['caches'] = cacheFileList
    
  except Exception as e:
    response['status'] = 'failed'
    response['reason'] = e
    print(e)
  return json.dumps(response)

@app.route('/api/clustering/processing', methods=['POST'])
def clustering_processing():
  print("clustering_processing")
  print(request.form)
  response = {}
  try:
    GET_TRANSFORMATION_METHOD = request.form['transformationMethod']
    GET_CLUSTERING_METHOD = request.form['clusteringMethod']
    print(GET_TRANSFORMATION_METHOD)
    print(GET_CLUSTERING_METHOD)
    print(PARTICIPANT)
    print(FEATURE_ordered)

    
    midCacheFlag = False
    midCacheFilePath = "./static/__cache__/midcache.csv"

    fixDirPath = "./static/fix/"
    featureDirPath = "./static/feature/"
    groundTruthDirPath = "./static/ground_truth/"
    aggregatedDataList = []
    for observer in PARTICIPANT:
      dataName = observer.split("/")[0]
      className = observer.split("/")[1]
      stiNameDir = observer.split("/")[2]
      stiName = stiNameDir.split("_")[0]
      stiExt = stiNameDir.split("_")[1]
      userId = observer.split("/")[3]
      if os.path.exists(midCacheFilePath):
        midCacheFlag = True
        break
      
      fixFilePath = fixDirPath + dataName +"/"+ className +"/"+ stiNameDir +"/"+ userId+".csv"
      print(fixFilePath)
      fixDF = pd.read_csv(fixFilePath)
      fixList = fixDF.values.tolist()
      gtFixMapPath = groundTruthDirPath + dataName +"/"+ className +"/"+ stiName +"."+ stiExt
      groundTruthFixMap = cv2.imread(gtFixMapPath)
      fmHeight, fmWidth = groundTruthFixMap.shape[:2]
      for _fp in fixList:
        _x = int(_fp[0])
        _y = int(_fp[1])
        _label = label_groundTruthFixationMap(groundTruthFixMap, _x, _y)
        _midStack = [observer, _x, _y, _label]
        for _f in FEATURE_ordered:
          featureFilePath = featureDirPath + _f +"/"+ dataName +"/"+ className +"/"+ stiName +".csv"
          featureDF = pd.read_csv(featureFilePath)
          fMean = getFeatureMeanVal(featureDF, _x, _y, fmWidth, fmHeight, PATCH_SIZE)
          _midStack.append(fMean)
        aggregatedDataList.append(_midStack)
    
    aggDF = []
    dfCols = ["id", "x", "y", "label"]
    for featName in FEATURE_ordered:
      dfCols.append(featName)
    if midCacheFlag == False:
      print("make file: "+midCacheFilePath)
      aggDF = pd.DataFrame(aggregatedDataList, columns=dfCols)
      aggDF.to_csv(midCacheFilePath, mode='w', index=False)
    else:
      print("load file: "+midCacheFilePath)
      aggDF = pd.read_csv(midCacheFilePath)
    
    # data transformation
    tfDF = dataTransformation(GET_TRANSFORMATION_METHOD, aggDF, FEATURE_ordered)
    print(tfDF)
    tsne = TSNE(learning_rate= 100, random_state=42)
    tsneDR = tsne.fit_transform(tfDF[FEATURE_ordered])
    print(tsneDR)

    # data clustering



    response['status'] = 'success'
  except Exception as e:
    response['status'] = 'failed'
    response['reason'] = e
    print(e)
  return json.dumps(response)



##########################
# scanpath analysis APIs #
##########################
@app.route('/api/scanpath/calcSimilarity', methods=['POST'])
def scanpath_calc_similarity():
  print(request.form)
  response = {}
  try:
    GET_SELECTED_SCANPATH_SIMILARITY_METHOD = request.form['scanpathSimilarityMethod']
    GET_SELECTED_SCANPATH_FILES = request.form['selectedScanpaths']
    splitSelectedScanpathFiles = GET_SELECTED_SCANPATH_FILES.split("-")
    GET_SELECTED_MAIN_SCANPATH = request.form['mainScanpath']

    print(GET_SELECTED_SCANPATH_SIMILARITY_METHOD)
    # print(GET_SELECTED_SCANPATH_FILES)
    print(splitSelectedScanpathFiles)
    print(GET_SELECTED_MAIN_SCANPATH)

    # load scanpath files
    fixationDirPath = "./static/fix/"
    scanpathList = []
    for _fixFile in splitSelectedScanpathFiles:
      mainFlag = False
      if _fixFile == GET_SELECTED_MAIN_SCANPATH:
        mainFlag = True
      filePath = fixationDirPath + _fixFile +".csv"
      fixDF = pd.read_csv(filePath)
      fixList = fixDF.values.tolist()
      scanpathList.append([mainFlag, _fixFile, fixList])
    
    # check main scanpath and save it
    # check fixations from same visual stimluls
    mainScanpathIndex = 0
    mainScanpath = []
    # prevStiName = ""
    diffStiFlag = False
    for i in range(0, len(scanpathList)):
      if scanpathList[i][0] == True:
        mainScanpathIndex = i
        mainScanpath = scanpathList[i]
      # curStiName = scanpathList[i][1].split("/")[2]
      # if i==0:
      #   prevStiName = curStiName
      # else:
      #   if prevStiName != curStiName:
      #     diffStiFlag = True
      # prevStiName = curStiName
    
    # calculation scanpath similarity
    stiPath = ""
    if diffStiFlag == False:
      splitValue = mainScanpath[1].split("/")
      datasetName = splitValue[0]
      className = splitValue[1]
      splitStiName = splitValue[2].split("_")
      stiName = ""
      if len(splitStiName) == 2:
        stiName = splitStiName[0] +"."+ splitStiName[1]
      else:
        for i in range(0, len(splitStiName)):
          if i == len(splitStiName)-1:
            stiName = stiName +"."+ splitStiName[i]
          else:
            if stiName == "":
              stiName = splitStiName[i]
            else:
              stiName = stiName +"_"+ splitStiName[i]
      stiPath = "./static/stimulus/"+ datasetName +"/"+ className +"/"+ stiName
    # print("stimulus path: ")
    # print(stiPath)
    scanpathSimilarityValueList = []
    stiImage = cv2.imread(stiPath)
    for i in range(0, len(scanpathList)):
      if i == mainScanpathIndex:
        continue
      targetScanpath = scanpathList[i][2]
      sv = computeScanpathSimilarity(GET_SELECTED_SCANPATH_SIMILARITY_METHOD, mainScanpath[2], targetScanpath, stiImage)
      scanpathSimilarityValueList.append([mainScanpath[1], scanpathList[i][1], sv])
      # print("Similarity between main with"+str(i)+" scanpath: "+str(sv))
    
    # get scanpath similarity calculation results
    similarityValueList = []
    for simData in scanpathSimilarityValueList:
      similarityValueList.append(simData[2])
    
    # clustering with IQR
    svlSeries = pd.Series(similarityValueList)
    Q1 = svlSeries.quantile(.25)
    Q3 = svlSeries.quantile(.75)

    similarityBaseClusteringIQR = []
    for i in range(0, len(scanpathSimilarityValueList)):
      _s = similarityValueList[i]
      simClu = IQRclusteringRange(Q1, Q3, _s)
      similarityBaseClusteringIQR.append({'main':scanpathSimilarityValueList[i][0], 'target':scanpathSimilarityValueList[i][1], 'svalue':scanpathSimilarityValueList[i][2], 'sclu':simClu})

    
    response['status'] = 'success'
    response['scanpathSimilarityValues'] = similarityBaseClusteringIQR
  except Exception as e:
    response['status'] = 'failed'
    response['reason'] = e
    print(e)
  return json.dumps(response)

###################
# processing APIs #
###################
@app.route('/api/processing/genFixationDataList', methods=['POST'])
def processing_gen_fixationDataList():
  print("processing_gen_fixationDataList")
  print(request.form)
  response = {}
  try:
    GET_PARTICIPANT = request.form['participantList']
    split_get_participant = GET_PARTICIPANT.split("-")

    # generate fixations (scanpath) data list
    PARTICIPANT_FIX_FILE_LIST = []
    for _participant in split_get_participant:
      split_pData = _participant.split("/")
      sDataset = split_pData[0]
      sSemanticClass = split_pData[1]
      sFixDirName = split_pData[2]
      sParticipantFixFileName = split_pData[3] +".csv"
      fixFilePath = "./static/fix/"+ sDataset +"/"+ sSemanticClass +"/"+ sFixDirName +"/"+ sParticipantFixFileName
      if not(os.path.exists(fixFilePath)):
        continue
      PARTICIPANT_FIX_FILE_LIST.append([split_pData, fixFilePath])
    FIX_DATA_LIST = []
    for fixFilePath in PARTICIPANT_FIX_FILE_LIST:
      _id = fixFilePath[0]
      _path = fixFilePath[1]
      df = pd.read_csv(_path)
      dfList = df.values.tolist()
      FIX_DATA_LIST.append([_id, dfList])

    # generate aggregated fixation patches image
    fixatedPatchPath = "./static/output_image_patch/"
    patchPos = 0
    aggregatedPatchImage = 0
    aggregatedPatchPath = "./static/__cache__/aggregated_patch.png"
    # patchInfo = []
    firstFlag = True
    for i in range(0, len(FIX_DATA_LIST)):
      fixData = FIX_DATA_LIST[i]
      dataName = fixData[0][0]
      className = fixData[0][1]
      stiName = fixData[0][2]
      userId = fixData[0][3]
      patchDirPath = fixatedPatchPath + dataName +"/"+ className +"/"+ stiName +"/"
      scanpath = fixData[1]
      _fixs = []
      for j in range(0, len(scanpath)):
        _fixs.append({'index': str(j).zfill(3), 'px': patchPos, 'py': 0})
        patchPath = patchDirPath + userId +"_"+ str(j).zfill(3) +".png"
        # print(patchPath)
        patch = 0
        if os.path.exists(patchPath):
          patch = cv2.imread(patchPath)
          if firstFlag == True:
            aggregatedPatchImage = patch.copy()
            patchPos = patchPos+PATCH_SIZE
            firstFlag = False
            continue
        else:
          patch = np.empty((PATCH_SIZE, PATCH_SIZE, 3), dtype=np.uint8)
          if firstFlag == True:
            aggregatedPatchImage = patch.copy()
            patchPos = patchPos+PATCH_SIZE
            firstFlag = False
            continue
        processAggImg = np.hstack((aggregatedPatchImage, patch))
        aggregatedPatchImage = processAggImg.copy()
        patchPos = patchPos+PATCH_SIZE
      FIX_DATA_LIST[i].append(_fixs)
    cv2.imwrite(aggregatedPatchPath, aggregatedPatchImage)

    response['status'] = 'success'
    response['fixDataList'] = FIX_DATA_LIST
  except Exception as e:
    response['status'] = 'failed'
    response['reason'] = e
    print(e)
  return json.dumps(response)


@app.route('/api/processing/loadFixationDataList', methods=['POST'])
def processing_load_fixationDataList():
  global PARTICIPANT
  print(request.form)
  response = {}
  try:
    GET_STI_NAMES = request.form['stiList']
    split_sti_names = GET_STI_NAMES.split("-")
    sti_files_list = []
    for sti in split_sti_names:
      datasetName = sti.split("/")[0]
      semanticClassName = sti.split("/")[1]
      stiName = sti.split("/")[2].split(".")[0]
      stiExt = sti.split("/")[2].split(".")[1]
      sti_files_list.append([datasetName, semanticClassName, stiName, stiExt])

    PARTICIPANT = []
    for sti in sti_files_list:
      _path = './static/fix/'+ sti[0] +"/"+ sti[1] +"/"+ sti[2] +"_"+ sti[3] +"/"
      if not(os.path.exists(_path)):
        continue
      participantList = os.listdir(_path)
      for _p in participantList:
        _pdata = sti[0] +"/"+ sti[1] +"/"+ sti[2] +"_"+ sti[3] +"/" + _p.split(".")[0]
        PARTICIPANT.append(_pdata)
    # PARTICIPANT = list(set(PARTICIPANT))
    
    # # temp test 20210409 move the code position
    # for sti in sti_files_list:
    #   _path = './static/ground_truth/'+ sti[0] +"/"+ sti[1] +"/"+ sti[2] +"."+ sti[3]
    #   print('_path')
    #   print(_path)
    #   print('test')
    #   groundTruthFixationMapToMat(_path)


    response['status'] = 'success'
    response['participantList'] = PARTICIPANT
  except Exception as e:
    response['status'] = 'failed'
    response['reason'] = e
    print(e)
  return json.dumps(response)


@app.route('/api/processing/loadStimulusNames', methods=['POST'])
def processing_load_stimulusFileNames():
  print(request.form)
  response = {}
  try:
    GET_SEMANTIC_CLASS = request.form['stiClass']
    SEMANTIC_CLASS = GET_SEMANTIC_CLASS.split("-")
    print(SEMANTIC_CLASS)
    STIMULUS_LIST = []
    for stiClass in SEMANTIC_CLASS:
      datasetName = stiClass.split("/")[0]
      semanticClass = stiClass.split("/")[1]
      stiDirPath = "./static/stimulus/"+datasetName+"/"+semanticClass+"/"
      stiList = os.listdir(stiDirPath)
      for stiName in stiList:
        _stiPath = stiDirPath + stiName
        stiImg = cv2.imread(_stiPath)
        stiHeight, stiWidth = stiImg.shape[:2]
        STIMULUS_LIST.append([datasetName+"/"+semanticClass+"/"+stiName, stiWidth, stiHeight])
    # print(STIMULUS_LIST)
    
    response['status'] = 'success'
    response['stimulusNames'] = STIMULUS_LIST
    
  except Exception as e:
    response['status'] = 'failed'
    response['reason'] = e
    print(e)
  return json.dumps(response)

@app.route('/api/processing/stiDataset', methods=['POST'])
def processing_stiDataset():
  print("processing_stiDataset")
  global STI_DATASET
  global STI_CLASS
  global PARTICIPANT
  global FEATURE
  print(request.form)
  response = {}
  try:
    GET_STI_DATASET = request.form['stiDataset']
    STI_DATASET = []
    if GET_STI_DATASET == "all":
      STI_DATASET = os.listdir("./static/stimulus/")
    else:
      STI_DATASET = GET_STI_DATASET.split("/")
      for stiDataset in STI_DATASET:
        if stiDataset == "all":
          STI_DATASET = os.listdir("./static/stimulus/")
          break
    print(STI_DATASET)
    
    STI_CLASS = []
    for stiDataset in STI_DATASET:
      _path = "./static/stimulus/"+stiDataset+"/"
      stiClassList = os.listdir(_path)
      STI_CLASS.append([stiDataset, stiClassList])
    # print(STI_CLASS)
    
    FEATURE = []
    featureDirPath = "./static/feature/"
    FEATURE = os.listdir(featureDirPath)

    # move last location of participant selectAction function
    spResFilePath = "./static/sp.csv"
    spDF = pd.read_csv(spResFilePath)
    spConvertedList = []
    spNanCountList = []
    spConvertedColumns = ['group', 'variable', 'value']
    
    for selectedDataset in STI_DATASET:
      _idx = 0
      isStidataset = spDF['dataset'] == selectedDataset
      filteredSPDF = spDF[isStidataset]
      for index, row in filteredSPDF.iterrows():
        variable = row['dataset'][0]+str(_idx).zfill(2)
        _idx = _idx + 1
        for featName in FEATURE:
          spCountStr = row[featName]
          spSplit = spCountStr.split("_")[1].split("/")
          spOverCount = spSplit[0]
          spNanCount = spSplit[1]
          stiCount = spSplit[2]
          spPer = (float(spOverCount)/float(stiCount))*100
          spConvertedList.append([featureNameConverter_short(featName), variable, spPer])
          # spConvertedList.append([featureNameConverter(featName), variable, spPer])
          spNanCountList.append([featureNameConverter_short(featName), variable, int(spNanCount)])
          # spNanCountList.append([featureNameConverter(featName), variable, int(spNanCount)])
    spCDF = pd.DataFrame(spConvertedList, columns=spConvertedColumns)
    spCDF.to_csv("./static/__cache__/sp_cvt.csv", mode='w', index=False, header=True)
    spNCDF = pd.DataFrame(spNanCountList, columns=spConvertedColumns)
    spNCDF.to_csv("./static/__cache__/sp_nan.csv", mode='w', index=False, header=True)
    

    response['status'] = 'success'
    response['classList'] = STI_CLASS
    response['featureList'] = FEATURE
    
  except Exception as e:
    response['status'] = 'failed'
    response['reason'] = e
    print(e)

  return json.dumps(response)
