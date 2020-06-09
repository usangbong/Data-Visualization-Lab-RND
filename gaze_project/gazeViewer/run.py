import os
import sys
import math
import time
import csv

from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout, QDesktopWidget, QLineEdit, QLabel, QTextEdit)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import (QPoint, QPointF, QRect, QRectF, QSize, Qt, QTime, QTimer, pyqtSlot, QFileInfo, QFile)

# import for gl
from PyQt5.QtGui import (QBrush, QColor, QFont, QFontMetrics, QImage, QLinearGradient, QRadialGradient, QPainter, QPen, QSurfaceFormat, QOpenGLShader, QOpenGLShaderProgram, QOpenGLTexture, QPixmap)
from PyQt5.QtWidgets import QOpenGLWidget
import OpenGL.GL as gl

from PIL import Image, ImageDraw

CSVDIRNAME = "Z:/paper_workspace/EuroVis_2020_short/participant_data_csv/"
CSVFILENAME = ""
CSVPATH = CSVDIRNAME+CSVFILENAME+".csv"
CSVDATA = []
LABELEDSTEP = []
STAGE_INDEX = []
TIMESTEP = 0
STEPSIZE = 1

WIDTH = 1920
HEIGHT = 1080
CARD_WIDTH = -1
CARD_HEIGHT = -1
CARD_HORIZONTAL_MARGIN = -1
CARD_VERTICAL_MARGIN = -1
TOTAL_WIDTH = -1
TOTAL_HEIGHT = -1
CARD_ROW = 4
CARD_COL = 3

DRAW_PUPIL_DIAMETER_POS = [60, 60]
CALI_LEFT_PUPIL = []
CALI_RIGHT_PUPIL = []
CALI_AVG_PUPIL = []
LEFT_MEAN_PUPIL_SIZE = 0
RIGHT_MEAN_PUPIL_SIZE = 0
AVG_MEAN_PUPIL_SIZE = 0
MAX_AVG_PUPIL_SIZE = 0
MIN_AVG_PUPIL_SIZE = 9999

STAGE_STATUS = 0

class Helper(object):
    def __init__(self):
        global CSVDIRNAME
        global CSVFILENAME
        global CSVPATH
        global CSVDATA

        self.background = QBrush(QColor(180, 180, 180))
        #CSVDATA = self.get_csv(CSVPATH)

    def paint(self, painter, event):
        global CSVDATA
        global STAGE_STATUS
        global TIMESTEP
        global CALI_AVG_PUPIL
        global DRAW_PUPIL_DIAMETER_POS
        global STAGE_INDEX

        # darw background
        painter.fillRect(event.rect(), self.background)
        painter.translate(0, 0)
        painter.save()

        # draw MAX pupil diameter Guidline (not real size)
        self.draw_Pupil_Diameter(painter, DRAW_PUPIL_DIAMETER_POS[0], DRAW_PUPIL_DIAMETER_POS[1], float(100), QColor(0, 0, 0, 255), 1, Qt.DotLine, QColor(255,255,255,255), Qt.SolidPattern)#Qt.FDiagPattern)

        if len(CSVDATA) != 0:
            # draw gaze points
            prevPointsColor = QColor(77, 77, 77)
            curPointColor = QColor(178, 24, 43)
            lineColor = QColor(31, 120, 180)
            STAGE_STATUS = CSVDATA[int(TIMESTEP)-1][13]
            _prev_x = -1
            _prev_y = -1
            _r = 10
            _w = 1
            lastPupilDiameter = len(CALI_AVG_PUPIL)
            for _tsCount in range(0, TIMESTEP):
                _row = CSVDATA[_tsCount]
                _curStageStatus = int(_row[13])

                if _tsCount == STAGE_INDEX[_curStageStatus]:
                    self.draw_Stage_Background(painter, _curStageStatus)
                    
                if _curStageStatus != STAGE_STATUS:
                    continue
                else:
                    _cur_x = _row[5]
                    _cur_y = _row[6]
                    
                    if _tsCount < TIMESTEP-1:
                        _color = prevPointsColor
                    elif _tsCount == TIMESTEP-1:
                        _color = curPointColor

                    if _prev_x == -1 and _prev_y == -1:
                        _prev_x = _cur_x
                        _prev_y = _cur_y
                    else:
                        self.draw_Line(painter, _prev_x, _prev_y, _cur_x, _cur_y, _w, lineColor)
                    self.draw_Ellipse(painter, _cur_x, _cur_y, _r, _color, _w, _color)
                    _prev_x = _cur_x
                    _prev_y = _cur_y

                # draw current pupil diameter
                curPupilDiameter = _row[11]
                diffMINMAX = MAX_AVG_PUPIL_SIZE-MIN_AVG_PUPIL_SIZE
                diffWeight = 50.0/diffMINMAX
                diffDia = curPupilDiameter - MIN_AVG_PUPIL_SIZE
                curRelativeDiaValue = 50.0 + (diffDia)*diffWeight
                self.draw_Pupil_Diameter(painter, DRAW_PUPIL_DIAMETER_POS[0], DRAW_PUPIL_DIAMETER_POS[1], curRelativeDiaValue, QColor(255, 255, 255, 0), 1, Qt.DotLine, QColor(251, 128, 114, 255), Qt.SolidPattern)#Qt.BDiagPattern)
            
        # draw MIN pupil diameter Guidline (not real size)
        self.draw_Pupil_Diameter(painter, DRAW_PUPIL_DIAMETER_POS[0], DRAW_PUPIL_DIAMETER_POS[1], float(50), QColor(0, 0, 0, 255), 1, Qt.DotLine, QColor(217,217,217,255), Qt.SolidPattern)#Qt.FDiagPattern)

        painter.restore()        

    def draw_Line(self, painter, _sx, _sy, _ex, _ey, _w, _c):
        pen = QPen(_c, _w, Qt.SolidLine)
        #pen.setStyle(Qt.DotLine)
        painter.setPen(pen)
        painter.drawLine(_sx, _sy, _ex, _ey)

    def draw_Card(self, painter, _x, _y, _w, _h, _penColor, _penWidth, _brushColor):
        pen = QPen(_penColor, _penWidth, Qt.DotLine)
        bru = QBrush(_brushColor, Qt.SolidPattern)
        painter.setPen(pen)
        painter.setBrush(bru)
        painter.drawRect(_x, _y, _w, _h)

    def draw_Ellipse(self, painter, _x, _y, _r, _penColor, _penWidth, _brushColor):
        _pen = QPen(_penColor, _penWidth, Qt.SolidLine)
        painter.setPen(_pen)
        _brush = QBrush(_brushColor, Qt.SolidPattern)
        painter.setBrush(_brush)
        painter.drawEllipse(_x-_r/2, _y-_r/2, _r, _r)

    def draw_Pupil_Diameter(self, painter, _x, _y, _diameter, _penColor, _penWidth, _penStyle, _brushColor, _brushStyle):
        pen = QPen(_penColor, _penWidth, _penStyle)
        brush = QBrush(_brushColor, _brushStyle)
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawEllipse(_x-_diameter/2, _y-_diameter/2, _diameter, _diameter)

    def get_Card_Total_Size(self, _r, _c, _card_width, _card_height, _h_space, _v_space):
        _total_width = (_c * _card_width) + ((_c-1) * _h_space)
        _total_height = (_r * _card_height) + ((_r-1) * _v_space)
        return _total_width, _total_height

    def get_Card_Distacne(self, _r, _c, _card_width, _card_height, _h_space, _v_space):
        _w_dis = (_c * _card_width) + (_c * _h_space)
        _h_dis = (_r * _card_height) + (_r * _v_space)
        return _w_dis, _h_dis

    def draw_Stage_Background(self, painter, _curStageStatus):
        global WIDTH
        global HEIGHT
        global CARD_WIDTH
        global CARD_HEIGHT
        global CARD_HORIZONTAL_MARGIN
        global CARD_VERTICAL_MARGIN
        global TOTAL_WIDTH
        global TOTAL_HEIGHT
        global CARD_ROW
        global CARD_COL
        if _curStageStatus == 0:
            self.background = QBrush(QColor(0, 0, 0))
        elif _curStageStatus == 1:
            self.background = QBrush(QColor(180, 180, 180))
        else:
            self.background = QBrush(QColor(180, 180, 180))
            _card_total_width, _card_total_height = self.get_Card_Total_Size(CARD_ROW, CARD_COL, CARD_WIDTH/2, CARD_HEIGHT/2, CARD_HORIZONTAL_MARGIN/2, CARD_VERTICAL_MARGIN/2)
            TOTAL_WIDTH = _card_total_width
            TOTAL_HEIGHT = _card_total_height
            for rowIdx in range(0, CARD_ROW):
                for colIdx in range(0, CARD_COL):
                    _distance_width = 0
                    _distance_height = 0
                    _w_dis, _h_dis = self.get_Card_Distacne(rowIdx, colIdx, CARD_WIDTH/2, CARD_HEIGHT/2, CARD_HORIZONTAL_MARGIN/2, CARD_VERTICAL_MARGIN/2)
                    sx = ((WIDTH - TOTAL_WIDTH)/2) + _w_dis
                    sy = ((HEIGHT - TOTAL_HEIGHT) / 2) + _h_dis
                    self.draw_Card(painter, sx, sy, CARD_WIDTH/2, CARD_HEIGHT/2, QColor(0,0,0), 2, QColor(130,130,130,0))#QColor(255,255,179)


    def get_csv(self, _filepath):
        global WIDTH
        global HEIGHT
        global CARD_WIDTH
        global CARD_HEIGHT
        global CARD_HORIZONTAL_MARGIN
        global CARD_VERTICAL_MARGIN
        global CALI_LEFT_PUPIL
        global CALI_RIGHT_PUPIL
        global CALI_AVG_PUPIL
        global LEFT_MEAN_PUPIL_SIZE
        global RIGHT_MEAN_PUPIL_SIZE
        global AVG_MEAN_PUPIL_SIZE
        global MAX_AVG_PUPIL_SIZE
        global MIN_AVG_PUPIL_SIZE
        global STAGE_INDEX

        f = open(_filepath, 'r', encoding='utf-8')
        c_csv = csv.reader(f)

        _prev_stage = -1
        _index = 0
        _csv_data = []
        # raw csv data colums
        # | (0) id | (1) status | (2) t | (3) t_order | (4) left_x | (5) left_y | (6) left_validity | (7) right_x | (8) right_y | (9) right_validity |
        # | (10) average_x | (11) average_y | (12) average_validity | (13) left_pupil_diameter | (14) left_pupil_validity | (15) right_pupil_diameter | 
        # | (16) right_pupil_validity | (17) average_pupil_diameter | (18) average_pupil_validity | (19) width | (20) height | (21) card_width | 
        # | (22) card_height | (23) card_horizontal_margin | (24) card_vertical_margin | (25) is_wandering |
        for row in c_csv:
            if row[0] == "id":
                continue
            # status | left_pupil_validity | right_pupil_validity | average_pupil_validity
            if int(row[1]) == 0 and int(row[14]) == 1 and int(row[16]) == 1 and int(row[18]) == 1:
                if CARD_WIDTH == -1 and CARD_HEIGHT -1 and CARD_HORIZONTAL_MARGIN == -1 and CARD_VERTICAL_MARGIN == -1:
                    #WIDTH = float(row[7])
                    #HEIGHT = float(row[8])
                    WIDTH = int(1920)
                    HEIGHT = int(1080)
                    CARD_WIDTH = float(row[21])
                    CARD_HEIGHT = float(row[22])
                    CARD_HORIZONTAL_MARGIN = float(row[23])
                    CARD_VERTICAL_MARGIN = float(row[24])
                    print("width: %d, height: %d"%(WIDTH, HEIGHT))
                    print("card_width: %f, card_height: %f, card_h_space: %f, card_v_space: %f"%(CARD_WIDTH, CARD_HEIGHT, CARD_HORIZONTAL_MARGIN, CARD_VERTICAL_MARGIN))
                CALI_LEFT_PUPIL.append(float(row[13]))
                CALI_RIGHT_PUPIL.append(float(row[15]))
                CALI_AVG_PUPIL.append(float(row[17]))
                #print("calibration pupil size...%d"%_index)

            # CSVDATA colums
            # | (0) id (raw=0)  | (1) left_x (raw=4) | (2) left_y (raw=5) | (3) right_x (raw=7) | (4) right_y (raw=8) | (5) average_x (raw=10) | (6) average_y (raw=11) |
            # | (7) t (raw=2) | (8) t_order (raw=3) | (9) left_pupil_diameter (raw=13) | (10) right_pupil_diameter (raw=15) | (11) average_pupil_diameter (raw=17) |  (12) is_wandering (raw=25) |
            # | (13) status (raw=1)
            if int(row[12]) == 1 and int(row[14]) != 0 and int(row[16]) != 0 and int(row[18]) != 0:
                # average_validity
                _row = [str(row[0]), float(row[4]), float(row[5]), float(row[7]), float(row[8]), float(row[10])/2.0, float(row[11])/2.0, int(row[2]), int(row[3]), float(row[13]), float(row[15]), float(row[17]), float(row[25]), int(row[1])]
                _csv_data.append(_row)

                if _row[11] > MAX_AVG_PUPIL_SIZE:
                    MAX_AVG_PUPIL_SIZE = _row[11]

                if _row[11] < MIN_AVG_PUPIL_SIZE:
                    MIN_AVG_PUPIL_SIZE = _row[11]

                if int(row[25]) == 1:
                    LABELEDSTEP.append(_index)
                
                _cur_stage = _row[13]
                if _prev_stage == -1:
                    _prev_stage = _cur_stage
                    STAGE_INDEX.append(1)
                else:
                    if _cur_stage != _prev_stage:
                        STAGE_INDEX.append(_index+1)

                _prev_stage = _cur_stage

                _index += 1



        f.close()
        return _csv_data

class GLWidget(QOpenGLWidget):
    def __init__(self, helper, parent):
        super(GLWidget, self).__init__(parent)
        self.helper = helper

        self.width = 1920
        self.height = 1080
        self.setFixedSize(self.width, self.height)
        self.setAutoFillBackground(False)

    def mousePressEvent(self, event):
        print("mouse click")

    def animate(self):
        self.update()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self.helper.paint(painter, event)
        painter.end()
        self.update()

class App(QDialog):
    def __init__(self):
        super().__init__()
        self.title = 'gazeDataViewer'
        self.width = 1920
        self.height = 1080

        self.helper = Helper()
        self.openGL = GLWidget(self.helper, self)

        self.initUI()

    def center(self):
        # geometry of the main window
        qr = self.frameGeometry()
        # center of the screen
        cp = QDesktopWidget().availableGeometry().center()
        # move the windos's point to the screen's center point
        qr.moveCenter(cp)
        # top left of window becomes top left of the window centering it
        self.move(qr.topLeft())

    def initUI(self):
        self.setWindowTitle(self.title)
        #self.setGeometry(self.left, self.top, self.width, self.height)

        self.resize(self.width, self.height)
        self.center()

        # set system function button
        self.csvfilenameTextBox = QLineEdit("\"INPUT USER ID\"")
        self.csvfilenameTextBox.setMaximumWidth(200)
        self.csvfilenameTextBox.setAlignment(Qt.AlignCenter)
        self.timeStepTextBox = QLineEdit("0")
        self.timeStepTextBox.setMaximumWidth(100)
        self.timeStepTextBox.setAlignment(Qt.AlignCenter)
        self.stepSizeTextBox = QLineEdit("1")
        self.stepSizeTextBox.setMaximumWidth(100)
        self.stepSizeTextBox.setAlignment(Qt.AlignCenter)

        self.dataLoadButton = QPushButton('LOAD')
        self.applyButton = QPushButton('APPLY')
        self.skipButton = QPushButton('SKIP')
        self.prevButton = QPushButton('PREV')
        self.nextButton = QPushButton('NEXT')
        self.saveStepButton = QPushButton('SAVE STEP IMAGE')
        self.saveAllStepButton = QPushButton('GENERATE ALL STEP IMAGE')

        self.dataLoadButton.clicked.connect(lambda: self.dataLoadButton_click())
        self.applyButton.clicked.connect(lambda: self.applyButton_click())
        self.skipButton.clicked.connect(lambda: self.skipButton_click())
        self.prevButton.clicked.connect(lambda: self.prevButton_click())
        self.nextButton.clicked.connect(lambda: self.nextButton_click())
        self.saveStepButton.clicked.connect(lambda: self.saveStepButton_click())
        self.saveAllStepButton.clicked.connect(lambda: self.saveAllStepButton_click())


        # set sub function button - select number
        self.createHorizontalGroupBox()
        self.createGridLayout()

        windowLayout = QGridLayout()
        windowLayout.setColumnStretch(0, 1)
        windowLayout.setColumnStretch(1, 2)

        #addWidget(QWidget *widget, int fromRow, int fromColumn, int rowSpan, int columnSpan, Qt::Alignment alignment = ...)
        windowLayout.addWidget(self.gridGroupBox, 0, 0, 1, 10)
        windowLayout.addWidget(self.horizontalGroupBox, 1, 0, 2, 10)

        self.setLayout(windowLayout)
        self.show()

    @pyqtSlot()
    def dataLoadButton_click(self):
        global CSVDIRNAME
        global CSVFILENAME
        global CSVPATH
        global TIMESTEP
        global CSVDATA
        global STAGE_INDEX

        dataloadflag = 0
        if self.csvfilenameTextBox.text() != "\"INPUT USER ID\"" and self.csvfilenameTextBox.text() != CSVFILENAME:
            CSVFILENAME = self.csvfilenameTextBox.text()
            dataloadflag = 1
        
        CSVPATH = CSVDIRNAME+CSVFILENAME+".csv"
        
        if dataloadflag == 1:
            CSVDATA = []
            CSVDATA = self.helper.get_csv(CSVPATH)
            if len(LABELEDSTEP) != 0 and LABELEDSTEP[0] != 0:
                skipBtnStr = "SKIP ("+str(LABELEDSTEP[0])+": 1/"+str(len(LABELEDSTEP))+")"
            else:
                skipBtnStr = "SKIP (N0_LABEL)"
            self.skipButton.setText(skipBtnStr)
            print("Data loaded: %s.csv"%CSVFILENAME)
            dataloadflag = 0

            TIMESTEP = 1
            self.timeStepTextBox.setText(str(TIMESTEP))
            self.nextButton.setText("NEXT-E:"+str(len(CSVDATA)))

            str_stage = "LOAD-"+str(STAGE_INDEX[0])+"|"+str(STAGE_INDEX[1])+"|"+str(STAGE_INDEX[2])            
            self.dataLoadButton.setText(str_stage)
        else:
            print("Data load fail")
            
        self.update()


    @pyqtSlot()
    def applyButton_click(self):
        global CSVDIRNAME
        global CSVFILENAME
        global CSVPATH
        global TIMESTEP
        global CSVDATA

        if self.csvfilenameTextBox.text() != "\"INPUT USER ID\"":
            CSVFILENAME = self.csvfilenameTextBox.text()
        
        CSVPATH = CSVDIRNAME+CSVFILENAME+".csv"
        
        _timeStep = int(self.timeStepTextBox.text())
        if _timeStep > len(CSVDATA):
            TIMESTEP = len(CSVDATA)
            self.timeStepTextBox.setText(str(len(CSVDATA)))
        else:
            TIMESTEP = _timeStep

        if len(LABELEDSTEP) != 0:
            for _t in range(0, len(LABELEDSTEP)):
                if TIMESTEP < LABELEDSTEP[_t]:
                    skipBtnStr = "SKIP ("+str(LABELEDSTEP[_t])+": "+str(_t+1)+"/"+str(len(LABELEDSTEP))+")"
                    break
                else:
                    skipBtnStr = "SKIP ("+str(LABELEDSTEP[_t])+": "+str(len(LABELEDSTEP))+"/"+str(len(LABELEDSTEP))+")"
            self.skipButton.setText(skipBtnStr)
        self.update()

    @pyqtSlot()
    def skipButton_click(self):
        global CSVDIRNAME
        global CSVFILENAME
        global CSVPATH
        global TIMESTEP
        global CSVDATA
        global LABELEDSTEP

        if len(LABELEDSTEP) != 0:
            for _t in range(0, len(LABELEDSTEP)):
                if TIMESTEP < LABELEDSTEP[_t]:
                    TIMESTEP = LABELEDSTEP[_t]
                    self.timeStepTextBox.setText(str(TIMESTEP))
                    if _t+1 < len(LABELEDSTEP):
                        skipBtnStr = "SKIP ("+str(LABELEDSTEP[_t+1])+": "+str(_t+2)+"/"+str(len(LABELEDSTEP))+")"
                        self.skipButton.setText(skipBtnStr)
                        break
                    else:
                        skipBtnStr = "SKIP ("+str(LABELEDSTEP[_t])+": "+str(len(LABELEDSTEP))+"/"+str(len(LABELEDSTEP))+")"
                        self.skipButton.setText(skipBtnStr)
                    break
        self.update()

    @pyqtSlot()
    def prevButton_click(self):
        global CSVFILENAME
        global TIMESTEP
        global CSVDATA
        global STEPSIZE
        global LABELEDSTEP
        global STAGE_STATUS

        _stepSize = int(self.stepSizeTextBox.text())
        if _stepSize < 0:
            _stepSize = 0
            self.stepSizeTextBox.setText("0")

        STEPSIZE = _stepSize

        if CSVFILENAME != self.csvfilenameTextBox.text():
            self.csvfilenameTextBox.setText(CSVFILENAME)

        TIMESTEP -= STEPSIZE
        if TIMESTEP > len(CSVDATA):
            TIMESTEP = len(CSVDATA)
            self.timeStepTextBox.setText(str(len(CSVDATA)))
        elif TIMESTEP < 0:
            TIMESTEP = 0
            self.timeStepTextBox.setText(str(TIMESTEP))
        else:
            self.timeStepTextBox.setText(str(TIMESTEP))

        if len(LABELEDSTEP) != 0:
            for _t in range(0, len(LABELEDSTEP)):
                if TIMESTEP < LABELEDSTEP[_t]:
                    skipBtnStr = "SKIP ("+str(LABELEDSTEP[_t])+": "+str(_t+1)+"/"+str(len(LABELEDSTEP))+")"
                    break
                else:
                    skipBtnStr = "SKIP ("+str(LABELEDSTEP[_t])+": "+str(len(LABELEDSTEP))+"/"+str(len(LABELEDSTEP))+")"
            self.skipButton.setText(skipBtnStr)

        if TIMESTEP != 0:
            _curStageStatus = int(CSVDATA[TIMESTEP-1][13])
            STAGE_STATUS = int(_curStageStatus)

        self.update()

    @pyqtSlot()
    def nextButton_click(self):
        global CSVFILENAME
        global TIMESTEP
        global CSVDATA
        global STEPSIZE
        global LABELEDSTEP
        global STAGE_STATUS

        self.nextButton.setText("NEXT-E:"+str(len(CSVDATA)))

        _stepSize = int(self.stepSizeTextBox.text())
        if _stepSize < 0:
            _stepSize = 0
            self.stepSizeTextBox.setText("0")

        STEPSIZE = _stepSize

        if CSVFILENAME != self.csvfilenameTextBox.text():
            self.csvfilenameTextBox.setText(CSVFILENAME)

        TIMESTEP += STEPSIZE
        if TIMESTEP > len(CSVDATA):
            TIMESTEP = len(CSVDATA)
            self.timeStepTextBox.setText(str(len(CSVDATA)))
        elif TIMESTEP < 0:
            TIMESTEP = 0
            self.timeStepTextBox.setText(str(TIMESTEP))
        else:
            self.timeStepTextBox.setText(str(TIMESTEP))

        if len(LABELEDSTEP) != 0:
            for _t in range(0, len(LABELEDSTEP)):
                if TIMESTEP < LABELEDSTEP[_t]:
                    skipBtnStr = "SKIP ("+str(LABELEDSTEP[_t])+": "+str(_t+1)+"/"+str(len(LABELEDSTEP))+")"
                    break
                else:
                    skipBtnStr = "SKIP ("+str(LABELEDSTEP[_t])+": "+str(len(LABELEDSTEP))+"/"+str(len(LABELEDSTEP))+")"
            self.skipButton.setText(skipBtnStr)

        if TIMESTEP != 0:
            _curStageStatus = int(CSVDATA[TIMESTEP-1][13])
            STAGE_STATUS = int(_curStageStatus)

        self.update()

    @pyqtSlot()
    def saveStepButton_click(self):
        global CSVDIRNAME
        global CSVFILENAME
        global TIMESTEP
        global STEPSIZE

        savedir_selected = "F:/workspace/EuroVis2020_data_collection/"+CSVFILENAME+"/interview/"
        self.create_directory(savedir_selected)
        self.saveSelectedStepDataToImg(savedir_selected)
        self.update()


    @pyqtSlot()
    def saveAllStepButton_click(self):
        global CSVDIRNAME
        global CSVFILENAME
        global TIMESTEP

        savedir_all = "F:/workspace/EuroVis2020_data_collection/"+CSVFILENAME+"/all/"
        self.create_directory(savedir_all)
        self.saveAllStepDataToImg(savedir_all)
        self.update()

    def create_directory(self, _dir):
        try:
            if not os.path.exists(_dir):
                os.makedirs(_dir)
        except OSError:
            print("Error: creating directory."+_dir)

    def saveAllStepDataToImg(self, _path):
        # CSVDATA colums
        # | (0) id (raw=0)  | (1) left_x (raw=4) | (2) left_y (raw=5) | (3) right_x (raw=7) | (4) right_y (raw=8) | (5) average_x (raw=10) | (6) average_y (raw=11) |
        # | (7) t (raw=2) | (8) t_order (raw=3) | (9) left_pupil_diameter (raw=13) | (10) right_pupil_diameter (raw=15) | (11) average_pupil_diameter (raw=17) |  (12) is_wandering (raw=25) |
        # | (13) status (raw=1)
        global CSVDATA
        global WIDTH
        global HEIGHT

        canvas = (int(WIDTH), int(HEIGHT))
        im = Image.new('RGB', canvas, (255, 255, 255))
        _r = 8
        _w = 2
        for saveIndex in range(0, len(CSVDATA)):
            if saveIndex == 0:
                continue
            _tsCount = 0
            _prev_x = 0
            _prev_y = 0
            for _p in CSVDATA:
                if saveIndex == _tsCount:
                    continue

                draw = ImageDraw.Draw(im)
                _lineColor = [31, 120, 180]
                _pointColor = [0, 0, 0]
                _x = _p[5]
                _y = _p[6]
                if _tsCount == 0:
                    _prev_x = _x
                    _prev_y = _y

                # drawline
                if _tsCount > 0:
                    draw.line((_prev_x, _prev_y, _x, _y), fill=(_lineColor[0], _lineColor[1], _lineColor[2]), width=_w)
                # set point color
                if _tsCount != saveIndex:
                    _pointColor = [77, 77, 77]
                elif _tsCount == saveIndex:
                    _pointColor = [178, 24, 43]
                # draw points
                draw.ellipse((_x-_r, _y-_r, _x+_r, _y+_r), fill=(_pointColor[0], _pointColor[1], _pointColor[2]))

                _prev_x = _x
                _prev_y = _y
                _tsCount += 1
            outputFileName = _path+CSVFILENAME+"_"+str(saveIndex)+".png"
            im.save(outputFileName)
            os.system('cls')
            print("%d/%d" %(saveIndex, len(CSVDATA)))
        print("all time step image saved.")

    def saveSelectedStepDataToImg(self, _path):
        # CSVDATA colums
        # | (0) id (raw=0)  | (1) left_x (raw=4) | (2) left_y (raw=5) | (3) right_x (raw=7) | (4) right_y (raw=8) | (5) average_x (raw=10) | (6) average_y (raw=11) |
        # | (7) t (raw=2) | (8) t_order (raw=3) | (9) left_pupil_diameter (raw=13) | (10) right_pupil_diameter (raw=15) | (11) average_pupil_diameter (raw=17) |  (12) is_wandering (raw=25) |
        # | (13) status (raw=1)
        global CSVDATA
        global WIDTHpython
        global HEIGHT
        global TIMESTEP
        global CSVFILENAME

        canvas = (int(WIDTH), int(HEIGHT))
        im = Image.new('RGB', canvas, (255, 255, 255))
        _tsCount = 0
        _prev_x = 0
        _prev_y = 0
        _r = 8
        _w = 2
        for _p in CSVDATA:
            draw = ImageDraw.Draw(im)
            _lineColor = [31, 120, 180]
            _pointColor = [0, 0, 0]
            _x = _p[5]
            _y = _p[6]
            if _tsCount == 0:
                _prev_x = _x
                _prev_y = _y

            # drawline
            if _tsCount > 0:
                draw.line((_prev_x, _prev_y, _x, _y), fill=(_lineColor[0], _lineColor[1], _lineColor[2]), width=_w)
            # set point color
            if _tsCount != TIMESTEP-1:
                _pointColor = [77, 77, 77]
            elif _tsCount == TIMESTEP-1:
                _pointColor = [178, 24, 43]
            # draw points
            draw.ellipse((_x-_r, _y-_r, _x+_r, _y+_r), fill=(_pointColor[0], _pointColor[1], _pointColor[2]))

            outputFileName = _path+CSVFILENAME+"_"+str(TIMESTEP)+".png"

                
            if _tsCount == TIMESTEP:    
                im.save(outputFileName)
                break
            else:
                _prev_x = _x
                _prev_y = _y
                _tsCount += 1

        print("selected time step image saved")

    def createHorizontalGroupBox(self):
        self.horizontalGroupBox = QGroupBox("| USER ID | DATA LOAD BTN | TIME STEP | APPLY BTN | STEP_SIZE |")
        layout = QGridLayout()

        layout.addWidget(self.csvfilenameTextBox, 0, 0, 1, 1)
        layout.addWidget(self.dataLoadButton, 0, 1, 1, 1)
        layout.addWidget(self.timeStepTextBox, 0, 2, 1, 1)
        layout.addWidget(self.applyButton,0, 3, 1, 1)
        layout.addWidget(self.stepSizeTextBox,0, 4, 1, 1)
        layout.addWidget(self.skipButton,0, 5, 1, 1)
        layout.addWidget(self.prevButton,0, 6, 1, 1)
        layout.addWidget(self.nextButton,0, 7, 1, 1)
        layout.addWidget(self.saveStepButton,0, 8, 1, 1)
        layout.addWidget(self.saveAllStepButton,0, 9, 1, 1)

        self.horizontalGroupBox.setLayout(layout)

    def createGridLayout(self):
        self.gridGroupBox = QGroupBox("Canvas")
        layout = QGridLayout()
        layout.addWidget(self.openGL)
        self.gridGroupBox.setLayout(layout)

    def createGLWidget(self):
        layout = QGLWidget(QtOpenGL.QGLFormat(QtOpenGL.QGL.SampleBuffers))

    def keyPressEvent(self, event):
        print("key pressed")
        #if event.key() == QtCore.Qt.Key_Left:
        #    print("left key pressed")
        #elif event.key() == QtCore.Qt.Key_Right:
        #    print("right key pressed")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())