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

clusters = [df.values[labels == i] for i in range(n_clusters_)]


fig = plt.figure(figsize=(20, 20))
fig_sub = []
fig_sub_count=0

for i in range(1,len(clusters)+1):
    fig_sub.append(fig.add_subplot(9,7,i))
    fig_sub[i-1].title.set_text(i-1)
    fig_sub[i-1].set_xlim([0, 1920])
    fig_sub[i-1].set_ylim([1080, 0])
    fig_sub[i-1].imshow(img, extent=[0, 1920, 1080, 0])
    
savecsv=[]
counts=[]
for i in range(1,len(clusters)+1):
    fig_sub_count+=1
    tmpres=[]
    count=0
    for j in clusters[i-1]:
        fig_sub[fig_sub_count-1].scatter(j[1], j[2], c='b', marker='o')
        tmpres.append(str(int(j[0]/other))+"/"+str(int(j[1]))+"/"+str(int(j[2])))
        count+=1
    tmpres="/".join(tmpres)
    savecsv.append(tmpres)
    counts.append(count)
print(savecsv)
#########################################################################
#########################################################################

range(1,len(clusters)+1)

#########################################################################
#########################################################################
maxd = max(counts)
print(maxd)
for i in range(len(counts)):
    counts[i]=counts[i]/maxd
d = {'data': savecsv, 'counts': counts}
csv_df = pd.DataFrame(d)
print(csv_df)
csv_df.to_csv("data/clusted_"+dataname,header=False,index=False)
#########################################################################
#########################################################################
import math

fig = plt.figure(figsize=(20, 20))
ax=[]
for i in range(1,n_clusters_+1):    
    ax.append(fig.add_subplot(8,4,i))
    
for q in range(1,n_clusters_+1):    
    ax[q-1].set_ylim([54, 0])
    x=clusters[q-1][:,1]/20
    y=clusters[q-1][:,2]/20

    grid_size=1
    h=10

    x_grid=np.arange(0,96)
    y_grid=np.arange(0,54)
    x_mesh,y_mesh=np.meshgrid(x_grid,y_grid)

    xc=x_mesh+(grid_size/2)
    yc=y_mesh+(grid_size/2)

    def kde_quartic(d,h):
        dn=d/h
        P=(15/16)*(1-dn**2)**2
        return P
    
    #PROCESSING
    intensity_list=[]
    for j in range(len(xc)):
        intensity_row=[]
        for k in range(len(xc[0])):
            kde_value_list=[]
            for i in range(len(x)):
                #CALCULATE DISTANCE
                d=math.sqrt((xc[j][k]-x[i])**2+(yc[j][k]-y[i])**2) 
                if d<=h:
                    p=kde_quartic(d,h)
                else:
                    p=0
                kde_value_list.append(p)
            p_total=sum(kde_value_list)
            intensity_row.append(p_total)
        intensity_list.append(intensity_row)

    intensity=np.array(intensity_list)
    
    ax[q-1].pcolormesh(x_mesh,y_mesh,intensity)
