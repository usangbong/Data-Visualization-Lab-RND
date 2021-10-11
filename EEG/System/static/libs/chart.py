import pandas as pd
import plotly as py
from plotly.graph_objs import Scatter, Layout

import cufflinks as cf

def updateChart():
    df = pd.read_csv('static/data/KOSPI.csv', thousands=',', encoding='euc-kr')
    print(df.columns)
    py.offline.plot({
        'data':[Scatter(x=df['date'],y=df['actual'], name='actual'),
                Scatter(x=df['date'],y=df['prediction'],name='prediction')]
    },filename='Chart.html',auto_open = False)

