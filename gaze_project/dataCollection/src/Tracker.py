import sys
from operator import eq
from time import sleep
import os
from random import *

import pyautogui
from PyQt5 import QtCore, QtWidgets, QtTest, QtGui
from PyQt5.QtCore import QSize, QCoreApplication, QEventLoop, QTimer, Qt, QTime
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QImage, QPalette, QBrush, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QSizePolicy

from database import constant as dbconstant
from database.lib import MYSQL
from gui.tracker import Ui_MainWindow
from objects import constant
from objects.GazeData import GazeData
from src.Tobii import Tobii

class Tracker(QMainWindow, Ui_MainWindow):
    def __init__(self, url, size, isPlotting, id, table, isCustomed):
        super().__init__()
        self.setupUi(self)
        self.image_url = url
        self.image_size = size
        self.isPlotting = isPlotting
        self.id = id
        self.table = table
        self.isCustomed = isCustomed
        self.imgCounting = 0
        #self.setupImage()
        self.data = GazeData(self)
        self.tobii = Tobii(self)
        self.setupGeometries()
        self.stiPath = "./resources/stimuli"
        self.stanbyImagePath = "./resources/stanby.jpg"
        self.checkList = []
        self.stiList = []
        self.fileList = []
        self.oneSetNumber = 10
        self.totalStimulus = 0
        self.setFilelist()
        self.stanbyTime = 1000
        self.showTime = 5000
        # self.stanbyTime = 500
        # self.showTime = 500
        self.timerVal = QTimer()
        self.timerVal.setInterval(self.stanbyTime)
        self.timerVal.timeout.connect(self.do_timeout)
        self.db_conn = self.db_connect()

        self.dirShowCount = 0
        self.stanbyFlag = True
        self.stanbyCounting = 0
        self.dirIdx = 0
        self.fileIdx = 0
        self.stiFilePath = ""


    def setFilelist(self):
        self.stiList = os.listdir(self.stiPath)
        self.fileList = []
        for stiDataset in self.stiList:
            dirList = os.listdir(self.stiPath+"/"+stiDataset)
            for dirname in dirList:
                if stiDataset == "MIT1003":
                    _filePath = self.stiPath+"/"+stiDataset+"/"+dirname
                    self.fileList.append(_filePath)
                    self.totalStimulus += 1
                else:
                    imageList = os.listdir(self.stiPath+"/"+stiDataset+"/"+dirname)
                    for imgFile in imageList:
                        _filePath = self.stiPath+"/"+stiDataset+"/"+dirname+"/"+imgFile
                        self.fileList.append(_filePath)
                        self.totalStimulus += 1


    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.key() == Qt.Key_1:
            self.visualizePressed()
        elif event.key() == Qt.Key_2:
            self.tobiiPressed()
            self.timerVal.start()
        elif event.key() == Qt.Key_Escape:
            self.timerVal.stop()
            self.db_disconnect()
            self.tobii.end()
            self.deleteLater()
            self.close()

    def tobiiPressed(self):
        if self.tobii.isRunning: 
            self.endTracking()
        else: 
            self.startTracking()

    def visualizePressed(self):
        self.isPlotting = True if self.isPlotting is False else False

    def setupImage(self):
        _exW = 2920-self.image_size.width()
        _exH = 1580-self.image_size.height()
        self.paint.setFixedWidth(self.image_size.width()+_exW)
        self.paint.setFixedHeight(self.image_size.height()+_exH)
        # self.paint.setFixedWidth(1920+1000)
        # self.paint.setFixedHeight(1080+500)

        pixmap = QPixmap(self.image_url)
        pixmap = pixmap.scaled(self.image_size)
        
        self.paint.setPixmap(pixmap)

    def setupImagePainter(self):
        _exW = 2920-self.image_size.width()
        _exH = 1580-self.image_size.height()
        self.paint.setFixedWidth(self.image_size.width()+_exW)
        self.paint.setFixedHeight(self.image_size.height()+_exH)
        # self.paint.setFixedWidth(1920+1000)
        # self.paint.setFixedHeight(1080+500)
        # self.paint.setRandomPosition(self.imgCounting, self.totalStimulus)
        self.paint.setImagePosition(self.image_size.width(), self.image_size.height())


        self.paint.setStiImage(self.image_url)
        self.paint.repaint()
        
    def setupGeometries(self):
        window = pyautogui.size()
        self.data.synchronize_geometries(window, self.geometry(), self.paint)

    def startTracking(self):
        self.showFullScreen()
        self.setFixedSize(self.size())
        self.setupGeometries()
        self.tobii.run()

    def endTracking(self):
        self.tobii.end()
        self.deleteLater()

    def plot(self, tuple):
        self.data.add_tuple(tuple)
        if self.isPlotting is False: return

        if self.data.data[-1].is_validate(constant.AVERAGE):
            self.paint.left = self.data.data[-1].left_point
            self.paint.right = self.data.data[-1].right_point
            self.paint.average = self.data.data[-1].average_point
            #self.paint.repaint()

    def db_connect(self):
        if self.isCustomed:
            dbconn = MYSQL(
                dbhost=self.table.item(0, 0).text(),
                dbuser=self.table.item(1, 0).text(),
                dbpwd=self.table.item(2, 0).text(),
                dbname=self.table.item(3, 0).text(),
                dbcharset=self.table.item(4, 0).text()
            )
        else:
            dbconn = MYSQL(
                dbhost=dbconstant.HOST,
                dbuser=dbconstant.USER,
                dbpwd=dbconstant.PASSWORD,
                dbname=dbconstant.DB_NAME,
                dbcharset=dbconstant.CHARSET
            )
        return dbconn

    def db_disconnect(self):
        self.db_conn.close()

    def db_save(self):
        self.data.order_in_time()
        _sti_x = self.paint.getStiPosition(0)
        _sti_y = self.paint.getStiPosition(1)
        self.data.save(self.db_conn, self.id, self.imgCounting, self.image_url, self.image_size.width(), self.image_size.height(), _sti_x, _sti_y)
        self.data.reset_data()
        
    def save(self):
        if self.isCustomed:
            dbconn = MYSQL(
                dbhost=self.table.item(0, 0).text(),
                dbuser=self.table.item(1, 0).text(),
                dbpwd=self.table.item(2, 0).text(),
                dbname=self.table.item(3, 0).text(),
                dbcharset=self.table.item(4, 0).text()
            )
        else:
            dbconn = MYSQL(
                dbhost=dbconstant.HOST,
                dbuser=dbconstant.USER,
                dbpwd=dbconstant.PASSWORD,
                dbname=dbconstant.DB_NAME,
                dbcharset=dbconstant.CHARSET
            )

        self.data.save(dbconn, self.id)
        dbconn.close()

    # def setStanbyFlag(self, _itv):
    #     if self.stanbyFlag == True:
    #         if self.stanbyCounting == 2:
    #             self.stanbyFlag = False
    #     else:
    #         self.stanbyFlag = True
    #     self.timerVal.setInterval(_itv)
    def setStanbyFlag(self, _itv):
        if self.stanbyFlag == True:
            self.stanbyFlag = False
        else:
            self.stanbyFlag = True
        self.timerVal.setInterval(_itv)

    def getStanbyFlag(self):
        return self.stanbyFlag
    
    def do_timeout(self):
        if self.imgCounting < self.totalStimulus:
            if self.stanbyFlag == True:
                # if self.stanbyCounting == 0:
                #     self.image_url = self.stanbyImagePath
                #     #self.setupImage()
                #     self.setupImagePainter()
                #     self.setStanbyFlag(self.stanbyTime)
                #     self.stanbyCounting += 1
                # elif self.stanbyCounting == 1:
                #     self.setStanbyFlag(self.stanbyTime)
                #     self.stanbyCounting += 1
                # elif self.stanbyCounting == 2:
                #     self.setStanbyFlag(self.stanbyTime)
                #     self.stanbyCounting = 0
                self.image_url = self.stanbyImagePath
                self.setupImagePainter()
                self.setStanbyFlag(self.stanbyTime)
                
            else:
                self.setStanbyFlag(self.showTime)
                self.image_url = self.fileList[self.imgCounting]
                print(self.image_url)
                
                self.db_save()
                self.imgCounting += 1
                #self.setupImage()
                self.setupImagePainter()
        else:
            print("End data collecting")
            self.timerVal.stop()
            self.db_disconnect()
            self.tobii.end()
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Tracker("./resources/stanby.jpg", QSize(1200, 628), True, "default_test", QtWidgets.QTableWidget())
    ex.showFullScreen()
    ex.setFixedSize(ex.size())
    # ex.startTracking()
    sys.exit(app.exec_())
