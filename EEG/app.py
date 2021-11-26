from flask import Flask, render_template, request
from itertools import product
import random
import os
import pandas as pd
import time
from static.libs.record import *

'''
Inject Marker
mark0: rest
mark1: eval
mark2: save
other: vis
'''

app = Flask(__name__)

global tasks
global taskCount
global userAnswer
global names

taskCount = -1
userAnswer = {}

def makeTask():
    df = pd.read_csv('static/data/task.csv', encoding='CP949')
    vis = ['bar', 'line', 'scatter', 'map']
    #task = ['Task1', 'Task2', 'Task3'] #A
    #task = ['Task1', 'Task2', 'Task4'] #B
    #task = ['Task1', 'Task3', 'Task4'] #C
    #task = ['Task2', 'Task3', 'Task4'] #D
    task = ['Task1', 'Task2', 'Task3', 'Task4'] #E
    design = ['shape', 'size', 'color']

    vis_marker = {'scatter':100, 'bar':200, 'line':300, 'map':400}
    task_marker = {'1':10, '2':20, '3':30, '4':40}
    design_marker = {'base':1, 'color':2, 'shape':3, 'size':4}

    items = [vis, task, design]
    result = list(product(*items))

    directoryList = []
    motherDirectory = 'templates/'
    defaultDirectory = 'vis/'
    for r in result:
        directory = motherDirectory + defaultDirectory + r[0] + '/' + r[1] + '/' + r[2] + '/'
        baseDirectory = motherDirectory + defaultDirectory + r[0] + '/' + r[1] + '/' + 'base/'

        files = os.listdir(directory)
        idx = random.randrange(0, 2)
        selectFile = files[idx] #current directory select
        baseFile = files[1-idx] #base directory select

        subdf = df[(df['vis']==r[0])&(df['taskNum']==int(r[1][-1]))&(df['type']==r[2])]
        basetask = subdf[subdf['filename'] == baseFile.replace('.html', '')]['task'].values.tolist()[0]
        selecttask = subdf[subdf['filename'] == selectFile.replace('.html', '')]['task'].values.tolist()[0]

        selectFileDirectory = directory.replace(motherDirectory, '') + selectFile
        baseFileDirectory = baseDirectory.replace(motherDirectory, '') + baseFile

        baseMarker = vis_marker[r[0]] + task_marker[r[1][-1]] + design_marker['base']
        selectMarker = vis_marker[r[0]] + task_marker[r[1][-1]] + design_marker[r[2]]

        directoryList.append((baseFileDirectory, basetask, baseMarker))
        directoryList.append((selectFileDirectory, selecttask, selectMarker))

    random.shuffle(directoryList)
    print(len(directoryList))
    return directoryList

global testcount
global testTasks
global saveCount
testcount = -1
testTasks = []
saveCount = -1

def makeTestTask():
    global testTasks

    test_df = pd.read_csv('static/data/test_task.csv', encoding='CP949')
    motherDirectory = 'templates/'
    testDirectory = 'test/'

    test_file_list = os.listdir(motherDirectory + testDirectory.replace('/', ''))
    for file in test_file_list:
        subdf = test_df[test_df['filename'] == file.replace('.html', '')]
        path = testDirectory + file
        task = subdf['task'].values.tolist()[0]
        sublist = (path, task)
        testTasks.append(sublist)

@app.route('/')
def hello_world():
    global tasks

    makeTestTask()
    directoryList = makeTask()
    tasks = directoryList

    return render_template('index.html')

@app.route('/test', methods=['POST'])
def test():
    global testTasks
    global testcount

    if request.method=='POST':
        print('test')
        testcount += 1

        if testcount >= 0:#len(testTasks):
            return render_template('index_real.html')
        else:
            return render_template(testTasks[testcount][0], task=testTasks[testcount][1], link='/testNasa')

@app.route('/testNasa', methods=['POST'])
def testNasa():
    return render_template('NASA-TLX_test.html', link='/testRest')

@app.route('/testRest', methods=['POST'])
def testRest():
    return render_template('rest_test.html', link='/test')

@app.route('/next', methods=['POST'])
def next():
    global tasks
    global taskCount
    global userAnswer
    global names
    global saveCount

    if request.method == 'POST':
        userName = request.form.get('search')
        if userName != None:
            print('Rest')
            startRecording(userName)
            injectMarker(0)
            userAnswer['name'] = userName
            userAnswer['value'] = {}

        taskCount += 1
        saveCount += 1
        if taskCount >= 2:#len(tasks):
            injectMarker(2)
            print('End')
            print(userAnswer)
            return render_template('end.html', link='/save')
        elif saveCount == 1:#10:
            print('Save Temp')
            print(userAnswer)
            injectMarker(2)
            taskCount -= 1
            return render_template('data_save.html', link='/save_temp')
        else:
            injectMarker(tasks[taskCount][2])
            print('VisCount', taskCount)
            print('Vis', tasks[taskCount][2])
            print(userAnswer)

            return render_template(tasks[taskCount][0], task=tasks[taskCount][1], link='/NASA')

@app.route('/save_temp', methods=['POST'])
def save_temp():
    global tasks
    global taskCount
    global userAnswer
    global saveCount

    if request.method == 'POST':
        print('Save Temp')
        data = pd.DataFrame(userAnswer['value'])
        path = 'C:/EEG data/EuroVis/UserData/' + userAnswer['name']

        try:
            if not os.path.exists(path):
                os.makedirs(path)
        except OSError:
            pass

        dataName = 'ans_' + str(taskCount)
        data.T.to_csv(path + '/' + dataName + '.csv', encoding='CP949')
        saveCount = -1

        return render_template('rerun.html', link='/next')

@app.route('/save', methods=['POST'])
def save_data():
    global tasks
    global taskCount
    global userAnswer

    if request.method == 'POST':
        print('Save')
        data = pd.DataFrame(userAnswer['value'])
        path = 'C:/EEG data/EuroVis/UserData/' + userAnswer['name']

        if taskCount == len(tasks):
            try:
                if not os.path.exists(path):
                    os.makedirs(path)
            except OSError:
                pass

        data.T.to_csv(path + '/' + 'ans_end.csv', encoding='CP949')
        stopRecording()

@app.route('/rest', methods=['POST'])
def rest():
    global tasks
    global taskCount
    global userAnswer

    if request.method == 'POST':
        injectMarker(0)
        print('Rest')
        task_split = tasks[taskCount][0].split('/')
        task_index = task_split[1] + '_' + task_split[2] + '_' + task_split[3] + '_' + task_split[4].replace('.html','')
        NASA_col = ['Mental', 'Physical', 'Temporal', 'Effort', 'Performance', 'Frustration']
        for col in NASA_col:
            userAnswer['value'][task_index][col] = request.form.get(col).replace('[POST]> ', '')

        return render_template('rest.html', link='/next')

@app.route('/NASA', methods=['POST'])
def nasa():
    global tasks
    global taskCount
    global userAnswer

    if request.method=='POST':
        injectMarker(1)
        print('Eval')
        task_split = tasks[taskCount][0].split('/')
        task_index = task_split[1] + '_' + task_split[2] + '_' + task_split[3] + '_' + task_split[4].replace('.html', '')

        userAnswer['value'][task_index] = {}
        ans = request.form.get('answer')
        if ans==None:
            userAnswer['value'][task_index]['Answer'] = 'Task 3'
        else:
            userAnswer['value'][task_index]['Answer'] = ans.replace('[POST]> ', '')

        userAnswer['value'][task_index]['marker'] = tasks[taskCount][2]
        return render_template('NASA-TLX.html', link='/rest')

if __name__ == '__main__':
    app.run(debug=True)