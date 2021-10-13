import random
import pandas as pd
from flask import Flask, render_template, request
import sys
import os
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
    global cnt
    cnt += 1
    src='../static/chart/' + chartList[cnt-1]
    #add marker in eeg record
    #injectMarker(cnt)
    return render_template('visualization.html', image=src)

@application.route('/answer')
def getAnswer():
    global cnt, chartList, userAnswer
    #add marker in eeg record
    #injectMarker(100)
    chartName = str(chartList[cnt-1]).replace('.png','')
    ans = request.args.get("answer")
    print(chartName)
    userAnswer.append([chartName, ans])
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
    if cnt >= 21:
        userData = pd.DataFrame(totalScore)
        userData.columns=userData.iloc[0]
        userData = userData.drop(userData.index[0])
        userData.to_csv('C:/EEG data/User/'+name+'.csv')

        userAnswer=pd.DataFrame(userAnswer)
        userAnswer.columns =['chartName','answer']
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
