#ece k.t.
# code from https://github.com/ecekt/eyegaze/blob/master/gaze.py
from __future__ import division
import numpy as np
from collections import Counter

#column indices of attributes, check csv file
index = 0
timestamp = 0
question = 2
x = 4
y = 5
user_id = 1
group_size = 6
gaze_cue = 7


def ivt(data, v_threshold):
    
	times = data[:,timestamp]
    
	ts = []
	firstt = float(times[0])
	for t in times:
		ts.append((float(t)-firstt)*100/1000)
	
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
        
	
	#print tdif
	dif = np.sqrt(np.power(difX,2) + np.power(difY,2)) #in pix
		
	velocity = dif / tdif
	#print velocity in pix/sec
	#print tdif

	mvmts = [] #length is len(data)-1
	#print velocity
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
	firstm = mvmts[0]
	for m in range(len(mvmts)):
		if(mvmts[m] != firstm):
			if(len(fs) > 0):
				fixations.append(fs)
				fs = []
				fs.append(m)
				firstm = mvmts[m]
		else:
			fs.append(m)

	if(len(fs) > 0):
		fixations.append(fs)

	
	centroidsX = []
	centroidsY = []
	time0 = []
	time1 = []
	fixList = []

	for f in fixations:
		cX = 0
		cY = 0
		fixlist=''
		t0=0
		if(len(f) == 1):
			i = f[0]
			cX = float(data[i][x])
			cY = float(data[i][y])
			t0 = float((float(data[i][timestamp])-firstt))*100/1000
			fixlist = str(data[i][timestamp])+"/"
            
		else:
            
			for e in range(len(f)):
				t0 += (float(data[f[e]][timestamp])-firstt)*100/1000
				cX += float(data[f[e]][x]) 
				cY += float(data[f[e]][y])
				fixlist += str(data[f[e]][timestamp])+"/"
				#print f[e]

			
			
			
			t0 = t0/ float(len(f)+1)
			cX = cX / float(len(f)+1)
			cY = cY / float(len(f)+1)
			
            
		centroidsX.append(cX)
		centroidsY.append(cY)
		time0.append(t0)
		fixList.append(fixlist)

                
	return centroidsX, centroidsY, time0, time1, fixList, fixations

def idt(data, dis_threshold, dur_threshold):

	window_range = [0,0]

	current = 0 #pointer to represent the current beginning point of the window
	last = 0
	#final lists for fixation info
	centroidsX = []
	centroidsY = []
	time0 = []
	time1 = []
	tDif = []
	fixList = []
	fixations = []
    
	while (current < len(data)):
        
		t0 = float(data[current][timestamp]) #beginning time
		t1 = t0 + float(dur_threshold)     #time after a min. fix. threshold has been observed

		for r in range(current, len(data)): 
			if(float(data[r][timestamp])>= t0 and float(data[r][timestamp])<= t1):
				#print "if",r
				last = r #this will find the last index still in the duration threshold

		window_range = [current,last]

		#now check the dispersion in this window
		#print "window", current, last
		dispersion = get_dispersion(data[current:last+1])
		#a[2:5] gives 2,3,4. To include last one, [2:6]
        
        
		if (dispersion <= dis_threshold):

			#add new points
			while(dispersion <= dis_threshold and last + 1 < len(data)):

				last += 1
				window_range = [current,last]
				#print current, last, "*"
				#print "*"
				dispersion = get_dispersion(data[current:last+1])
       
			#dispersion threshold is exceeded
			#fixation at the centroid [current,last]

			cX = 0
			cY = 0
			fs = []
            
			for f in range(current, last + 1):
				cX += float(data[f][x])
				cY += float(data[f][y])
				fs.append([data[f][x], data[f][y]])

			cX = cX / float(last - current + 1)
			cY = cY / float(last - current + 1)
			fixList.append(fs)
    
			t0 = float(data[current][timestamp])
			t1 = float(data[last][timestamp])
			td = t1-t0
            
			centroidsX.append(cX)
			centroidsY.append(cY)
			time0.append(t0)
			time1.append(t1)
			tDif.append(td)
			fixations.append(last)
            
			current = last + 1 #this will move the pointer to a novel window

		else:
			current += 1 #this will remove the first point
			last = current #this is not necessary
            
	return centroidsX, centroidsY, time0, tDif, fixList, fixations


def get_dispersion(points):

	dispersion = 0
    
	argxmin = np.min(points[:,x].astype(np.float))
	argxmax = np.max(points[:,x].astype(np.float))
    
	argymin = np.min(points[:,y].astype(np.float))
	argymax = np.max(points[:,y].astype(np.float))

	dispersion = ((argxmax - argxmin) + (argymax - argymin))/2
	#TODO: look for other ways of calculating dispersion
    
	return dispersion

