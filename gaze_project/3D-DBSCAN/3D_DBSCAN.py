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
