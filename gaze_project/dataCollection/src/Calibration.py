import sys
from operator import eq

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QSize, QPoint, pyqtSlot
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QImage, QPalette, QBrush
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QSizePolicy, QSizeGrip

from gui.calibration import Ui_MainWindow


class Calibration(QMainWindow, Ui_MainWindow):
    resized = QtCore.pyqtSignal()
    def __init__(self, parent, url, image_size):
        super().__init__()
        self.main = parent
        self.setupUi(self)
        self.setAcceptDrops(True)
        self.url = url
        self.image = QImage(url)
        self.image_size = image_size
        self.setBackgroundExists()
        self.resized.connect(self.synchronize)
        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(flags)
        sizegrip = QSizeGrip(self)
        sizegrip.setVisible(True)
        self.gridLayout.addWidget(sizegrip)
        self.pushButton_close.clicked.connect(self.on_click)
        self.pushButton_cancel.clicked.connect(self.on_click)
        self.pushbutton_calibrate.clicked.connect(self.on_click)
        self.title.installEventFilter(self)
        self.pressing = False

    def setBackgroundExists(self):
        if self.image.isNull() is True:
            self.isBackgroundExists = False
        else:
            self.isBackgroundExists = True
            self.setBackground()

    @pyqtSlot()
    def on_click(self):
        sending_button = self.sender()
        if eq(sending_button.objectName(), "pushButton_close"):
            self.deleteLater()
        if eq(sending_button.objectName(), "pushButton_cancel"):
            self.deleteLater()
        if eq(sending_button.objectName(), "pushbutton_calibrate"):
            self.deleteLater()
            self.main.on_calibration_click("calibrate")

    def eventFilter(self, object, event):
        if object is self.title:
            if event.type() == QtCore.QEvent.MouseButtonPress:
                self.start = self.mapToGlobal(event.pos())
                self.pressing = True
            if event.type() == QtCore.QEvent.MouseMove:
                if self.pressing:
                    self.end = self.mapToGlobal(event.pos())
                    self.movement = self.end - self.start
                    self.setGeometry(self.mapToGlobal(self.movement).x(), self.mapToGlobal(self.movement).y(), self.width(), self.height())
                    self.start = self.end
            if event.type() == QtCore.QEvent.MouseButtonRelease:
                self.pressing = False
        return False

    def dragEnterEvent(self, e: QDragEnterEvent):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e: QDropEvent):
        if e.mimeData().hasUrls():
            e.accept()
            self.url = e.mimeData().urls()[0].toLocalFile()
            self.dropImage()
        else:
            e.ignore()

    def dropImage(self):
        self.image = QImage(self.url)
        self.image_size = self.image.size()
        self.isBackgroundExists = True
        self.setBackground()

    def resizeEvent(self, event):
        self.resized.emit()
        return super(Calibration, self).resizeEvent(event)

    def synchronize(self):
        if self.isBackgroundExists is False: return
        if self.isSameAspectRatio(self.size(), self.image.size()): return
        height = (self.size().width() * self.image.size().height()) / self.image.size().width()
        self.image_size = QSize(self.size().width(), height)
        self.setBackground()

    def setBackground(self):
        scaled = self.image.scaled(self.image_size)
        self.ratio = (100 * self.image_size.width()) / self.image.size().width()
        palette = QPalette()
        palette.setBrush(10, QBrush(scaled))
        self.resize(self.image_size)
        self.setPalette(palette)
        self.lwidth_value.setText("%d" % self.image_size.width())
        self.lheight_value.setText("%d" % self.image_size.height())
        self.lratio_value.setText("%0.2f" % self.ratio)

    def isSameAspectRatio(self, size1, size2):
        ratio1 = size1.width() / size1.height()
        ratio2 = size2.width() / size2.height()
        return True if ratio1 == ratio2 else False
