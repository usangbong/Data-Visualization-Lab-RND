import math
import sys
from operator import eq
import pyautogui
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot, QSize
from PyQt5.QtGui import QImage, QPixmap, QPalette, QBrush, QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

from database.lib import MYSQL
from gui.main import Ui_MainWindow
from src.Calibration import Calibration
import database.constant as dbconstant
from src.Tracker import Tracker

class MainWindow(QMainWindow, Ui_MainWindow):
    resized = QtCore.pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_bubble.clicked.connect(self.on_click)
        self.pushButton_dbsetting.clicked.connect(self.on_click)
        self.pushButton_start.clicked.connect(self.on_click)
        self.pushButton_cancel.clicked.connect(self.on_click)
        self.pushButton_apply.clicked.connect(self.on_click)
        self.edit_id.returnPressed.connect(self.on_enter)
        self.check_id.stateChanged.connect(self.on_check)
        self.image = QImage()
        self.image_size = QSize()
        self.stack.setCurrentWidget(self.page_main)
        self.url = ""
        self.customConnected = False

    def setInitImageSize(self, img_url):
        self.image = QImage(self.url)
        width = self.image.size().width()
        if width <= 0:
            self.setImageSize(self.image_size)
            return
        self.image_size.setWidth(width)
        self.image_size.setHeight(self.getScaledHeight(width))
        self.setImageSize(self.image_size)
        
    def on_check(self):
        if self.check_id.isChecked():
            if self.isExistingID():
                self.warning("Duplicated ID!")
                self.check_id.setChecked(False)

    def on_enter(self):
        sending_edit = self.sender()
        if eq(sending_edit.objectName(), "edit_id"):
            if self.isExistingID():
                self.warning("Duplicated ID!")
            elif self.isValidID() is not True:
                self.edit_id.setText("")
            else:
                self.check_id.setChecked(True)

    def warning(self, warning):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(warning)
        msg.setWindowTitle("Error")
        msg.show()
        msg.exec_()

    def isValidID(self):
        if eq(self.edit_id.displayText(), "") is True: return False
        if len(self.edit_id.displayText()) > 255: return False
        return True

    def isExistingID(self):
        if self.customConnected is True:
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

        condition = {'id': self.edit_id.displayText()}
        count = dbconn.count(table=dbconstant.TABLE, condition=condition)
        dbconn.close()

        return True if count > 0 else False

    def isFloat(self, str):
        try:
            float(str)
            return True
        except:
            return False

    @pyqtSlot()
    def on_click(self):
        sending_button = self.sender()
        if eq(sending_button.objectName(), "pushButton_bubble"):
            self.toggleName(sending_button)
        if eq(sending_button.objectName(), "pushButton_dbsetting"):
            self.stack.setCurrentWidget(self.page_database)
        if eq(sending_button.objectName(), "pushButton_start"):
            isPlotting = True
            # 2. db check
            if self.check_id.isChecked():
                if eq(self.edit_id.text(), ""):
                    self.warning("there is no id")
                    return
                if self.isExistingID():
                    self.warning("Database ID Duplicated!")
                    return
                id = self.edit_id.text()
            else:
                id = ""
            # 3. image check
            self.url = "./resources/stanby.jpg"
            self.setInitImageSize(self.url)
            if eq(self.url, ""):
                self.warning("There is no image!")
                return
            if self.image_size.width() > pyautogui.size().width or self.image_size.height() > pyautogui.size().height:
                self.warning("Image size is too big")
                return
            self.tracking_window = Tracker(self.url, self.image_size, isPlotting, id, self.table, self.customConnected)
            self.tracking_window.showFullScreen()
            self.tracking_window.setFixedSize(self.tracking_window.size())
        if eq(sending_button.objectName(), "pushButton_ok"):
            print("on_click: pushbutton_ok")
            self.stack.setCurrentWidget(self.page_main)
        if eq(sending_button.objectName(), "pushButton_cancel"):
            filled = self.checkFilled()
            if filled is False:
                self.table.clearContents()
                self.stack.setCurrentWidget(self.page_main)
                return
            if self.checkConnect() is False:
                self.table.clearContents()
                self.stack.setCurrentWidget(self.page_main)
        if eq(sending_button.objectName(), "pushButton_apply"):
            print("on_click: pushButton_apply")
            if self.checkFilled() is not True:
                self.warning("Not Filled!")
                return
            if self.checkConnect() is True:
                self.stack.setCurrentWidget(self.page_main)
            else:
                print("on_click: else")
                self.warning("Not Valid Information!")

    def checkFilled(self):
        for row in range(5):
            if self.table.item(row, 0) is None:
                self.customConnected = False
                return False
        return True

    def checkConnect(self):
        dbconn = MYSQL(
            dbhost=self.table.item(0, 0).text(),
            dbuser=self.table.item(1, 0).text(),
            dbpwd=self.table.item(2, 0).text(),
            dbname=self.table.item(3, 0).text(),
            dbcharset=self.table.item(4, 0).text()
        )

        if dbconn.session() is None:
            dbconn.close()
            self.customConnected = False
            return False
        else:
            dbconn.close()
            self.customConnected = True
            return True

    def eventFilter(self, object, event):
        return False

    def setBoardBackground(self):
        print("setBoardBackground")

    def getScaledHeight(self, width):
        #print("getScaledHeight")
        height = math.floor((width * self.image.size().height()) / self.image.size().width())
        return height

    def setImageSize(self, size):
        #print("setImageSize function")
        self.image_size = size
        self.ratio = (100 * self.image_size.width()) / self.image.size().width()
        # self.label_widthValue.setText("%d" % self.image_size.width())
        # self.label_heightValue.setText("%d" % self.image_size.height())
        # self.edit_ratioValue.setText("%0.2f" % self.ratio)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
