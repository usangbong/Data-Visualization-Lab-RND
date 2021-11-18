import random
import pandas as pd
from flask import Flask, render_template, request
import sys
import os
import json
import plotly
import plotly.express as px
#from static.libs.record import *

sys.path.append("module/")
application = Flask(__name__)

global cnt, name
global userAnswer, chartList

cnt = 0
userAnswer=[]
chartList=os.listdir('static/chart/')
random.shuffle(chartList)
totalScore=[['Mental','Physical','Temporal','Effort','Performance','Frustration']]

@application.route('/')
def chart1():
    df = pd.DataFrame({
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Amount": [4, 1, 2, 2, 4, 5],
        "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
    })

    fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header="Fruit in North America"
    description = """
    A academic study of the number of apples, oranges and bananas in the cities of
    San Francisco and Montreal would probably not come up with this chart.
    """
    return render_template('plotlyChart.html', graphJSON=graphJSON, header=header,description=description)


@application.route('/search')
def searchResult():
    '''
    global name
    name = request.args.get("search")

    # eeg record start
    startRecording(name)

    #add marker in eeg record
    injectMarker(0) #100:eval, 0: rest, cnt: vis number
    '''
    return render_template('firstRest.html')

@application.route('/visualization')
def getVis():
    global cnt
    cnt += 1
    src='../static/chart/' + chartList[cnt-1]
    #add marker in eeg record
    #injectMarker(cnt)
    return render_template('visualization.html', image=src)

'''
@application.route('/visualization')
def getVis():
    global cnt
    cnt += 1
    src='../static/chart/' + chartList[cnt-1]
    #add marker in eeg record
    #injectMarker(cnt)
    return render_template('visualization.html', image=src)
'''

@application.route('/answer')
def getAnswer():
    '''
    global cnt, chartList, userAnswer
    #add marker in eeg record
    injectMarker(100)
    chartName = str(chartList[cnt-1]).replace('.png','')
    ans = request.args.get("answer")
    print(chartName)
    userAnswer.append([chartName, ans])
    print(ans)
    '''
    return render_template('NASA-TLX.html')

@application.route('/NASA-TLX')
def getNASA():
    #add marker in eeg record
    #injectMarker(100)
    return render_template('NASA-TLX.html')

@application.route('/eval')
def eval():
    '''
    global cnt, name, userAnswer
    print(cnt)
    score=[]
    score.append(request.args.get("Mental"))
    score.append(request.args.get("Physical"))
    score.append(request.args.get("Temporal"))
    score.append(request.args.get("Effort"))
    score.append(request.args.get("Performance"))
    score.append(request.args.get("Frustration"))

    totalScore.append(score)
    '''
    if cnt >= 1:
        '''
        userData = pd.DataFrame(totalScore)
        userData.columns=userData.iloc[0]
        userData = userData.drop(userData.index[0])
        userData.to_csv('C:/EEG data/User/'+name+'.csv')

        userAnswer=pd.DataFrame(userAnswer)
        userAnswer.columns =['chartName','answer']
        userAnswer.to_csv('C:/EEG data/UserAnswer/'+name+'Answer.txt')

        # save emotiv data
        stopRecording()
        '''
        return render_template('end.html')
    else:
        #injectMarker(0)
        return render_template('rest.html')

@application.route('/rest')
def getRest():
    #add marker in eeg record
    #injectMarker(0)
    return render_template('rest.html')


if __name__ == "__main__":
    application.run(debug=True)
