# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lasttrial.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel

from objects.object import Point, Size


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(838, 615)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 1, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.paint = Paint(self.centralwidget)
        self.paint.setStyleSheet("background-color: black")
        self.paint.setObjectName("paint")
        self.gridLayout_2.addWidget(self.paint, 1, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 1, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 2, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 2, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 2, 2, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.setBackgroundColor()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    def setBackgroundColor(self):
        self.label.setStyleSheet("background-color: black;")
        self.label_2.setStyleSheet("background-color: black;")
        self.label_3.setStyleSheet("background-color: black;")
        self.label_4.setStyleSheet("background-color: black;")
        self.label_6.setStyleSheet("background-color: black;")
        self.label_7.setStyleSheet("background-color: black;")
        self.label_8.setStyleSheet("background-color: black;")
        self.label_9.setStyleSheet("background-color: black;")


class Paint(QLabel):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.points = []
        self.left = Point(0, 0, 0)
        self.right = Point(0, 0, 0)
        self.average = Point(0, 0, 0)
        self.my_size = Size(0, 0)

    def paintEvent(self, e):
        super().paintEvent(e)
        if self.average.validity is 0: return
        self.points.append(self.average)

        qp = QtGui.QPainter(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing)
        pen = QtGui.QPen(QtCore.Qt.red, 5)
        brush = QtGui.QBrush(QtCore.Qt.red)
        qp.setPen(pen)
        qp.setBrush(brush)

        qp.drawEllipse(self.points[-1].x, self.points[-1].y, 5, 5)

        # for point in self.points:
        #     qp.drawEllipse(point.x, point.y, 5, 5)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
