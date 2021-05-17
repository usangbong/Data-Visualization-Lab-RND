# -*- coding: utf-8 -*-
from flask import Flask, abort,render_template, redirect, request, url_for, json, send_file, Response,jsonify, Blueprint, g
import pandas as pd
import numpy as np
import threading
import os
import platform

#앱
app = Flask(__name__) 

#시스템 온 로드 변수
home_dir = os.getcwd()

#시스템 판별 Windows Linux Darwin
OS_system = platform.system()

#thread 결과 모음과 락
add_thrd_res = 0
locker = threading.Lock()

IMG_NAME = ""


#특정 path위치의 1단계 하위리스트 출력 -> 실험자 목록이나 이미지 목록 리스트 출력.
def load_dir_list(direc):
	direcs = os.listdir(direc)
	resdic = []
	for di in direcs:
		#full_dir = os.path.join(direc, di)
		resdic.append(di.split('.')[0])
	return resdic

print(OS_system)
if OS_system == "Windows":
	experimental_list = load_dir_list(os.getcwd()+'\\static\\data\\experimental')
	experimental_image_list = load_dir_list(os.getcwd()+'\\static\\data\\experimental_image')

	visualization_list = load_dir_list(os.getcwd()+'\\static\\data\\vislist')
	patients_list = load_dir_list(os.getcwd()+'\\static\\data\\pati')
elif OS_system == "Darwin":
	experimental_list = load_dir_list(os.getcwd()+'/static/data/experimental')
	experimental_image_list = load_dir_list(os.getcwd()+'/static/data/experimental_image')

	visualization_list = load_dir_list(os.getcwd()+'/static/data/vislist')
	patients_list = load_dir_list(os.getcwd()+'/static/data/pati')	



params_list = {}
for name in visualization_list:
	df = pd.read_csv('static/data/vislist/'+name+'.csv',sep=",", dtype='unicode',header=0)
	params_list[name] = {'val':df['val'].tolist(),'tag':df['tag'].tolist()}

patient_list = {}
for name in patients_list:
	df = pd.read_csv('static/data/pati/'+name+'.csv',sep=",", dtype='unicode',header=0)
	patient_list[name] = {'id':df['id'].tolist()}
#print(params_list)

#data 반환 -> csv, 연산결과, 기타등등 

''' csv
@app.route("/data")
def data_resp():
	return None
'''
#연산결과 -> 순환식은 Thread 사용할 예정. #matrix일시 Process를 참조하여 수정
'''
def add_thrd_100(i):
	global add_thrd_res
	locker.acquire()
	try:
		add_thrd_res += i
	finally:
		locker.release()
	print("done : " + str(add_thrd_res))


for i in range(1,101):
	thrd_stack = threading.Thread(target=add_thrd_100,args=(i,))
	thrd_stack.start()
'''

@app.route("/data_res", methods=['GET','POST'])
def data_res():
	name = request.form['name']
	df = pd.read_csv('static/data/experimental/'+name+'.csv',sep=",", dtype='unicode', header=None, names=["no","userid","timestamp","timecount","x","y"])
	return df.to_json(orient='records')

@app.route("/clusted_data_res", methods=['GET','POST'])
def clusted_data_res():
	name = request.form['name']
	df = pd.read_csv('static/data/clusted_data/clusted_'+name+'.csv',sep=",", dtype='unicode', header=None)
	return df.to_json()
'''
@app.route("/vs_intensity_res", methods=['GET','POST'])
def vs_intensity_res():
	name = request.form['name']
	df = pd.read_csv('static/data/visual_saliency/'+name+'_intensity.csv',sep=",", dtype='unicode', header=None)
	return df.to_json()

@app.route("/vs_color_res", methods=['GET','POST'])
def vs_color_res():
	name = request.form['name']
	df = pd.read_csv('static/data/visual_saliency/'+name+'_color.csv',sep=",", dtype='unicode', header=None)
	return df.to_json()

@app.route("/vs_orientation_res", methods=['GET','POST'])
def vs_orientation_res():
	name = request.form['name']
	df = pd.read_csv('static/data/visual_saliency/'+name+'_orientation.csv',sep=",", dtype='unicode', header=None)
	return df.to_json()

@app.route("/vs_saliency_res", methods=['GET','POST'])
def vs_saliency_res():
	name = request.form['name']
	df = pd.read_csv('static/data/visual_saliency/'+name+'_orientation.csv',sep=",", dtype='unicode', header=None)
	return df.to_json()
'''
@app.route("/")
def home():
	return render_template('home.html',experimental_list=experimental_list,visualization_list=visualization_list,params_list=params_list,
		experimental_image_list=experimental_image_list,patient_list=patient_list)

if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0',port=5000)
	
	