from flask import Flask, escape, request, jsonify, send_from_directory, abort, render_template
from flask_cors import CORS
from marvelmind import MarvelmindHedge
from time import sleep
import sys
from parse import *
from random import *
import csv

global idx

app = Flask(__name__)
cors = CORS(app, resources={'*': {"origins": "*"}})
idx=0
hedge = MarvelmindHedge(tty = "COM3", adr=5, debug=False) # create MarvelmindHedge thread
hedge.daemon = True
hedge.start();

f = open('./positions.csv', 'r', encoding='utf-8')
rdr = csv.reader(f)
csv = []
for line in rdr:
	if line[0] == 'x':
		continue
	csv.append([float(a) for a in line])
f.close()

@app.route('/')
def get_position():
    return jsonify(hedge.position());

@app.route('/beacon')
def get_beacon():
    f = open("map.ini", 'r')
    beacon_number = None
    beacons = [[i + 1, None, None, None, None] for i in range(20)]

    while True:
        line = f.readline()
        if not line: break
        
        result = parse("[beacon {:d}]", line)
        if result:
            beacon_number = result[0] - 1
            continue

        result = parse("Position_X= {:f}", line)
        if result:
            beacons[beacon_number][1] = result[0]
        
        result = parse("Position_Y= {:f}", line)
        if result:
            beacons[beacon_number][2] = result[0]
        
        result = parse("Position_Z= {:f}", line)
        if result:
            beacons[beacon_number][3] = result[0]

        result = parse("Hedgehog_mode= {:d}", line)
        if result:
            beacons[beacon_number][4] = bool(result[0])

    f.close()

    return jsonify(beacons);

@app.route('/log1')
def log1():
    f = open("logs/log1.txt", 'r')
    log = []

    while True:
        line = f.readline()
        if not line: break
        
        result = parse("Hedge 5: X: {:f}, Y: {:f}, Z: {:f}, Angle: 0 at time T: {:d}", line)
        if result:
            log.append({"x": result[0], "y": result[1], "z": result[2], "T": result[3]})
            continue

    f.close()

    return jsonify(log);

@app.route('/log2')
def log2():
    f = open("logs/log2.txt", 'r')
    log = []

    while True:
        line = f.readline()
        if not line: break
        
        result = parse("Hedge 5: X: {:f}, Y: {:f}, Z: {:f}, Angle: 0 at time T: {:d}", line)
        if result:
            log.append({"x": result[0], "y": result[1], "z": result[2], "T": result[3]})
            continue

    f.close()

    return jsonify(log);

@app.route('/wmr')
def wmr():
    f = open("test1.dat", 'r')
    log = []
    f.readline()

    while True:
        line = f.readline()
        if not line: break
        
        result = parse("{:f} #{:d} {:f} {:f} {:f} x: {:f}, y: {:f}, z: {:f}", line)
        if result:
            log.append({"x": result[2], "y": result[3], "yaw": result[4], "T": result[0]})
            continue
-]
    f.close()

    return jsonify(log);

@app.route('/write')
def write():
    hedge.write_log()
    return jsonify([]);

@app.route('/get-coordinate')
def get_coordinate():
	global idx
	i = randint(0, len(csv) - 1)
	
	idx += 1
	if idx>= len(csv) : 
		idx=0
	return jsonify(csv[idx])

@app.route('/get-image')
def get_image():
	try:
		i = randint(1, 5)
		filename = "%d.jpg" % i
		name = 'http://localhost:5000/static/images/%d.jpg' % i
		#return send_from_directory('./static/images', filename=filename, as_attachment=True)
		return name
	except FileNotFoundError:
		abort(404)
@app.route('/get-image2')
def get_image2():
	try:
		i = randint(1, 5)
		filename = "%d.jpg" % i
		name = "http://localhost:5000/static/images/%d.jpg" % i
		return name
		
	except FileNotFoundError:
		abort(404)
@app.route('/test')
def test():
	i = randint(1, 5)
	name = "./images/%d.jpg" % i
	print(name)
	return render_template('index.html', image_file=name )