import sys
from operator import eq
from time import sleep
import os

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
        self.fileList = ["./resources/Action/002.jpg", "./resources/Action/004.jpg", "./resources/Action/006.jpg", "./resources/Action/002.jpg", "./resources/Action/004.jpg", "./resources/Action/006.jpg"]
        self.oneSetNumber = 5
        self.dirNumber = 5
        self.setFilelist()
        self.timerVal = QTimer()
        self.timerVal.setInterval(1000)
        self.timerVal.timeout.connect(self.do_timeout)
        self.db_conn = self.db_connect()

    def setFilelist(self):
        if self.oneSetNumber*self.dirNumber > 200:
            self.oneSetNumber = 10
            self.dirNumber = 20
        self.dirList = os.listdir(self.stiPath)
        self.fileList = []
        self.checkList = []

        dirCount = 0
        for dirname in self.dirList:
            if dirCount > self.dirNumber-1:
                break
            _fileInDir = []
            _checkList = []
            _n = 2
            while _n < self.oneSetNumber:
                _fileInDir.append(self.stiPath+"/"+dirname+"/"+str(_n).zfill(3)+".jpg")
                _checkList.append(0)
                _n += 2
            self.fileList.append(_fileInDir)
            self.checkList.append(_checkList)
            dirCount += 1
        #print(self.fileList)
        print(len(self.fileList))


    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.key() == Qt.Key_1:
            self.visualizePressed()
        elif event.key() == Qt.Key_2:
            self.tobiiPressed()
            self.timerVal.start()
        elif event.key() == Qt.Key_3:
            self.imgCounting += 1
            print("imgCounting ++")
            if self.imgCounting < 4:
                self.image_url = self.fileList[self.imgCounting-1]
                self.setupImage()
            else:
                self.image_url = "./resources/default.jpg"
                self.setupImage()
                print("over index")
        elif event.key() == Qt.Key_Escape:
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
            self.paint.repaint()

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

    
    def do_timeout(self):
        self.imgCounting += 1
        print(self.imgCounting)
        if self.imgCounting < 5:
            self.image_url = self.fileList[self.imgCounting-1]
            self.setupImage()
            self.db_save()
        else:
            print("counting end")
            self.timerVal.stop()
            self.db_disconnect()
            self.tobii.end()
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Tracker("../resources/default.jpg", QSize(1200, 628), True, "default_test", QtWidgets.QTableWidget())
    ex.showFullScreen()
    ex.setFixedSize(ex.size())
    # ex.startTracking()

    sys.exit(app.exec_())
