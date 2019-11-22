#I-VT & I-DT clustering algoritm: reference https://github.com/ecekt/eyegaze.git
#ece k.t.
from __future__ import division
import numpy as np
from collections import Counter

#column indices of attributes, check csv file
index = 0
timestamp = 1
question = 2
x = 3
y = 4
user_id = 5
group_size = 6
gaze_cue = 7

def ivt(data, v_threshold):
  times = data[:,timestamp]
    
	ts = []
    
	for t in times:
		ts.append(float(t)/1000.0)
     
	times = ts #TOD0: CHECK if times in sec
    
	Xs = data[:,x]
	Ys = data[:,y]
	
	difX = []
	difY = []
	tdif = []
	

	for i in range(len(data) - 1):
		difX.append(float(Xs[i+1]) - float(Xs[i]))
		difY.append(float(Ys[i+1]) - float(Ys[i]))
		tdif.append(float(times[i+1]) - float(times[i]))
        
	
	print tdif
	dif = np.sqrt(np.power(difX,2) + np.power(difY,2)) #in pix
	
	velocity = dif / tdif
	#print velocity in pix/sec
	#print tdif

	mvmts = [] #length is len(data)-1
	
	
	
  
