# Copyright (C) 2017 Sejong University, Seoul, South Korea
# Yun Jang: jangy@sejong.edu
# Sangbong Yoo: usangbong@sju.ac.kr
# Sujin Jeong: tnwls0812@icloud.com

from threading import Lock
from flask import Flask, redirect, render_template, session, request, jsonify
import sqlite3
import MySQLdb
import pandas
import json
import csv
import os
from sqlalchemy import create_engine
from bson.json_util import dumps
from werkzeug.utils import secure_filename
from flask_socketio import SocketIO, emit
from skimage.filters.rank import entropy
from skimage.morphology import disk
from skimage.color import rgb2gray
from skimage import io
from skimage import img_as_float
from skimage import util
from skimage.filters import threshold_otsu
import matplotlib.pyplot as plt
import numpy
import scipy
import sys
sys.path.insert(0, './static/py')
import pySaliencyMap
import pySaliencyMapDefs
import cv2
# need subprocess for r script exec

async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

def background_thread():
    """Example of how to send server generated events to clients."""
    while True:
        #print 'sending...%d'% count
        mysqlCon = MySQLdb.connect(mysql_HOST, mysql_ID, mysql_PWD, mysql_DBNAME)
        mysqlCur = mysqlCon.cursor()
        # get data from database (mysql)
        datar = pandas.read_sql('SELECT * FROM %s' % tableName, mysqlCon)
        datar = datar.to_json()
        socketio.sleep(10)

        socketio.emit('refresh_data', {'table': datar}, namespace='/app_start_mysql')

# root function (own system) comment: 20180327
#@app.route('/')
#def get_image():
#    #print 'root'
#    return render_template('access.html')


@app.route('/access_local', methods=['GET'])
def access_local():
    #print 'access_local'
    return render_template('local.html')

@app.route('/system_local', methods=['GET', 'POST'])
def system_local():
    #print 'system_local'
    local_IMG = request.files['uploadImg']
    local_TXT = request.files['uploadTxt']
    imgname = secure_filename(local_IMG.filename)
    csvname = secure_filename(local_TXT.filename)

    # connect sqlite database (inmemory) & make table
    global sqliteCon
    sqliteCon = sqlite3.connect(':memory:')
    sqliteCon.execute('''CREATE TABLE gaze_test
                        (no INT PRIMARY KEY NOT NULL,
                         userid VARCHAR(50) NOT NULL,
                         timestep VARCHAR(50) NOT NULL,
                         timecount INT NOT NULL,
                         gazeX DOUBLE NOT NULL,
                         gazeY DOUBLE NOT NULL,
                         stiType INT NOT NULL,
                         usermemo INT);''')

    # read csv file
    with open('./static/data/%s'% csvname, 'rb') as csvfile:
        data_csv = csv.reader(csvfile)
        i = 0
        for row in data_csv:
            # make query
            qr = 'INSERT INTO gaze_test VALUES (%d, "%s", "%s", %s, %s, %s, %s, %s);'% (i, row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            #print qr
            # insert data into sqlite
            sqliteCon.execute(qr)
            i =  i + 1

    dataf = pandas.read_sql('SELECT * FROM gaze_test', sqliteCon)
    useridf = pandas.read_sql('SELECT userid FROM gaze_test GROUP BY userid', sqliteCon)
    dataf = dataf.to_json()
    useridJsonf = useridf.to_json()
    #print dataf

    #json_url = os.path.join("./static/data/data.json")
    #with open(json_url) as fdata:
    #    data = json.load(fdata)
    #print data
    #return render_template('local_connect.html',imgname=imgname, table=dataf)
    return render_template('graphs.html', imgname=imgname, table=dataf, userid=useridJsonf)

@app.route('/access_db_mysql', methods=['GET'])
def access_db_mysql():
    #print 'access_db_mysql'
    return render_template('db_connect_input_dialog.html')

@app.route('/system_mysql', methods=['GET', 'POST'])
def app_start_mysql():
    #print 'Database connection request'
    # connect mysql database
    global mysql_HOST
    global mysql_ID
    global mysql_PWD
    global mysql_DBNAME
    mysql_HOST = request.args.get('replyHost')
    mysql_ID = request.args.get('replyDBID')
    mysql_PWD = request.args.get('replyDBPW')
    mysql_DBNAME = request.args.get('replyDBname')


    print 'Set user database information'
    print 'Try to connect database: %s' % mysql_HOST
    mysqlCon = MySQLdb.connect(mysql_HOST, mysql_ID, mysql_PWD, mysql_DBNAME)
    mysqlCur = mysqlCon.cursor()
    tableList = pandas.read_sql('SELECT table_name FROM information_schema.tables where table_schema="%s"' % mysql_DBNAME, mysqlCon);

    print 'table list:\n%s' % tableList
    tableListJson = tableList.to_json()
    return dumps(tableListJson)

# comment by sangbong 20180329
#@app.route('/app_start_mysql', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def send_reply():
    global mysql_HOST
    global mysql_ID
    global mysql_PWD
    global mysql_DBNAME
    global tableName

    mysql_HOST = '223.195.38.39'
    mysql_ID = 'vis_dev'
    mysql_PWD = 'vislab604b'
    mysql_DBNAME = 'qtdbtestbysangbong'
    tableName = 'gaze_test'

    global imgvis
    imgvis = './static/img/d1.png'

    tableName = request.args.get('replyTable')
    tableName = 'gaze_test'
    print 'table name: %s' % tableName

    #print 'send_reply'
    mysqlCon = MySQLdb.connect(mysql_HOST, mysql_ID, mysql_PWD, mysql_DBNAME)
    mysqlCur = mysqlCon.cursor()

    # get data from database (mysql)
    datar = pandas.read_sql('SELECT * FROM %s ORDER BY timestep ASC' % tableName, mysqlCon)
    userid = pandas.read_sql('SELECT userid FROM %s GROUP BY userid' % tableName, mysqlCon)
    datar = datar.to_json()
    useridJson = userid.to_json()
    #print datar

    # get data which userid equals 'test'
    #datar_load=datar[datar.userid=='test']
    #return render_template('graphs.html', table=datar_load)
    imgname = imgvis
    return render_template('graphs.html', imgname=imgname, table=datar, userid=useridJson, async_mode=socketio.async_mode)

@app.route('/graph_type', methods=['GET'])
def graph_type():
    print 'graph_type'
    mysqlCon = MySQLdb.connect(mysql_HOST, mysql_ID, mysql_PWD, mysql_DBNAME)
    mysqlCur = mysqlCon.cursor()

    # get data from database (mysql)
    datar = pandas.read_sql('SELECT * FROM %s' % tableName, mysqlCon)
    datar = datar.to_json()

    return render_template('graph_select_type.html', table=datar)

@app.route('/calc_entropy', methods=['GET', 'POST'])
def calc_entropy():
    print 'calc_entropy'
    src_img = request.args.get('src_img')
    print src_img
    # input image
    #src = io.imread(src_img)
    src = io.imread('./static/img/coffee.jpg')

    # convert src image to grayscale
    gray_image = img_as_float(rgb2gray(src))

    fig, (ax0, ax1) = plt.subplots(ncols=2, figsize=(16, 6))

    diskLevel = 5
    img0 = ax0.imshow(gray_image, cmap=plt.cm.gray)

    thresh = threshold_otsu(gray_image)
    fe = gray_image > thresh
    feo = entropy(fe,disk(diskLevel))
    ifeo = util.invert(entropy(fe,disk(diskLevel)))
    ifeo_f = ifeo -fe

    img1 = ax1.imshow(ifeo_f, cmap=plt.cm.Greys)
    #ax1.set_title('Entropy')
    #fig.colorbar(img1, ax=ax1)

    #plt.show()
    scipy.misc.imsave('./static/img/en_res.png', util.invert(entropy(gray_image, disk(diskLevel))))

    entropy_res = entropy(gray_image, disk(diskLevel))

    return dumps(ifeo_f)

@app.route('/calc_features', methods=['GET', 'POST'])
def calc_features():
    print 'calc_features'
    src_img = request.args.get('src_img')
    print src_img
    img = cv2.imread('./static/img/nullschool_1.png')
    # initialize
    imgsize = img.shape
    img_width  = imgsize[1]
    img_height = imgsize[0]
    sm = pySaliencyMap.pySaliencyMap(img_width, img_height)
    # computation
    feature_intensity = sm.SMGetICM(img)
    feature_color = sm.SMGetCCM(img)
    feature_orientation = sm.SMGetOCM(img)

    intensity_res = img_as_float(feature_intensity)
    color_res = img_as_float(feature_color)
    orientation_res = img_as_float(feature_orientation)

    return dumps(intensity_res, color_res, orientation_res)

@app.route('/calc_feature_intensity', methods=['GET', 'POST'])
def calc_feature_intensity():
    print 'calc_feature_intensity'
    src_img = request.args.get('src_img')
    img = cv2.imread(imgvis)
    # initialize
    imgsize = img.shape
    img_width  = imgsize[1]
    img_height = imgsize[0]
    sm = pySaliencyMap.pySaliencyMap(img_width, img_height)
    # computation
    feature_intensity = sm.SMGetICM(img)
    intensity_res = img_as_float(feature_intensity)

    return dumps(intensity_res)

@app.route('/calc_feature_color', methods=['GET', 'POST'])
def calc_feature_color():
    print 'calc_feature_color'
    src_img = request.args.get('src_img')
    img = cv2.imread(imgvis)
    # initialize
    imgsize = img.shape
    img_width  = imgsize[1]
    img_height = imgsize[0]
    sm = pySaliencyMap.pySaliencyMap(img_width, img_height)
    # computation
    feature_color = sm.SMGetCCM(img)
    color_res = img_as_float(feature_color)

    return dumps(color_res)

@app.route('/calc_feature_orientation', methods=['GET', 'POST'])
def calc_feature_orientation():
    print 'calc_feature_orientation'
    src_img = request.args.get('src_img')
    img = cv2.imread(imgvis)
    # initialize
    imgsize = img.shape
    img_width  = imgsize[1]
    img_height = imgsize[0]
    sm = pySaliencyMap.pySaliencyMap(img_width, img_height)
    # computation)
    feature_orientation = sm.SMGetOCM(img)
    orientation_res = img_as_float(feature_orientation)

    return dumps(orientation_res)

#@app.route('/getUserData')
#def getUserData():
#    userid = request.agrs.get('userid')
#    userData = db.datar.find_one({'userid':userid})
#    print userData
#    return dumps(userData)

#@app.route('/refreshging_data')
#def refreshing_data(ws):
#    while True:
#        msg = ws.receive()
#        ws.send(msg)

#@socketio.on('refresh_data', namespace='/graph_type')
#def refresh_data():
#    print 'refresh_data'
#    mysqlCon = MySQLdb.connect(mysql_HOST, mysql_ID, mysql_PWD, mysql_DBNAME)
#    mysqlCur = mysqlCon.cursor()

    # get data from database (mysql)
#    datar = pandas.read_sql('SELECT * FROM %s' % tableName, mysqlCon)
#    datar = datar.to_json()
#    emit('refresh_data',{'table': datar})

@socketio.on('connect', namespace='/app_start_mysql')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)
    emit('refresh_data', {'table':0})

if __name__=='__main__':
    app.debug = True
    app.host = '0.0.0.0'
    #app.run(host='0.0.0.0')
    socketio.run(app)
