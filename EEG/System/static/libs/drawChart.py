import os
import random
from collections import Counter

import pandas as pd
import plotly as py
from plotly.graph_objs import Scatter, Bar
from plotly.express import scatter
import matplotlib.pyplot as plt
# 한글 폰트 사용을 위해서 세팅
from matplotlib import font_manager, rc
font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

def Chart(src, cnt, task):
    df = pd.read_csv(src, thousands=',', encoding='utf-8')
    col = df.columns
    print(col[1],col[2],col[3])
    py.offline.plot({
        'data':[Scatter(x=df[col[1]],y=df[col[2]], line=None)], #, name=df[col[1]],
        'layout': {"title": {"text": task, 'y': 0.9, 'x': 0.5,
                             'xanchor': 'center', 'yanchor': 'top'},
                   "xaxis": {"title": {"text": col[1]}},
                   "yaxis": {"title": {"text": col[2]}}}
    },
        filename ='templates/Chart.html', auto_open = False)

def updateChart():
    df = pd.read_csv('static/data/KOSPI.csv', thousands=',', encoding='euc-kr')
    print(df.columns)
    py.offline.plot({
        'data':[Scatter(x=df['date'],y=df['actual'], name='actual'),
                Scatter(x=df['date'],y=df['prediction'],name='prediction')]
    },filename='templates/Chart.html',auto_open = False)

dataList = os.listdir('../data/')
task = pd.read_csv('../task.txt')
vis_name = pd.read_csv('../vis_name.txt', encoding='utf-8')

data = pd.read_csv('../data/'+dataList[0])
x = data[vis_name['x'][0]]
y = data[vis_name['y'][0]]
color = data[vis_name['color'][0]]
fig = plt.figure()

weights = [i for i in Counter(color).values() for j in range(i)]

plt.scatter(x,y, c=color,
           alpha=0.3, s=weights, edgecolors='gray')
plt.colorbar(label=vis_name['color_col'][0])
plt.xlabel(vis_name['x_col'][0])
plt.ylabel(vis_name['y_col'][0])



x_range, y_range = plt.xlim(), plt.ylim()
x_range_num = [0,1]
random.shuffle(x_range_num)
y_range_num = [0,1]
random.shuffle(y_range_num)

plt.xlim([x_range[x_range_num[0]], x_range[x_range_num[1]]])      # X축의 범위: [xmin, xmax]
plt.ylim([y_range[y_range_num[0]], y_range[y_range_num[1]]])     # Y축의 범위: [ymin, ymax]

fig.savefig('../chart/'+vis_name['vis_name'][0]+'.png')
plt.show()