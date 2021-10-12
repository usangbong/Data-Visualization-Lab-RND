import pandas as pd
import plotly as py
from plotly.graph_objs import Scatter, Bar
from plotly.express import scatter

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
