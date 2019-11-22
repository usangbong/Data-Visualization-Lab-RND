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
  
