import sys
import os
import csv
import math
import json
from datetime import datetime

import numpy as np
import pandas as pd
import cv2

from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
from collections import OrderedDict

from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import PowerTransformer
from sklearn.decomposition import PCA
from sklearn.decomposition import FastICA
from sklearn.manifold import MDS
from sklearn.manifold import TSNE
from sklearn.cross_decomposition import PLSRegression
from sklearn.cluster import KMeans
from sklearn.pipeline import make_pipeline
from scipy.stats import entropy

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

########################################
# saliency evaluation metirc fucntions #
########################################
def NSS(saliency_map, ground_truth_map):
  """"
  normalized scanpath saliency between two different
  saliency maps as the mean value of the normalized saliency map at
  fixation locations.
    Computer NSS score.
    :param saliency_map : predicted saliency map
    :param fixation_map : ground truth saliency map.
    :return score: float : score
  """
  if not isinstance(saliency_map, np.ndarray):
    saliency_map = np.array(saliency_map)

  if not isinstance(ground_truth_map, np.ndarray):
    ground_truth_map = np.array(ground_truth_map)

  if saliency_map.size != ground_truth_map.size:
    saliency_map = cv2.resize(saliency_map, dsize=(ground_truth_map.shape[1], ground_truth_map.shape[0]))
    # saliency_map = imresize(saliency_map, fixation_map.shape)

  MAP = (saliency_map - saliency_map.mean()) / (saliency_map.std())
  mask = ground_truth_map.astype(np.bool)
  score = MAP[mask].mean()
  return score

def CC(saliency_map, ground_truth_map):
  """
  This finds the linear correlation coefficient between two different
  saliency maps (also called Pearson's linear coefficient).
  score=1 or -1 means the maps are correlated
  score=0 means the maps are completely uncorrelated
  saliencyMap1 and saliencyMap2 are 2 real-valued matrices
    Computer CC score .
    :param saliency_map : first saliency map
    :param saliency_map_gt : second  saliency map.
    :return score: float : score
  """
  if not isinstance(saliency_map, np.ndarray):
    saliency_map = np.array(saliency_map, dtype=np.float32)
  elif saliency_map.dtype != np.float32:
    saliency_map = saliency_map.astype(np.float32)

  if not isinstance(ground_truth_map, np.ndarray):
    ground_truth_map = np.array(ground_truth_map, dtype=np.float32)
  elif saliency_map.dtype != np.float32:
    ground_truth_map = ground_truth_map.astype(np.float32)

  if saliency_map.size != ground_truth_map.size:
    saliency_map = cv2.resize(saliency_map, dsize=(ground_truth_map.shape[1], ground_truth_map.shape[0]))
    # saliency_map = imresize(saliency_map, ground_truth_map.shape)

  saliency_map = (saliency_map - saliency_map.mean()) / (saliency_map.std())
  ground_truth_map = (ground_truth_map - ground_truth_map.mean()) / (ground_truth_map.std())
  score = np.corrcoef(saliency_map.flatten(),ground_truth_map.flatten())[0][1]
  return score

def KLdiv(saliency_map, ground_truth_map):
  """
  This finds the KL-divergence between two different saliency maps when
  viewed as distributions: it is a non-symmetric measure of the information
  lost when saliencyMap is used to estimate fixationMap.
    Computer KL-divergence.
    :param saliency_map : predicted saliency map
    :param fixation_map : ground truth saliency map.
    :return score: float : score
  """
  if saliency_map.size != ground_truth_map.size:
    saliency_map = cv2.resize(saliency_map, dsize=(ground_truth_map.shape[1], ground_truth_map.shape[0]))

  if not isinstance(saliency_map, np.ndarray):
    saliency_map = np.array(saliency_map, dtype=np.float32)
  elif saliency_map.dtype != np.float32:
    saliency_map = saliency_map.astype(np.float32)

  if not isinstance(ground_truth_map, np.ndarray):
    ground_truth_map = np.array(ground_truth_map, dtype=np.float32)
  elif ground_truth_map.dtype != np.float32:
    ground_truth_map = ground_truth_map.astype(np.float32)

  EPS = np.finfo(np.float32).eps
  # the function will normalize maps before computing Kld
  score = entropy(saliency_map.flatten() + EPS, ground_truth_map.flatten() + EPS)
  return score

def AUC(saliency_map, ground_truth_map):
  """Computes AUC for given saliency map 'saliency_map' and given
  fixation map 'fixation_map'
  """
  def area_under_curve(predicted, actual, labelset):
    def roc_curve(predicted, actual, cls):
      si = np.argsort(-predicted)
      tp = np.cumsum(np.single(actual[si]==cls))
      fp = np.cumsum(np.single(actual[si]!=cls))
      tp = tp/np.sum(actual==cls)
      fp = fp/np.sum(actual!=cls)
      tp = np.hstack((0.0, tp, 1.0))
      fp = np.hstack((0.0, fp, 1.0))
      return tp, fp
    def auc_from_roc(tp, fp):
      h = np.diff(fp)
      auc = np.sum(h*(tp[1:]+tp[:-1]))/2.0
      return auc

    tp, fp = roc_curve(predicted, actual, np.max(labelset))
    auc = auc_from_roc(tp, fp)
    return auc

  ground_truth_map = (ground_truth_map>0.7).astype(int)
  salShape = saliency_map.shape
  fixShape = ground_truth_map.shape

  predicted = saliency_map.reshape(salShape[0]*salShape[1], -1, order='F').flatten()
  actual = ground_truth_map.reshape(fixShape[0]*fixShape[1], -1, order='F').flatten()
  labelset = np.arange(2)
  return area_under_curve(predicted, actual, labelset)

def SAUC(saliency_map, ground_truth_map, shuf_map=np.zeros((480,640)), step_size=.01):
  # shuf_map=np.zeros(ground_truth_map.shape)
  # shuf_map = ground_truth_map
  """
    please cite:  https://github.com/NUS-VIP/salicon-evaluation
    calculates shuffled-AUC score.
    :param salinecy_map : predicted saliency map
    :param fixation_map : ground truth saliency map.
    :return score: int : score
  """
  
  saliency_map -= np.min(saliency_map)
  ground_truth_map = np.vstack(np.where(ground_truth_map!=0)).T
  
  if np.max(saliency_map) > 0:
    saliency_map = saliency_map / np.max(saliency_map)
  Sth = np.asarray([ saliency_map[y-1][x-1] for y,x in ground_truth_map ])
  
  Nfixations = len(ground_truth_map)
  others = np.copy(shuf_map)
  for y,x in ground_truth_map:
    others[y-1][x-1] = 0

  ind = np.nonzero(others) # find fixation locations on other images
  nFix = shuf_map[ind]
  randfix = saliency_map[ind]
  Nothers = sum(nFix)

  allthreshes = np.arange(0,np.max(np.concatenate((Sth, randfix), axis=0)),step_size)
  allthreshes = allthreshes[::-1]
  tp = np.zeros(len(allthreshes)+2)
  fp = np.zeros(len(allthreshes)+2)
  tp[-1]=1.0
  fp[-1]=1.0
  tp[1:-1]=[float(np.sum(Sth >= thresh))/Nfixations for thresh in allthreshes]
  fp[1:-1]=[float(np.sum(nFix[randfix >= thresh]))/Nothers for thresh in allthreshes]
  score = np.trapz(tp,fp)
  return score

def IG(saliency_map, ground_truth_map, baseline_map=np.zeros((480,640))):
  """
    please cite:
    calculates Information gain score.
    :param salinecy_map : predicted saliency map
    :param fixation_map : ground truth saliency map.
    :param baseline_fixation_map : a baseline fixtion map
    :return score: int : score
  """
  if saliency_map.size != ground_truth_map.size:
    saliency_map = cv2.resize(saliency_map, dsize=(ground_truth_map.shape[1], ground_truth_map.shape[0]))

  if not isinstance(saliency_map, np.ndarray):
    saliency_map = np.array(saliency_map, dtype=np.float32)
  elif saliency_map.dtype != np.float32:
    saliency_map = saliency_map.astype(np.float32)

  if not isinstance(ground_truth_map, np.ndarray):
    ground_truth_map = np.array(ground_truth_map, dtype=np.float32)
  elif ground_truth_map.dtype != np.float32:
    ground_truth_map = ground_truth_map.astype(np.float32)

  if not isinstance(baseline_map, np.ndarray):
    baseline_map = np.array(baseline_map, dtype=np.float32)
  elif ground_truth_map.dtype != np.float32:
    baseline_map = baseline_map.astype(np.float32)

  saliency_map = (saliency_map - saliency_map.min()) / (saliency_map.max() - saliency_map.min())
  saliency_map = saliency_map / saliency_map.sum()
  baseline_map = (baseline_map - baseline_map.min()) / (baseline_map.max() - baseline_map.min())
  baseline_map = baseline_map / baseline_map.sum()
  fixs = ground_truth_map.astype(np.bool)
  EPS = np.finfo(np.float32).eps
  return (np.log2(EPS + saliency_map[fixs]) - np.log2(EPS + baseline_map[fixs])).mean()

def SIM(saliency_map, ground_truth_map):
  """
    Compute similarity score.
    :param saliency_map : predicted saliency map
    :param fixation_map : ground truth saliency map.
    :return score: float : score
  """
  if saliency_map.size != ground_truth_map.size:
    saliency_map = cv2.resize(saliency_map, dsize=(ground_truth_map.shape[1], ground_truth_map.shape[0]))
    
  if not isinstance(saliency_map, np.ndarray):
    saliency_map = np.array(saliency_map, dtype=np.float32)
  elif saliency_map.dtype != np.float32:
    saliency_map = saliency_map.astype(np.float32)

  if not isinstance(ground_truth_map, np.ndarray):
    ground_truth_map = np.array(ground_truth_map, dtype=np.float32)
  elif ground_truth_map.dtype != np.float32:
    ground_truth_map = ground_truth_map.astype(np.float32)

  saliency_map = (saliency_map - saliency_map.min()) / (saliency_map.max() - saliency_map.min())
  saliency_map = saliency_map / saliency_map.sum()
  ground_truth_map = (ground_truth_map - ground_truth_map.min()) / (ground_truth_map.max() - ground_truth_map.min())
  ground_truth_map = ground_truth_map / ground_truth_map.sum()
  return np.minimum(saliency_map, ground_truth_map).sum()

def normalize_map(s_map):
  # normalize the salience map (as done in MIT code)
  norm_s_map = (s_map - np.min(s_map))/((np.max(s_map)-np.min(s_map))*1.0)
  return norm_s_map
  

######################
# overview functions #
######################
def overview_count(stimulusNames, datasetName, semanticClass):
  fixDirPath = "./static/fix/"+ datasetName +"/"+ semanticClass +"/"
  countList = []
  for stiFileFullName in stimulusNames:
    stiName = stiFileFullName.split(".")[0]
    stiExe = stiFileFullName.split(".")[1]
    humanFixationMapPath = "./static/ground_truth/"+ datasetName +"/"+ semanticClass +"/"+ stiName +".jpg"
    
    humanFixationMap = cv2.imread(humanFixationMapPath)
    fixFileDirPath = fixDirPath + stiName +"_"+ stiExe +"/"
    fixFileList = os.listdir(fixFileDirPath)
    patchList = []
    patchList_on = []
    patchList_out = []
    for fixFileName in fixFileList:
      path = fixFileDirPath + fixFileName
      pDF = pd.read_csv(path, header=None)
      pList = pDF.values.tolist()
      for _p in pList:
        patchList.append([_p[0], _p[1]])
        labelVal = label_groundTruthFixationMap(humanFixationMap, int(_p[0]), int(_p[1]))
        if labelVal == 0:
          patchList_out.append([_p[0], _p[1]])
        else:
          patchList_on.append([_p[0], _p[1]])
    countList.append([stiFileFullName, len(fixFileList), len(patchList), len(patchList_on), len(patchList_out)])
  return countList


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

def generate_discrete_groundTruthFixationMap(_gt):
  _dgtfmPath = "./static/__cache__/discrete_ground_truth_fixation_map.png"
  gtCopy = _gt.copy()
  for i in range(0, len(gtCopy)):
    for j in range(0, len(gtCopy[i])):
      replaceArr = np.array([255, 255, 255])
      if np.array_equal(gtCopy[i][j], np.array([0, 0, 0])):
        replaceArr = np.array([0, 0, 0])
      gtCopy[i][j] = replaceArr
  cv2.imwrite(_dgtfmPath, gtCopy)

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
  colCount = 3
  for featureName in featureList:
    colCount = colCount+1
    colFeatDF = df[featureName]
    scaler = MinMaxScaler()
    _tf = scaler.fit_transform(colFeatDF.values.reshape(-1, 1))
    tfDF.insert(colCount, featureName, _tf, True)
    # tfDF[featureName] = _tf
  return tfDF

def dt_zScore(df, featureList):
  getColNames = df.columns
  tfDF = df[[getColNames[0], getColNames[1], getColNames[2], getColNames[3]]]
  colCount = 3
  for featureName in featureList:
    colCount = colCount+1
    colFeatDF = df[featureName]
    scaler = StandardScaler()
    _tf = scaler.fit_transform(colFeatDF.values.reshape(-1, 1))
    tfDF.insert(colCount, featureName, _tf, True)
    # tfDF[featureName] = _tf
  return tfDF

def dt_yeoJohnson(df, featureList):
  getColNames = df.columns
  tfDF = df[[getColNames[0], getColNames[1], getColNames[2], getColNames[3]]]
  colCount = 3
  for featureName in featureList:
    colCount = colCount+1
    colFeatDF = df[featureName]
    scaler = PowerTransformer(method='yeo-johnson')
    _tf = scaler.fit_transform(colFeatDF.values.reshape(-1, 1))
    tfDF.insert(colCount, featureName, _tf, True)
    # tfDF[featureName] = _tf
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

def dimensionReduction(drMethod, df, featureList):
  print("Dimension reduction method: "+drMethod)
  if drMethod == "MDS":
    return dr_MDS(df, featureList)
  elif drMethod == "PCA":
    return dr_PCA(df, featureList)
  elif drMethod == "ICA":
    return dr_ICA(df, featureList)
  elif drMethod == "t_SNE":
    return dr_TSNE(df, featureList)
  elif drMethod == "PLS":
    return dr_PLS(df, featureList)
  else:
    print("ERROR: unavailable dimension reduction method selected")
    return df[['x', 'y']]

def dr_MDS(df, featureList):
  drm = MDS(n_components=2, random_state=0)
  drDF = drm.fit_transform(df[featureList])
  return drDF

def dr_PCA(df, featureList):
  drm = PCA(n_components=2, random_state=0)
  drDF = drm.fit_transform(df[featureList])
  return drDF

def dr_ICA(df, featureList):
  drm = FastICA(n_components=2, random_state=0)
  drDF = drm.fit_transform(df[featureList])
  return drDF

def dr_TSNE(df, featureList):
  drm = TSNE(learning_rate=100, random_state=0)
  drDF = drm.fit_transform(df[featureList])
  return drDF

def dr_PLS(df, featureList):
  drm = PLSRegression(n_components=2)
  drDF, _ = drm.fit_transform(df[featureList], df["label"])
  return drDF

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

@app.route('/api/multiPatchVisualization/selectDivUpdate', methods=['POST'])
def multiPatchVisualization_selectDivUpdate():
  print("multiPatchVisualization_selectDivUpdate")
  print(request.form)
  response = {}
  try:
    SELECTED_DIV_CACHE_PATH = request.form['cachePath']
    splitPath = SELECTED_DIV_CACHE_PATH.split("-")
    get_dataset = splitPath[0].split("/cache_")[1]
    get_semantic = splitPath[1]
    get_stimulus = splitPath[2]
    get_data_transformation = splitPath[3]
    get_dimension_reduction = splitPath[4]

    slectedDivData = [get_dataset, get_semantic, get_stimulus, get_data_transformation, get_dimension_reduction]
    makeJSON("./static/__cache__/select_div.json", slectedDivData)

    response['status'] = 'success'
  except Exception as e:
    response['status'] = 'failed'
    response['reason'] = e
    print(e)
  return json.dumps(response)

@app.route('/api/clustering/processingMulti', methods=['POST'])
def clustering_processingMulti():
  print("clustering_processingMulti")
  print(request.form)
  response = {}
  try:
    GET_TRANSFORMATION_METHOD_STR = request.form['transformationMethod']
    GET_DIMEN_REDUCTION_METHOD_STR = request.form['dimensionReductionMethod']
    GET_SELECTED_STIMULUS_INFO_STR = request.form['selectedStimulus']

    GET_SELECTED_STIMULUS_INFO = GET_SELECTED_STIMULUS_INFO_STR.split("-")
    GET_TRANSFORMATION_METHOD = GET_TRANSFORMATION_METHOD_STR.split("/")
    GET_DIMEN_REDUCTION_METHOD = GET_DIMEN_REDUCTION_METHOD_STR.split("/")
    print(GET_TRANSFORMATION_METHOD)
    print(GET_DIMEN_REDUCTION_METHOD)
    print(PARTICIPANT)
    print(GET_SELECTED_STIMULUS_INFO)

    datasetName = GET_SELECTED_STIMULUS_INFO[0].split("/")[0]
    semanticClassName = GET_SELECTED_STIMULUS_INFO[0].split("/")[1]
    stimulusFileName = GET_SELECTED_STIMULUS_INFO[0].split("/")[2]
    stimulusName = stimulusFileName.split(".")[0]
    stimulusExe = stimulusFileName.split(".")[1]
    stimulusDirName = stimulusName +"_"+ stimulusExe

    groundTruthPath = "./static/ground_truth/" + datasetName +"/"+ semanticClassName +"/"+ stimulusName +".jpg"
    groundTruthFixMap = cv2.imread(groundTruthPath)
    generate_discrete_groundTruthFixationMap(groundTruthFixMap)
    fmHeight, fmWidth = groundTruthFixMap.shape[:2]

    cacheFilePathList = []
    pExistsFlag = True
    for dtm in GET_TRANSFORMATION_METHOD:
      for drm in GET_DIMEN_REDUCTION_METHOD:
        cacheFilePath = "./static/__cache__/pcache/cache_"+ datasetName +"-"+ semanticClassName +"-"+ stimulusDirName +"-"+ dtm +"-"+ drm +"-"+ str(len(PARTICIPANT)) +".csv"
        existsFlag = True
        if not(os.path.exists(cacheFilePath)):
          existsFlag = False
          pExistsFlag = False
        cacheFilePathList.append([cacheFilePath, existsFlag])
    
    patchProcessDataLists = []
    if pExistsFlag == True:
      print("All cache file exists")
      for cPath in cacheFilePathList:
        p = cPath[0]
        aggDF = pd.read_csv(p)
        patchProcessDataLists.append(aggDF.values.tolist())
    else:
      print("Some cache files do not exists")
      for cPath in cacheFilePathList:
        p = cPath[0]
        eFlag = cPath[1]
        if eFlag == True:
          aggDF = pd.read_csv(p)
          patchProcessDataLists.append(aggDF.values.tolist())
        else:
          fixDirPath = "./static/fix/" + datasetName +"/"+ semanticClassName +"/"+ stimulusDirName +"/"
          featureDirPath = "./static/feature/"
          featureDFList = []
          for _f in FEATURE_ordered:
            featureFilePath = featureDirPath + _f +"/"+ datasetName +"/"+ semanticClassName +"/"+ stimulusName +".csv"
            featureDF = pd.read_csv(featureFilePath)
            featureDFList.append(featureDF)
          PARTICIPANT_LIST = []
          
          for obInfo in PARTICIPANT:
            _dataName = obInfo.split("/")[0]
            _className = obInfo.split("/")[1]
            _stiNameDir = obInfo.split("/")[2]
            if datasetName == _dataName and semanticClassName == _className and stimulusDirName == _stiNameDir:
              PARTICIPANT_LIST.append(obInfo)
          
          aggregatedDataList = []
          for observer in PARTICIPANT_LIST:
            userId = observer.split("/")[3]
            fixFilePath = fixDirPath + datasetName +"/"+ semanticClassName +"/"+ stimulusDirName +"/"+ userId+".csv"
            ob = datasetName +"/"+ semanticClassName +"/"+ stimulusDirName +"/"+ userId
            fixDF = pd.read_csv(fixFilePath, header=None)
            fixList = fixDF.values.tolist()
            for _fp in fixList:
              _x = int(_fp[0])
              _y = int(_fp[1])
              _label = label_groundTruthFixationMap(groundTruthFixMap, _x, _y)
              _midStack = [ob, _x, _y, _label]
              for i in range(0, len(FEATURE_ordered)):
                fMean = getFeatureMeanVal(featureDFList[i], _x, _y, fmWidth, fmHeight, PATCH_SIZE)
                _midStack.append(fMean)
              aggregatedDataList.append(_midStack)
          dfCols = ["id", "x", "y", "label"]
          for featName in FEATURE_ordered:
            dfCols.append(featName)
          aggDF = pd.DataFrame(aggregatedDataList, columns=dfCols)


          # data transformation
          dtm = p.split("-")[3]
          drm = p.split("-")[4]
          tfDF = dataTransformation(dtm, aggDF, FEATURE_ordered)
          # dimension reduction
          dr = dimensionReduction(drm, tfDF, FEATURE_ordered)
          drDF = pd.DataFrame(dr, columns=['x', 'y'])
          
          indexCount = 0
          processedDF = pd.DataFrame(aggDF['id'].values.tolist(), columns=['id'])
          indexCount = indexCount+1
          processedDF.insert(indexCount, "x", drDF['x'].values.tolist(), True)
          indexCount = indexCount+1
          processedDF.insert(indexCount, "y", drDF['y'].values.tolist(), True)
          indexCount = indexCount+1
          processedDF.insert(indexCount, "label", aggDF['label'].values.tolist(), True)
          indexCount = indexCount+1
          for featName in FEATURE_ordered:
            processedDF.insert(indexCount, featName, tfDF[featName].values.tolist(), True)
            indexCount = indexCount+1

          processedDF.to_csv(p, mode='w', index=False, header=True)
          processedDataList = processedDF.values.tolist()
          patchProcessDataLists.append(processedDataList)
          if os.path.exists(p):
            cPath[1] = True

    response['status'] = 'success'
    response['processingData'] = patchProcessDataLists
    response['cacheFilePath'] = cacheFilePathList
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
    GET_USE_CACHE_FLAG = request.form['cacheUseFlag']
    GET_TRANSFORMATION_METHOD = request.form['transformationMethod']
    GET_DIMEN_REDUCTION_METHOD = request.form['dimensionReductionMethod']
    GET_SELECTED_STIMULUS_INFO_STR = request.form['selectedStimulus']
    GET_SELECTED_STIMULUS_INFO = GET_SELECTED_STIMULUS_INFO_STR.split("-")
    print(GET_USE_CACHE_FLAG)
    print(GET_TRANSFORMATION_METHOD)
    print(GET_DIMEN_REDUCTION_METHOD)
    print(PARTICIPANT)
    print(GET_SELECTED_STIMULUS_INFO)
    
    cacheFilePath = ""
    fixDirPath = "./static/fix/"
    featureDirPath = "./static/feature/"
    groundTruthDirPath = "./static/ground_truth/"
    aggregatedDataList = []

    if GET_USE_CACHE_FLAG == "use":
      print("Use cache flag on: "+cacheFilePath)
      stiInfo = GET_SELECTED_STIMULUS_INFO[0]
      
      dataName = stiInfo.split("/")[0]
      className = stiInfo.split("/")[1]
      stiFileName = stiInfo.split("/")[2]
      stiName = stiFileName.split(".")[0]
      stiExe = stiFileName.split(".")[1]
      stiNameDir = stiName +"_"+ stiExe
      cacheFilePath = "./static/__cache__/pcache/cache_"+ dataName +"-"+ className +"-"+ stiNameDir +"-"+ GET_TRANSFORMATION_METHOD +"-"+ GET_DIMEN_REDUCTION_METHOD +"-"+ str(len(PARTICIPANT)) +".csv"
    else:
      for stiInfo in GET_SELECTED_STIMULUS_INFO:
        dataName = stiInfo.split("/")[0]
        className = stiInfo.split("/")[1]
        stiFileName = stiInfo.split("/")[2]
        stiName = stiFileName.split(".")[0]
        stiExe = stiFileName.split(".")[1]
        stiNameDir = stiName +"_"+ stiExe
        
        cacheFilePath = "./static/__cache__/pcache/cache_"+ dataName +"-"+ className +"-"+ stiNameDir +"-"+ GET_TRANSFORMATION_METHOD +"-"+ GET_DIMEN_REDUCTION_METHOD +"-"+ str(len(PARTICIPANT)) +".csv"
        
        gtFixMapPath = groundTruthDirPath + dataName +"/"+ className +"/"+ stiName +".jpg"
        groundTruthFixMap = cv2.imread(gtFixMapPath)
        generate_discrete_groundTruthFixationMap(groundTruthFixMap)
        fmHeight, fmWidth = groundTruthFixMap.shape[:2]
        featureDFList = []
        for _f in FEATURE_ordered:
          featureFilePath = featureDirPath + _f +"/"+ dataName +"/"+ className +"/"+ stiName +".csv"
          featureDF = pd.read_csv(featureFilePath)
          featureDFList.append(featureDF)

        PARTICIPANT_LIST = []
        for obInfo in PARTICIPANT:
          _dataName = obInfo.split("/")[0]
          _className = obInfo.split("/")[1]
          _stiNameDir = obInfo.split("/")[2]
          if dataName == _dataName and className == _className and stiNameDir == _stiNameDir:
            PARTICIPANT_LIST.append(obInfo)

        for observer in PARTICIPANT_LIST:
          # stiExt = stiNameDir.split("_")[1]
          userId = observer.split("/")[3]
          fixFilePath = fixDirPath + dataName +"/"+ className +"/"+ stiNameDir +"/"+ userId+".csv"
          ob = dataName +"/"+ className +"/"+ stiNameDir +"/"+ userId
          fixDF = pd.read_csv(fixFilePath, header=None)
          fixList = fixDF.values.tolist()
          # print(fixFilePath)
          for _fp in fixList:
            _x = int(_fp[0])
            _y = int(_fp[1])
            _label = label_groundTruthFixationMap(groundTruthFixMap, _x, _y)
            _midStack = [ob, _x, _y, _label]
            for i in range(0, len(FEATURE_ordered)):
              fMean = getFeatureMeanVal(featureDFList[i], _x, _y, fmWidth, fmHeight, PATCH_SIZE)
              _midStack.append(fMean)
            aggregatedDataList.append(_midStack)
    
    aggDF = []
    if GET_USE_CACHE_FLAG == "use":
      aggDF = pd.read_csv(cacheFilePath)
    else:
      dfCols = ["id", "x", "y", "label"]
      for featName in FEATURE_ordered:
        dfCols.append(featName)
      aggDF = pd.DataFrame(aggregatedDataList, columns=dfCols)
    

    # data transformation
    tfDF = dataTransformation(GET_TRANSFORMATION_METHOD, aggDF, FEATURE_ordered)
    # dimension reduction
    dr = dimensionReduction(GET_DIMEN_REDUCTION_METHOD, tfDF, FEATURE_ordered)
    drDF = pd.DataFrame(dr, columns=['x', 'y'])
    
    indexCount = 0
    processedDF = pd.DataFrame(aggDF['id'].values.tolist(), columns=['id'])
    indexCount = indexCount+1
    processedDF.insert(indexCount, "x", drDF['x'].values.tolist(), True)
    indexCount = indexCount+1
    processedDF.insert(indexCount, "y", drDF['y'].values.tolist(), True)
    indexCount = indexCount+1
    processedDF.insert(indexCount, "label", aggDF['label'].values.tolist(), True)
    indexCount = indexCount+1
    for featName in FEATURE_ordered:
      processedDF.insert(indexCount, featName, tfDF[featName].values.tolist(), True)
      indexCount = indexCount+1

    dataColumns = processedDF.columns.values.tolist()
    processedDataList = processedDF.values.tolist()
    rawDataList = aggDF.values.tolist()
    processedDF.to_csv(cacheFilePath, mode='w', index=False, header=True)

    response['status'] = 'success'
    response['dataColumns'] = dataColumns
    response['processingData'] = processedDataList
    response['cacheFilePath'] = cacheFilePath.split(".")[1]+".csv"
    response['rawData'] = rawDataList
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
      fixDF = pd.read_csv(filePath, header=None)
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
      df = pd.read_csv(_path, header=None)
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

#################
# overview APIs #
#################
@app.route('/api/overview', methods=['POST'])
def overview_calc():
  print("overview_calc")
  print(request.form)
  response = {}
  try:
    GET_SELECTED_DATAINFO = request.form['semanticClass']
    GET_DATASET = GET_SELECTED_DATAINFO.split("/")[0]
    GET_SEMANTIC_CLASS = GET_SELECTED_DATAINFO.split("/")[1]
    
    stimulusPath = "./static/stimulus/"+ GET_DATASET +"/"+ GET_SEMANTIC_CLASS +"/"
    stimulusList = os.listdir(stimulusPath)
    
    OVERVIEW_COUNT_LIST = []
    OVERVIEW_COUNT_LIST = overview_count(stimulusList, GET_DATASET, GET_SEMANTIC_CLASS)
    
    response['status'] = 'success'
    response['overview'] = OVERVIEW_COUNT_LIST
  except Exception as e:
    response['status'] = 'failed'
    response['reason'] = e
    print(e)

  return json.dumps(response)