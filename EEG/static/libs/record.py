from static.libs.cortex import Cortex
from static.libs.user import user
from datetime import datetime
from threading import Thread
import time

class Record():
	def __init__(self):
		self.c = Cortex(user, debug_mode=True)
		self.c.do_prepare_steps()

	def record(self,
			   record_name,
			   record_description):
		self.c.create_record(record_name,
							 record_description)

	def add_markers(self, label):
		marker_time = time.time() * 1000
		print('add marker at : ', marker_time)

		marker = {
			"label": 'label',
			"value": label,
			"port": "python-app",
			"time": marker_time
		}
		self.c.inject_marker_request(marker)

	def export(self,
			   record_export_folder,
			   record_export_data_types,
			   record_export_format,
			   record_export_version):
		self.c.stop_record()
		self.c.disconnect_headset()
		self.c.export_record(record_export_folder,
							 record_export_data_types,
							 record_export_format,
							 record_export_version,
							 [self.c.record_id])


r = Record()

def startRecording(name):
	r.record(name,str(datetime.now()))

def injectMarker(label):
	r.add_markers(label)

def stopRecording():
	r.export('C:/EEG data/EuroVis',
			 ['EEG', 'MOTION', 'PM', 'MC', 'FE', 'BP'],
			 'CSV', 'V2' )
