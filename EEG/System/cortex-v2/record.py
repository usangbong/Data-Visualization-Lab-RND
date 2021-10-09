from cortex import Cortex
from user import user
from datetime import datetime
from threading import Thread
import time

class Record():
	def __init__(self):
		self.c = Cortex(user, debug_mode=True)
		self.c.do_prepare_steps()

	def record(self,
			   record_name,
			   record_description,
			   record_length_s):
		self.c.create_record(record_name,
							 record_description)

	def add_markers(self, label):
		marker_time = time.time() * 1000
		print('add marker at : ', marker_time)

		marker = {
			"label": label,
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


	def wait(self, record_length_s):
		print('start recording -------------------------')
		length = 0
		while length < record_length_s:
			print('recording at {0} s'.format(length))
			time.sleep(1)
			length+=1
		print('end recording -------------------------')

def put_label(record_export_folder,
			 record_export_data_types,
			 record_export_format,
			 record_export_version):
	label = input('label: ')
	while label != 'end':
		print(label)
		r.add_markers(label)
		label = input('label: ')

	print(label)
	# stop record --> disconnect headset --> export record
	r.export(record_export_folder,
			 record_export_data_types,
			 record_export_format,
			 record_export_version )
	return label


if __name__ == "__main__":
	r = Record()

	record_name = input("이름: ")
	record_description = str(datetime.now())
	record_length_s = 10  # 기록 시간(초)
	record_export_folder = 'C:/EEG data'
	record_export_data_types = ['EEG', 'MOTION', 'PM', 'MC', 'FE', 'BP']
	record_export_format = 'CSV'
	record_export_version = 'V2'

	label_thread = Thread(target=put_label,
						  args=(record_export_folder,
								record_export_data_types,
								record_export_format,
								record_export_version))

	record_thread = Thread(target=r.record,
						   args=(record_name,
								 record_description,
								 record_length_s))
	record_thread.start()
	label_thread.start()
