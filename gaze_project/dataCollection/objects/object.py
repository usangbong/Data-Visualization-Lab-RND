import pyautogui

class Point:
    def __init__(self, x, y, validity):
        self.x = x
        self.y = y
        self.validity = validity

class Size:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def set(self, size):
        self.width = size.width
        self.height = size.height

class Geometry:
    def __init__(self, point, size):
        self.point = point
        self.size = size

    def set(self, geometry):
        self.point.x = geometry.x()
        self.point.y = geometry.y()
        self.size.width = geometry.width()
        self.size.height = geometry.height()