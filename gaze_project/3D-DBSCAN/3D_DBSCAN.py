#########################################################################
# DBSCAN 코드 레퍼런스 찾아서 표기해야 함
# This import registers the 3D projection, but is otherwise unused.

from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

dataname='tdata9.csv'
img = plt.imread("test.png")

df = pd.read_csv(dataname,sep=",", dtype={'x':float,'y':float,'timecount':float},header=None,names=["no","userid","timestamp","timecount","x","y"])

temp_tc =df['timecount']
#df['timecount']=df['timecount'].multiply(other = 30) 
df['timecount']=df['timecount']-df['timecount'][0]
df = df.drop(columns=['no', 'userid', 'timestamp'])

# Fixing random state for reproducibility
np.random.seed(19680801)

fig = plt.figure(figsize=(20, 20))
ax = fig.add_subplot(1,1,1, projection='3d')

# For each set of style and range settings, plot n random points in the box
# defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
current_t = -1
cmap = ['r','g','b','c','m','y','k']
asc = -1
count=0
for index, row in df.iterrows():
    if current_t!=row['timecount']:
        current_t=row['timecount']
        asc=(asc+1)%7
        count+=1
    ax.scatter(row['x'], row['y'], row['timecount'], c=cmap[asc], marker='o')

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
print(count)
#########################################################################
#########################################################################
X = np.random.normal(0, 1, 100)
Y = np.random.normal(0, 1, 100)

fig = plt.figure(figsize=(20, 20))

ycount = round(count/5)+1
sublist = []
subcount=0
print(count)
raw_data_time_cl = []

for i in range(1,count+1):
    sublist.append(fig.add_subplot(5,ycount,i))
    sublist[i-1].title.set_text(i-1)
    sublist[i-1].set_xlim([0, 1920])
    sublist[i-1].set_ylim([1080, 0])
    sublist[i-1].imshow(img, extent=[0, 1920, 1080, 0])
    
    
for index, row in df.iterrows():
    if current_t!=row['timecount']:
        current_t=row['timecount']
        asc=(asc+1)%7
        subcount+=1
        raw_data_time_cl.append([])
    raw_data_time_cl[subcount-1].append([row['x'], row['y']])
    sublist[subcount-1].scatter(row['x'], row['y'], c='r', marker='o')

#########################################################################
#########################################################################
import math
Cnt = 0
sumdist=0
dist_data = np.array([])
for i in raw_data_time_cl:
    dist=0
    if len(i)>1:    
        for j in range(0,len(i)-1):
            dist=math.sqrt(pow(i[j][0]-i[j+1][0],2)+pow(i[j][1]-i[j+1][1],2))
            sumdist+=dist/2
            dist_data = np.append(dist_data, dist)
            Cnt+=1
            
fig, axs = plt.subplots(1, 1, sharey=True, tight_layout=True)

axs.hist(dist_data, bins=100)

lebun=0.20
hibun=0.80

dist_data = np.sort(dist_data)
eps = dist_data[round(dist_data.size*hibun)]+1.5*(dist_data[round(dist_data.size*hibun)]-dist_data[round(dist_data.size*lebun)])
other = dist_data[round(dist_data.size*hibun)]           

print(dist_data.size)
print(eps)
print(other)
print(df.values)
#########################################################################
#########################################################################
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
data = np.random.rand(500,3)

db = DBSCAN(eps=eps, min_samples=1).fit(df.values)
labels = db.labels_

from collections import Counter
print(Counter(labels))

n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

print(n_clusters_)

clusters = [df.values[labels == i] for i in range(n_clusters_)]


fig = plt.figure(figsize=(20, 20))
fig_sub = []
fig_sub_count=0

for i in range(1,len(clusters)+1):
    fig_sub.append(fig.add_subplot(7,9,i))
    fig_sub[i-1].title.set_text(i-1)
    fig_sub[i-1].set_xlim([0, 1920])
    fig_sub[i-1].set_ylim([1080, 0])
    fig_sub[i-1].imshow(img, extent=[0, 1920, 1080, 0])
    
for i in range(1,len(clusters)+1):
    fig_sub_count+=1
    for j in clusters[i-1]:
        fig_sub[fig_sub_count-1].scatter(j[1], j[2], c='r', marker='o')
#########################################################################
#########################################################################
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
df['timecount']=df['timecount'].multiply(other = other) 

db = DBSCAN(eps=eps, min_samples=3).fit(df.values)
labels = db.labels_

from collections import Counter
print(Counter(labels))

n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

print(n_clusters_)

