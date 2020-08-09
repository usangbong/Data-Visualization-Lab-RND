import math

from objects import constant
from objects.object import Point


class GazeTuple:
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.id = 0
        self.timestamp = 0
        self.left_point = Point(0, 0, 0)
        self.right_point = Point(0, 0, 0)
        self.average_point = Point(0, 0, 0)

    def initialize(self, screen_size, paint_point, display_geometry):
        self.id = self.raw_data.get('id')
        self.timestamp = self.raw_data.get('device_time_stamp')
        self.extract_points()
        self.average_point = self.extract_average_point()
        self.calibrate(screen_size, paint_point, display_geometry.point)
        self.check_in_range(display_geometry.size)

    def extract_points(self):
        self.left_point = self.extract_point(constant.LEFT)
        self.right_point = self.extract_point(constant.RIGHT)

    def extract_point(self, direction):
        validity_attribute = '_gaze_point_validity'
        coordinate_attribute = '_gaze_point_on_display_area'
        attribute = 'left' if direction is constant.LEFT else 'right'

        validity = self.raw_data.get(attribute + validity_attribute)
        x = self.raw_data.get(attribute + coordinate_attribute)[0]
        y = self.raw_data.get(attribute + coordinate_attribute)[1]

        if math.isnan(x) or math.isnan(y):
            validity = 0
            x = 0 if math.isnan(y) else x
            y = 0 if math.isnan(y) else y

        return Point(x, y, validity)

    def extract_average_point(self):
        if self.left_point.validity == 0 or self.right_point.validity == 0:
            validity = 0
            x = 0
            y = 0
        else:
            validity = 1
            x = (self.left_point.x + self.right_point.x) / 2
            y = (self.left_point.y + self.right_point.y) / 2
        return Point(x, y, validity)

    def calibrate(self, screen_size, paint_point, display_point):
        self.left_point.x *= screen_size.width
        self.left_point.y *= screen_size.height
        self.right_point.x *= screen_size.width
        self.right_point.y *= screen_size.height
        self.average_point.x *= screen_size.width
        self.average_point.y *= screen_size.height

        self.left_point.x -= (paint_point.x + display_point.x)
        self.left_point.y -= (paint_point.y + display_point.y)
        self.right_point.x -= (paint_point.x + display_point.x)
        self.right_point.y -= (paint_point.y + display_point.y)
        self.average_point.x -= (paint_point.x + display_point.x)
        self.average_point.y -= (paint_point.y + display_point.y)

    def check_in_range(self, display_size):
        self.left_point.validity = 1 if self.is_in_range(constant.LEFT, display_size) else 0
        self.right_point.validity = 1 if self.is_in_range(constant.RIGHT, display_size) else 0
        self.average_point.validity = 1 if self.is_in_range(constant.AVERAGE, display_size) else 0

    def is_in_range(self, direction, display_size):
        if direction is constant.LEFT:
            if self.left_point.x <= 0 or self.left_point.x >= display_size.width: return False
            if self.left_point.y <= 0 or self.left_point.y >= display_size.height: return False
            return True
        if direction is constant.RIGHT:
            if self.right_point.x <= 0 or self.right_point.x >= display_size.width: return False
            if self.right_point.y <= 0 or self.right_point.y >= display_size.height: return False
            return True
        if direction is constant.AVERAGE:
            if self.average_point.x <= 0 or self.average_point.x >= display_size.width: return False
            if self.average_point.y <= 0 or self.average_point.y >= display_size.height: return False
            return True

    def is_validate(self, direction):
        if direction is constant.LEFT:
            return True if self.left_point.validity is 1 else False
        elif direction is constant.RIGHT:
            return True if self.right_point.validity is 1 else False
        elif direction is constant.AVERAGE:
            return True if self.average_point.validity is 1 else False