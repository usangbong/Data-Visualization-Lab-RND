import pandas as pd
from flask import Flask, render_template, request
import sys
import os
from static.libs.record import *
from static.libs.drawChart import Chart
sys.path.append("module/")
application = Flask(__name__)

global cnt, name
global state #visualization number  100:eval, 0: rest, etc: vis
global userAnswer, taskList, dataList

cnt = 0
state = 0
userAnswer=[]
dataList=os.listdir('static/data/')
taskList=pd.read_csv('static/task.txt', sep=',')
totalScore=[['Mental','Physical','Temporal','Effort','Performance','Frustration']]


@application.route('/')
def index():
    return render_template('index.html')

@application.route('/search')
def searchResult():
    global name, state
    name = request.args.get("search")

    # eeg record start
    startRecording(name)

    #add marker in eeg record
    injectMarker(state)

    return render_template('firstRest.html')

@application.route('/visualization')
def getVis():
    global cnt, state, dataList, taskList
    cnt += 1
    state = cnt
    src='static/data/'+dataList[cnt-1]
    Chart(src)
    #add marker in eeg record
    injectMarker(state)
    return render_template('visualization.html', task=taskList.iloc[cnt-1])

@application.route('/answer')
def getAnswer():
    global state, userAnswer
    state = 100
    #add marker in eeg record
    injectMarker(state)
    ans = request.args.get("answer")
    userAnswer.append(ans)
    print(ans)
    return render_template('NASA-TLX.html')

@application.route('/NASA-TLX')
def getNASA():
    global state
    state = 100
    #add marker in eeg record
    injectMarker(state)
    return render_template('NASA-TLX.html')

@application.route('/eval')
def eval():
    global cnt, name, userAnswer, state
    print(cnt)
    score=[]
    score.append(request.args.get("Mental"))
    score.append(request.args.get("Physical"))
    score.append(request.args.get("Temporal"))
    score.append(request.args.get("Effort"))
    score.append(request.args.get("Performance"))
    score.append(request.args.get("Frustration"))

    totalScore.append(score)
    if cnt >= 1:
        userData = pd.DataFrame(totalScore)
        userData.columns=userData.iloc[0]
        userData = userData.drop(userData.index[0])
        userData.to_csv('C:/EEG data/User/'+name+'.csv')

        userAnswer=pd.DataFrame(userAnswer)
        userAnswer.columns =['answer']
        userAnswer.to_csv('C:/EEG data/UserAnswer/'+name+'Answer.txt')

        # save emotiv data
        stopRecording()
        return render_template('end.html')
    else:
        state=0
        injectMarker(state)
        return render_template('rest.html')

@application.route('/rest')
def getRest():
    global state
    state = 0
    #add marker in eeg record
    injectMarker(state)
    return render_template('rest.html')


if __name__ == "__main__":
    application.run(debug=True)
