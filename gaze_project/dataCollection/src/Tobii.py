from datetime import datetime

import tobii_research as tr


class Tobii:
    def __init__(self, GazeTracker):
        self.tracker = GazeTracker
        self.tobii = tr.find_all_eyetrackers()[0]
        self.raw_data = RawData(self)
        self.dictionary = None
        self.isRunning = False

    def run(self):
        self.raw_data.__init__(self)
        self.isRunning = True
        self.tobii.subscribe_to(tr.EYETRACKER_GAZE_DATA, self.raw_data.gaze_data_callback, as_dictionary=True)

    def end(self):
        self.isRunning = False
        self.tobii.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, self.raw_data.gaze_data_callback)
        #self.tracker.data.order_in_time()
        #self.tracker.save()
        self.tracker.paint.points = []

    def to_dictionary(self):
        index = len(self.raw_data.left_gaze_point_on_display_area) - 1

        dictionary = {
            'id': self.raw_data.id,
            'left_gaze_point_on_display_area': self.raw_data.left_gaze_point_on_display_area[index],
            'right_gaze_point_on_display_area': self.raw_data.right_gaze_point_on_display_area[index],
            'left_gaze_point_validity': self.raw_data.left_gaze_point_validity[index],
            'right_gaze_point_validity': self.raw_data.right_gaze_point_validity[index],
            'device_time_stamp': self.raw_data.device_time_stamp[index]
        }
        self.tracker.plot(dictionary)


class RawData:
    def __init__(self, tobii):
        self.tobii = tobii
        self.id = datetime.now().strftime("%y%m%d%H%M%S")
        self.left_gaze_point_on_display_area = []
        self.right_gaze_point_on_display_area = []
        self.left_gaze_point_validity = []
        self.right_gaze_point_validity = []
        self.device_time_stamp = []

    def gaze_data_callback(self, gaze_data):
        self.left_gaze_point_on_display_area.append(gaze_data['left_gaze_point_on_display_area'])
        self.right_gaze_point_on_display_area.append(gaze_data['right_gaze_point_on_display_area'])
        self.left_gaze_point_validity.append(gaze_data['left_gaze_point_validity'])
        self.right_gaze_point_validity.append(gaze_data['right_gaze_point_validity'])
        self.device_time_stamp.append(gaze_data['device_time_stamp'])
        self.tobii.to_dictionary()
