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
	
	for v in velocity:
		if (v < v_threshold):
			#fixation
			mvmts.append(1)
			#print v, v_threshold
		else:
			mvmts.append(0)

	fixations = []
	fs = []

	#print mvmts
    
	for m in range(len(mvmts)):
		if(mvmts[m] == 0):
			if(len(fs) > 0):
				fixations.append(fs)
				fs = []
		else:
			fs.append(m)
			
			
	if(len(fs) > 0):
		fixations.append(fs)

	#print fixations
	centroidsX = []
	centroidsY = []
	time0 = []
	time1 = []
  
	for f in fixations:
		cX = 0
		cY = 0
        
		if(len(f) == 1):
			i = f[0]
			cX = (float(data[i][x]) + float(data[i+1][x]))/2.0
			cY = (float(data[i][y]) + float(data[i+1][y]))/2.0
			t0 = float(data[i][timestamp])
			t1 = float(data[i+1][timestamp])
            
		else:
			t0 = float(data[f[0]][timestamp])
			t1 = float(data[f[len(f)-1]+1][timestamp])
            
			for e in range(len(f)):
                
				cX += float(data[f[e]][x]) 
				cY += float(data[f[e]][y])

			cX += float(data[f[len(f)-1]+1][x]) 
			cY += float(data[f[len(f)-1]+1][y]) 
			
			cX = cX / float(len(f)+1)
			cY = cY / float(len(f)+1)
            
		centroidsX.append(cX)
		centroidsY.append(cY)
		time0.append(t0)
		time1.append(t1)
		
	return centroidsX, centroidsY, time0, time1	
