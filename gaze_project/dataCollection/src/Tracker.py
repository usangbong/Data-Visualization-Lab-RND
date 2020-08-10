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
        self.setupImage()
        self.data = GazeData(self)
        self.tobii = Tobii(self)
        self.setupGeometries()
        self.stiPath = "./resources/sti"
        self.stanbyImagePath = "./resources/stanby.jpg"
        self.checkList = []
        self.dirList = []
        self.fileList = []
        self.oneSetNumber = 5
        self.dirNumber = 5
        self.totalStimulus = 0
        self.setFilelist()
        self.timerVal = QTimer()
        self.timerVal.setInterval(1000)
        self.timerVal.timeout.connect(self.do_timeout)
        self.db_conn = self.db_connect()

        self.dirShowCount = 0
        
        self.stanbyFlag = True
        self.stanbyCounting = 0
        self.dirIdx = 0
        self.fileIdx = 0

    def setFilelist(self):
        if self.oneSetNumber*self.dirNumber > 200:
            self.oneSetNumber = 10
            self.dirNumber = 20

        self.totalStimulus = self.oneSetNumber * self.dirNumber

        self.dirList = os.listdir(self.stiPath)
        self.fileList = []
        self.checkList = []

        dirCount = 0
        for dirname in self.dirList:
            if dirCount > self.dirNumber:
                break
            _fileInDir = []
            _checkList = []

            _n = 1
            while _n < self.oneSetNumber:
                _fileInDir.append(self.stiPath+"/"+dirname+"/"+str(_n*2).zfill(3)+".jpg")
                _checkList.append(0)
                _n += 1
            self.fileList.append(_fileInDir)
            self.checkList.append(_checkList)
            dirCount += 1
        print(self.fileList[0])
        #print(len(self.fileList))

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.key() == Qt.Key_1:
            self.visualizePressed()
        elif event.key() == Qt.Key_2:
            self.tobiiPressed()
            self.timerVal.start()
        # elif event.key() == Qt.Key_3:
        #     self.imgCounting += 1
        #     print("imgCounting ++")
        #     if self.imgCounting < 4:
        #         self.image_url = self.fileList[self.imgCounting-1]
        #         self.setupImage()
        #     else:
        #         self.image_url = "./resources/default.jpg"
        #         self.setupImage()
        #         print("over index")
        elif event.key() == Qt.Key_Escape:
            self.timerVal.stop()
            self.db_disconnect()
            self.tobii.end()
            self.close()

    def tobiiPressed(self):
        if self.tobii.isRunning: 
            self.endTracking()
        else: 
            self.startTracking()

    def visualizePressed(self):
        self.isPlotting = True if self.isPlotting is False else False

    def setupImage(self):
        self.paint.setFixedWidth(self.image_size.width())
        self.paint.setFixedHeight(self.image_size.height())

        pixmap = QPixmap(self.image_url)
        pixmap = pixmap.scaled(self.image_size)
        self.paint.setPixmap(pixmap)

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
        self.data.save(self.db_conn, self.id)
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

    def setStanbyFlag(self, _itv):
        if self.stanbyFlag == True:
            if self.stanbyCounting == 2:
                self.stanbyFlag = False
        else:
            self.stanbyFlag = True
        self.timerVal.setInterval(_itv)

    def getStanbyFlag(self):
        return self.stanbyFlag
    
    def do_timeout(self):
        print(self.imgCounting)
        self.dirIdx = self.imgCounting%self.dirNumber
        self.fileIdx = int(self.imgCounting/self.dirNumber)
        print("dirIdx: %d"%self.dirIdx)
        print("fileIdx: %d"%self.fileIdx)
        if self.imgCounting < self.totalStimulus:
            if self.stanbyFlag == True:
                if self.stanbyCounting == 0:
                    self.image_url = self.stanbyImagePath
                    self.setupImage()
                    self.setStanbyFlag(500)
                    self.setBackgroundColor_red()
                    self.stanbyCounting += 1
                elif self.stanbyCounting == 1:
                    self.setStanbyFlag(500)
                    self.setBackgroundColor_green()
                    self.stanbyCounting += 1
                elif self.stanbyCounting == 2:
                    self.setStanbyFlag(500)
                    self.setBackgroundColor_gray()
                    self.stanbyCounting = 0
            else:
                # self.setStanbyFlag(1000)
                self.setStanbyFlag(500)
                self.setBackgroundColor_black()
                if self.imgCounting < self.dirNumber:
                    self.image_url = self.fileList[self.dirIdx][0]
                    self.checkList[self.dirIdx][0] += 1
                elif self.imgCounting < self.totalStimulus/2:
                    self.setNoneDupStimulus()
                    #self.image_url = self.fileList[self.dirIdx][self.fileIdx]
                else:
                    self.setDupStimulus()
                    #self.image_url = self.fileList[self.dirIdx][0]
                    #self.image_url = self.fileList[self.dirIdx][self.fileIdx]
                self.db_save()
                self.imgCounting += 1
                self.setupImage()
        else:
            print("End data collecting")
            self.timerVal.stop()
            self.db_disconnect()
            self.tobii.end()
            self.close()
    
    def setNoneDupStimulus(self):
        rVal = -999
        while rVal < 0:
            rVal = randint(1, len(self.checkList[self.dirIdx])-1)
            if self.checkList[self.dirIdx][rVal] == 0:
                self.checkList[self.dirIdx][rVal] += 1
                break
            else:
                rVal = -999
        self.image_url = self.fileList[self.dirIdx][rVal]
        
    def setDupStimulus(self):
        rVal = -999
        while rVal < 0:
            rVal = randint(0, len(self.checkList[self.dirIdx])-1)
            if self.checkList[self.dirIdx][rVal] != 0:
                self.checkList[self.dirIdx][rVal] += 1
                break
            else:
                rVal = -999
        self.image_url = self.fileList[self.dirIdx][rVal]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Tracker("./resources/stanby.jpg", QSize(1200, 628), True, "default_test", QtWidgets.QTableWidget())
    ex.showFullScreen()
    ex.setFixedSize(ex.size())
    # ex.startTracking()

    sys.exit(app.exec_())
