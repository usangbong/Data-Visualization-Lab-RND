import pandas as pd
from flask import Flask, render_template, request
import sys
import os
#from static.libs.record import *

sys.path.append("module/")
application = Flask(__name__)

global cnt, name
global userAnswer, taskList, dataList, vis_name

cnt = 0
userAnswer=[]
dataList=os.listdir('static/data/')
taskList=pd.read_csv('static/task.txt')
vis_name = pd.read_csv('static/vis_name.txt', encoding='utf-8')
totalScore=[['Mental','Physical','Temporal','Effort','Performance','Frustration']]


@application.route('/')
def index():
    return render_template('index.html')

@application.route('/search')
def searchResult():
    global name
    name = request.args.get("search")

    # eeg record start
    #startRecording(name)

    #add marker in eeg record
    #injectMarker(0) #100:eval, 0: rest, cnt: vis number

    return render_template('firstRest.html')

@application.route('/visualization')
def getVis():
    global cnt, dataList, taskList, vis_name
    cnt += 1
    src='static/chart/'+vis_name['vis_name'][cnt-1]+'.png'
    #add marker in eeg record
    #injectMarker(cnt)
    return render_template('visualization.html', image=src, task=taskList[taskList.columns[0]][cnt-1])

@application.route('/answer')
def getAnswer():
    global userAnswer
    #add marker in eeg record
    #injectMarker(100)
    ans = request.args.get("answer")
    userAnswer.append(ans)
    print(ans)
    return render_template('NASA-TLX.html')

@application.route('/NASA-TLX')
def getNASA():
    #add marker in eeg record
    #injectMarker(100)
    return render_template('NASA-TLX.html')

@application.route('/eval')
def eval():
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
    if cnt >= 1:
        userData = pd.DataFrame(totalScore)
        userData.columns=userData.iloc[0]
        userData = userData.drop(userData.index[0])
        userData.to_csv('C:/EEG data/User/'+name+'.csv')

        userAnswer=pd.DataFrame(userAnswer)
        userAnswer.columns =['answer']
        userAnswer.to_csv('C:/EEG data/UserAnswer/'+name+'Answer.txt')

        # save emotiv data
        #stopRecording()
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
