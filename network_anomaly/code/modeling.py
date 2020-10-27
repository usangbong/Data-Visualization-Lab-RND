# -*- coding: utf-8 -*-
# import relevant modules
# %matplotlib inline
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import sklearn
#import imblearn

# cross validation
from sklearn.model_selection import StratifiedKFold  # Stratified K-fold cross validation 테스트
skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=0)

# Ignore warnings
import warnings
warnings.filterwarnings('ignore')

# Time Calculation (나중에 알고리즘 학습/테스트 시간 계산하려고 코드 넣어놓음)
#import time
#train_start = time.clock()
#train_end = time.clock()
#test_start = time.clock()
#test_end = time.clock()
#print ('Training time : %fs' %(train_end - train_start))
#print ('Test Results time : %fs' %(test_end - test_start))


# Settings
# pd.set_option('display.max_columns', None)
# np.set_printoptions(threshold=np.nan)
# np.set_printoptions(precision=3)
# sns.set(style="darkgrid")
# plt.rcParams['axes.labelsize'] = 14
# plt.rcParams['xtick.labelsize'] = 12
# plt.rcParams['ytick.labelsize'] = 12

train = pd.read_csv("./input/Train_data.csv")
test = pd.read_csv("./input/Test_data.csv")

print(train.head(4))

print("Training data has {} rows & {} columns".format(train.shape[0],train.shape[1]))

print(test.head(4))

print("Testing data has {} rows & {} columns".format(test.shape[0],test.shape[1]))

# Descriptive statistics
train.describe()

print(train['num_outbound_cmds'].value_counts())
print(test['num_outbound_cmds'].value_counts())

#'num_outbound_cmds' is a redundant column so remove it from both train & test datasets
train.drop(['num_outbound_cmds'], axis=1, inplace=True)
test.drop(['num_outbound_cmds'], axis=1, inplace=True)

# Attack Class Distribution
train['class'].value_counts()

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()

# extract numerical attributes and scale it to have zero mean and unit variance
cols = train.select_dtypes(include=['float64','int64']).columns
sc_train = scaler.fit_transform(train.select_dtypes(include=['float64','int64']))
sc_test = scaler.fit_transform(test.select_dtypes(include=['float64','int64']))

# turn the result back to a dataframe
sc_traindf = pd.DataFrame(sc_train, columns = cols)
sc_testdf = pd.DataFrame(sc_test, columns = cols)


from sklearn.preprocessing import LabelEncoder
encoder = LabelEncoder()

# extract categorical attributes from both training and test sets
cattrain = train.select_dtypes(include=['object']).copy()
cattest = test.select_dtypes(include=['object']).copy()

# encode the categorical attributes
traincat = cattrain.apply(encoder.fit_transform)
testcat = cattest.apply(encoder.fit_transform)

print(cattrain)

# separate target column from encoded data
enctrain = traincat.drop(['class'], axis=1)
cat_Ytrain = traincat[['class']].copy()

train_x = pd.concat([sc_traindf,enctrain],axis=1)
train_y = train['class']
train_x.shape

test_df = pd.concat([sc_testdf,testcat],axis=1)
test_df.shape

from sklearn.ensemble import RandomForestClassifier
rfc = RandomForestClassifier()

# fit random forest classifier on the training set
rfc.fit(train_x, train_y)
# extract important features
score = np.round(rfc.feature_importances_,3)
importances = pd.DataFrame({'feature':train_x.columns,'importance':score})
importances = importances.sort_values('importance',ascending=False).set_index('feature')
# plot importances
plt.rcParams['figure.figsize'] = (11, 4)
importances.plot.bar();

print(importances)

from sklearn.feature_selection import RFE
import itertools
rfc = RandomForestClassifier()

# create the RFE model and select 10 attributes
rfe = RFE(rfc, n_features_to_select=15)
rfe = rfe.fit(train_x, train_y)

# summarize the selection of the attributes
feature_map = [(i, v) for i, v in itertools.zip_longest(rfe.get_support(), train_x.columns)]
selected_features = [v for i, v in feature_map if i==True]

selected_features

from sklearn.model_selection import train_test_split

X_train,X_test,Y_train,Y_test = train_test_split(train_x,train_y,train_size=0.70, random_state=2)

from sklearn import metrics
from sklearn.svm import SVC
from sklearn.naive_bayes import BernoulliNB
from sklearn import tree
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
import sklearn.ensemble as ske
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
import xgboost as xgb
from lightgbm import LGBMClassifier

# Train KNeighborsClassifier Model
KNN_Classifier = KNeighborsClassifier(n_jobs=-1)
KNN_Classifier.fit(X_train, Y_train);

# Train LogisticRegression Model
LGR_Classifier = LogisticRegression(n_jobs=-1, random_state=0)
LGR_Classifier.fit(X_train, Y_train);

# Train Gaussian Naive Baye Model
BNB_Classifier = BernoulliNB()
BNB_Classifier.fit(X_train, Y_train)

# Train Decision Tree Model
DTC_Classifier = tree.DecisionTreeClassifier(criterion='entropy', random_state=0)
DTC_Classifier.fit(X_train, Y_train)

# Random Forest Model
RD_Classifier = ske.RandomForestClassifier(n_estimators=100)
RD_Classifier.fit(X_train, Y_train)

# GradientBoosting
GB_Classifier = ske.GradientBoostingClassifier(n_estimators=50)
GB_Classifier.fit(X_train, Y_train)

# AdaBoost
AD_Classifier = ske.AdaBoostClassifier(n_estimators=100)
AD_Classifier.fit(X_train, Y_train)

# GaussianNB
GS_Classifier = GaussianNB()
GS_Classifier.fit(X_train, Y_train)

# XGBoost
XGB_Classifier = xgb.XGBClassifier()
XGB_Classifier.fit(X_train, Y_train)

# LightGBM
lgbm_Classifier = LGBMClassifier()
lgbm_Classifier.fit(X_train, Y_train)

models = []
models.append(('Naive Baye Classifier', BNB_Classifier))
models.append(('Decision Tree Classifier', DTC_Classifier))
models.append(('KNeighborsClassifier', KNN_Classifier))
models.append(('LogisticRegression', LGR_Classifier))
models.append(('RandomForest',RD_Classifier))
models.append(('GradientBoosting',GB_Classifier))
models.append(('AdaBoost',AD_Classifier))
models.append(('GaussianNB',GS_Classifier))
models.append(('XGBoost',XGB_Classifier))
models.append(('LightGBM',lgbm_Classifier))

for i, v in models:
   #scores = cross_val_score(v, X_train, Y_train, cv=10) # 단순 교차검증
   scores = cross_val_score(v, X_train, Y_train, cv=skf) # ==> K분할 교차검증 (Stratified K-fold cross validation)
   accuracy = metrics.accuracy_score(Y_train, v.predict(X_train))
   confusion_matrix = metrics.confusion_matrix(Y_train, v.predict(X_train))
   classification = metrics.classification_report(Y_train, v.predict(X_train))
   print()
   print('============================== {} Model Evaluation =============================='.format(i))
   print()
   print ("Cross Validation Mean Score:" "\n", scores.mean())  # 교차검증결과
   print()
   print ("Model Accuracy:" "\n", accuracy) # train 정확도
   print()
   print("Confusion matrix:" "\n", confusion_matrix) # TP(True Positive), FN, FP, TN
   print()
   print("Classification report:", classification)
   print()

result = {}

for i, v in models:
       accuracy = metrics.accuracy_score(Y_test, v.predict(X_test))
       confusion_matrix = metrics.confusion_matrix(Y_test, v.predict(X_test))
       classification = metrics.classification_report(Y_test, v.predict(X_test))
       f1score = sklearn.metrics.f1_score(Y_test, v.predict(X_test),pos_label=None, average='weighted')
       print()
       print('============================== {} Model Test Results =============================='.format(i))
       print()
       print("Model Accuracy:" "\n", accuracy)  # test 정확도
       print()
       print("Confusion matrix:" "\n", confusion_matrix)  # TP(True Positive), FN, FP, TN
       print()
       print("Classification report:" "\n", classification)
       print()
       print("f1_score:", f1score)
       print()
       result[i] = f1score

winner = max(result,key=result.get)
print("Winner algorithm is %s : %f %% success" % (winner,result[winner]*100))



