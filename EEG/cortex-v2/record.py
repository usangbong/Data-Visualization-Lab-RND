from cortex import Cortex
from user import user
import time

class Record():
	def __init__(self):
		self.c = Cortex(user, debug_mode=True)
		self.c.do_prepare_steps()

	def create_record_then_export(self,
								record_name,
								record_description,
								record_length_s,
								record_export_folder,
								record_export_data_types,
								record_export_format,
								record_export_version):
		
		self.c.create_record(record_name,
							record_description)

		self.wait(record_length_s)

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


r = Record()

# record parameters
record_name = 'test3'
record_description = 'test1_30'
record_length_s = 2 #기록 시간(초)


# export parameters
record_export_folder = 'C:/EEG data'
record_export_data_types = ['EEG', 'MOTION', 'PM', 'MC', 'FE', 'BP']
record_export_format = 'CSV'
record_export_version = 'V2'


# start record --> stop record --> disconnect headset --> export record
r.create_record_then_export(record_name,
							record_description,
							record_length_s,
							record_export_folder,
							record_export_data_types,
							record_export_format,
							record_export_version )
# -----------------------------------------------------------
