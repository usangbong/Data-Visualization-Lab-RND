
# coding: utf-8

# In[ ]:


import sys
import os
import cv2
import numpy as np
import math
import random
import copy
import time
import shutil

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from functools import partial
from numpy import unique
from scipy.stats import entropy as scipy_entropy
from math import log, e


from subimage_control import SubImageControl
from imgproc import ImgProc
from uIuserfunction import UIuserFunction




class App(QDialog):
    def __init__(self, parent=None):
        super(App,self).__init__(parent)
        self.chosen_points = []
        self.title = 'test window'
        self.left = 100
        self.top = 100
        self.width = 1500
        self.height = 1000
        self._image = QPixmap(700,700)
        self._image.fill(QColor(240,240,240))
        self.currentGridSize = 64
        self.subImglist = []
        self.subPos = []
        self.subImage_labellist = []
        self.subImage_labelPos = []
        self.selectedIdx = []
        self.classifyWindow=''
        self.subImages = SubImageControl()
        self.subImages._ToUpdate.connect(self._updateWidgets)

        self._image_originSize = [700,700]
        self.selectedImageScrollBarIndex = 0
        self.classedImageScrollBarIndex = 0
        self.flagSelecting_Button1 = False
        self.flagSelecting_Button2 = False
        self.flagViewClass = [True, True, True, True, True, True]

        self.modelFileName = ""
        self.initUI()
        ImgProc.Init()


        #test learning.py
        #Learning()



    @pyqtSlot(int)
    def _updateWidgets(self, index) :
        self.re_draw_rawImageRect()
        self.re_draw_subImageWidget()
        self.re_draw_classWidget()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.createCtrlLayout()        #Top - 2row, 5col gridLayout (10button)
        self.createRawImageLayout()        #Mid - 2col gridLayout (1Image, 1 VLayout)
        self.createSelectImageLayout()        #Bottom - vLayout (HLayout + scrollbar )
        self.createClassLayout()

        self.MainLayout = QGridLayout()
        self.ImagesLayout = QGridLayout()
        self.ImagesLayout.addWidget(self.ctrlGroupBox, 0, 0, 1, 1)
        self.ImagesLayout.addWidget(self.rawImageGroupBox, 1, 0, 7, 1)
        self.ImagesLayout.addWidget(self.selectImageGroupBox, 8, 0, 2, 1)
        self.ImagesLayout.setAlignment(Qt.AlignTop)

        self.ClassLayout = QHBoxLayout()
        self.ClassLayout.addWidget(self.classGroupBox)
        self.ClassLayout.setAlignment(Qt.AlignTop)

        self.MainLayout.addLayout(self.ImagesLayout,0,0,1,2)
        self.MainLayout.addLayout(self.ClassLayout,0,2,1,1)
        self.setLayout(self.MainLayout)

        #self.setFixedWidth(1000)
        self.show()

    def _get_line(self, vertical=True):
        line = QFrame()
        line.setContentsMargins(0, 0, 0, 0)
        if vertical is True:
            line.setFrameShape(line.VLine)
        else:
            line.setFrameShape(line.HLine)
        line.setFrameShadow(line.Sunken)
        return line

    def createClassLayout(self) :
        self.classGroupBox = QGroupBox("classify")

        self.classedImageLayout = QGridLayout()

        self.button_class1 = QPushButton('class1 [1:q]')
        self.button_class2 = QPushButton('class2 [2:w]')
        self.button_class3 = QPushButton('class3 [3:e]')
        self.button_class4 = QPushButton('class4 [4:r]')
        self.button_class5 = QPushButton('class5 [5:t]')

        self.button_class1.setStyleSheet("background-color: rgb(200,100,0)")
        self.button_class2.setStyleSheet("background-color: rgb(100,200,0)")
        self.button_class3.setStyleSheet("background-color: rgb(50,100,150)")
        self.button_class4.setStyleSheet("background-color: rgb(100,100,100)")
        self.button_class5.setStyleSheet("background-color: rgb(100,50,150)")

        self.button_class1.clicked.connect(partial(self.saveSelectedImage, 1))
        self.button_class2.clicked.connect(partial(self.saveSelectedImage, 2))
        self.button_class3.clicked.connect(partial(self.saveSelectedImage, 3))
        self.button_class4.clicked.connect(partial(self.saveSelectedImage, 4))
        self.button_class5.clicked.connect(partial(self.saveSelectedImage, 5))

        self.classedImageLayout.addWidget(self.button_class1,0,0)
        self.classedImageLayout.addWidget(self.button_class2,0,2)
        self.classedImageLayout.addWidget(self.button_class3,0,4)
        self.classedImageLayout.addWidget(self.button_class4,0,6)
        self.classedImageLayout.addWidget(self.button_class5,0,8)

        self.class1Layout =  QVBoxLayout()
        self.class1Layout.addStretch()
        self.class2Layout =  QVBoxLayout()
        self.class2Layout.addStretch()
        self.class3Layout =  QVBoxLayout()
        self.class3Layout.addStretch()
        self.class4Layout =  QVBoxLayout()
        self.class4Layout.addStretch()
        self.class5Layout =  QVBoxLayout()
        self.class5Layout.addStretch()

        self.classedImageLayout.addLayout(self.class1Layout,1,0)
        self.classedImageLayout.addLayout(self.class2Layout,1,2)
        self.classedImageLayout.addLayout(self.class3Layout,1,4)
        self.classedImageLayout.addLayout(self.class4Layout,1,6)
        self.classedImageLayout.addLayout(self.class5Layout,1,8)

        line1 = self._get_line()
        line2 = self._get_line()
        line3 = self._get_line()
        line4 = self._get_line()

        self.classedImageLayout.addWidget(line1, 0, 1, 2, 1)
        self.classedImageLayout.addWidget(line2, 0, 3, 2, 1)
        self.classedImageLayout.addWidget(line3, 0, 5, 2, 1)
        self.classedImageLayout.addWidget(line4, 0, 7, 2, 1)

        self.classedImageScrollBar = QScrollBar(Qt.Vertical)
        self.classedImageScrollBar.valueChanged.connect(self.classedscrollchanged)
        self.classedImageScrollBar.setRange(0, 0)

        self.classedImageLayout.addWidget(self.classedImageScrollBar,1,9,1,1)

        self.classGroupBox.setLayout(self.classedImageLayout)

    def createCtrlLayout(self):
        self.ctrlGroupBox = QGroupBox("File Controller")
        layout = QGridLayout()

        self.button_load = QPushButton('Image Load')
        self.button_cnn_model_load = QPushButton('CNN model Load')
        self.button_prev = QPushButton('<<')
        self.button_next = QPushButton('>>')
        self.button_done = QPushButton('Done')
        self.button_learning = QPushButton('Learning')
        self.button_gray_learning = QPushButton('gray_learning')
        self.button_edge_learning = QPushButton('edge_learning')
        #self.button_classify = QPushButton('classify result')

        layout.addWidget(self.button_cnn_model_load, 0,0)
        layout.addWidget(self.button_learning, 0,2)
        layout.addWidget(self.button_gray_learning, 0,3)
        layout.addWidget(self.button_edge_learning, 0,4)
        layout.addWidget(self.button_load, 1,0)
        layout.addWidget(self.button_prev, 1,1)
        layout.addWidget(self.button_next, 1,2)
        layout.addWidget(self.button_done, 1,3)

        #layout.addWidget(self.button_classify, 0,4)
        self.button_cnn_model_load.clicked.connect(self.LoadCNNModel)
        self.button_load.clicked.connect(self.getfiles)
        self.button_prev.clicked.connect(self.preView)
        self.button_next.clicked.connect(self.nextView)
        self.button_done.clicked.connect(self.doneButton)
        self.button_learning.clicked.connect(self.learningButton)
        self.button_gray_learning.clicked.connect(self.graylearningButton)
        #self.button_classify.clicked.connect(self.on_classyfyButton_clicked)
        self.button_edge_learning.clicked.connect(self.edgelearningButton)

        layout2 = QGridLayout()
        self.checkbox_Class = []
        self.checkbox_Class.append(QCheckBox("All",self))
        self.checkbox_Class.append(QCheckBox("unclassified",self))
        self.checkbox_Class.append(QCheckBox("class1",self))
        self.checkbox_Class.append(QCheckBox("class2",self))
        self.checkbox_Class.append(QCheckBox("class3",self))
        self.checkbox_Class.append(QCheckBox("class4",self))
        self.checkbox_Class.append(QCheckBox("class5",self))

        i=-1
        for checkbox in self.checkbox_Class :
            checkbox.setChecked(1)
            checkbox.stateChanged.connect(partial(self.classCheckBoxEvents, i))
            i+=1

        i=0
        for checkbox in self.checkbox_Class :
            layout2.addWidget(checkbox, 0,i)
            i+=1
        self.semiAutoBox = QCheckBox("semi-auto labeling",self)

        layout2.addWidget(self.semiAutoBox, 0, 10)

        layout.addLayout(layout2, 2,0, 1, 4)

        self.ctrlGroupBox.setLayout(layout)

    def createRawImageLayout(self):
        self.rawImageGroupBox = QGroupBox("Raw Image")
        layout = QGridLayout()
        self.label = QLabel()
        self.label.setPixmap(self._image)
        layout.addWidget(self.label,0,0,1,7)

        layout.setAlignment(Qt.AlignTop)

        self.label.mousePressEvent = self.mainImage_mousePressEvent
        self.label.mouseMoveEvent = self.mainImage_mouseMoveEvent
        self.label.mouseReleaseEvent = self.mainImage_mouseReleaseEvent

        self.ImgDetailLayout = QVBoxLayout()
        layout.addLayout(self.ImgDetailLayout, 0,7,1,3 )

        self.entropySlider = QSlider(Qt.Horizontal)
        self.entropySlider.setMinimum(0)
        self.entropySlider.setMaximum(100)
        self.entropySlider.setValue(10)
        self.entropySlider.setTickInterval(10)
        self.entropySlider.setSingleStep(5)
        self.entropySlider.setTickPosition(QSlider.TicksBelow)

        self.entropySliderLayout = QVBoxLayout()
        self.entropySliderLabel = QLabel("minimum entropy : 0.1")
        self.entropySliderLabel.setAlignment(Qt.AlignLeft)
        self.entropySliderLayout.addWidget(self.entropySliderLabel)
        self.entropySliderLayout.addWidget(self.entropySlider)
        self.minEntropy = 0.1

        self.ImgDetailLayout.addLayout(self.entropySliderLayout)

        self.buttonSize32 = QPushButton('GridSize : 32')
        self.buttonSize64 = QPushButton('GridSize : 64')
        self.buttonSize128 = QPushButton('GridSize : 128')
        self.buttonSize256 = QPushButton('GridSize : 256')
        self.buttonSize512 = QPushButton('GridSize : 512')

        self.ImgDetailLayout.addWidget(self.buttonSize32)
        self.ImgDetailLayout.addWidget(self.buttonSize64)
        self.ImgDetailLayout.addWidget(self.buttonSize128)
        self.ImgDetailLayout.addWidget(self.buttonSize256)
        self.ImgDetailLayout.addWidget(self.buttonSize512)

        self.info = QLabel()
        self.info.setText('Image Info : None ')

        self.info2 = QLabel()
        self.info2.setText('gridSize : %d' %(self.currentGridSize))

        self.info3 = QLabel()
        self.info3.setText('')

        self.ImgDetailLayout.addWidget(self.info)
        self.ImgDetailLayout.addWidget(self.info2)
        self.ImgDetailLayout.addWidget(self.info3)

        self.ImgDetailLayout.setAlignment(Qt.AlignTop)

        self.buttonSize32.clicked.connect(partial(self.refresh_GridSize, 32))
        self.buttonSize64.clicked.connect(partial(self.refresh_GridSize, 64))
        self.buttonSize128.clicked.connect(partial(self.refresh_GridSize, 128))
        self.buttonSize256.clicked.connect(partial(self.refresh_GridSize, 256))
        self.buttonSize512.clicked.connect(partial(self.refresh_GridSize, 512))
        self.entropySlider.valueChanged.connect(self.entropySliderValueChange)

        self.rawImageGroupBox.setLayout(layout)

    def createSelectImageLayout(self):
        self.selectImageGroupBox = QGroupBox("Selected Image")
        self.scroll_layout = QVBoxLayout()
        self.selectedImageLayout = QHBoxLayout()

        NullImg64 = QPixmap(64,64)
        NullImg64.fill(QColor(240,240,240))
        temp = QLabel()
        temp.setPixmap(NullImg64)
        self.selectedImageLayout.addWidget(temp)

        self.selectedImageScrollBar = QScrollBar(Qt.Horizontal)
        self.selectedImageScrollBar.valueChanged.connect(self.selectedscrollchanged)
        self.selectedImageScrollBar.setRange(0, 0)

        self.selectedImageLayout.setAlignment(Qt.AlignLeft)

        self.scroll_layout.addLayout(self.selectedImageLayout)
        self.scroll_layout.addWidget(self.selectedImageScrollBar)
        self.selectImageGroupBox.setLayout(self.scroll_layout)

    '''Events functions'''
    def classCheckBoxEvents(self, index, state) :
        if index == -1 : #All
            if state == Qt.Checked:
                for checkbox in self.checkbox_Class :
                    checkbox.setChecked(1)
            else :
                for checkbox in self.checkbox_Class :
                    checkbox.setChecked(0)

        else :
            if state == Qt.Checked:
                self.flagViewClass[index] = True
            else :
                self.flagViewClass[index] = False

        self.re_draw_rawImageRect()
        #print('index[%d] : %s' % (index, 'true' if self.flagViewClass[index] else 'false'))

    def LoadCNNModel(self) :
        '''
        file_path,_=QFileDialog.getOpenFileName(self,'Fileload','./','CNN model Files(*.h5)')
        if not os.path.exists(file_path):
            return
        self.modelFileName=file_path
        print("CNN model file loaded : \n%s" % (self.modelFileName) )
        '''
    def getfiles(self) :
        self.foldername = QFileDialog.getExistingDirectory(self, 'Select directory')

        print(self.foldername )
        self.file_list = os.listdir(self.foldername)
        self.file_list.sort()

        if self.file_list :
            self.fileIdx = 0
        else :
            QMessageBox.about(self, "Image Directory", "folder is empty!")
            return
        self.imgToUI()

    def selectedscrollchanged(self, value) :
        self.selectedImageScrollBarIndex = value
        self.re_draw_subImageWidget()

    def classedscrollchanged(self,value) :
        self.classedImageScrollBarIndex = value
        self.re_draw_classWidget()

    def preView(self) :
        self.fileIdx = self.fileIdx - 1
        if self.fileIdx < 0 :
            self.fileIdx = 0
            QMessageBox.about(self, "Previous Image", "This is First Image!")
        else :
            self.imgToUI()

    def nextView(self) :
        self.fileIdx = self.fileIdx + 1
        if self.fileIdx >= len(self.file_list) :
            self.fileIdx = self.fileIdx - 1
            QMessageBox.about(self, "Next Image", "This is Final Image!")
        else :
            self.imgToUI()

    def doneButton(self) :
        self.fileIdx = self.fileIdx
        self.saveImageClassToFile()
        print(self.current_filepath)
        shutil.move(self.current_filepath, '%s/done' %(self.foldername))

    def learningButton(self) :
        from learning_test2 import Learning
        #deep learning model reversion
        print('learning model START')
        Learning.gray_learning()
        print('learning model END')

    def edgelearningButton(self) :
        from learning_test2 import Learning
        Learning.canny_edge_learning()

    def graylearningButton(self) :
        from learning_test2 import Learning
        Learning.gray_learning()

    def on_classyfyButton_clicked(self) :
        #print(self.subImages)
        self.classifyWindow = CurrentClassViewWindow(self)
        self.classifyWindow.setClassSubImages(self.subImages)
        self.classifyWindow.exec_()

    def refresh_GridSize(self, gridsize) :
        self.currentGridSize = gridsize
        self.subImages.deleteAllSelectedIdx()
        self.subImages.makeWorkingList(self.currentGridSize, self.minEntropy)
        self.re_draw_rawImageRect()
        self.re_draw_subImageWidget()
        self.re_draw_classWidget()
        self.update()

    def entropySliderValueChange(self):
        value = self.entropySlider.value()
        self.minEntropy = value/10
        self.entropySliderLabel.setText('minimum entropy : %.1f'%(value/10))
        self.subImages.deleteAllSelectedIdx()
        self.subImages.makeWorkingList(self.currentGridSize, self.minEntropy)
        self.re_draw_rawImageRect()
        self.re_draw_subImageWidget()
        self.re_draw_classWidget()

    def mouseMoveEvent(self, event):
        self.info2.setText('gridSize : %d\nglobalPos : [%d,%d]\nmousePosition : [%d,%d]' %(self.currentGridSize, event.x(), event.y(),event.globalX(), event.globalY()))

    def mainImage_mousePressEvent(self, event):
        if event.button() == 1 :
            print('mouse button1 pressed')
            self.flagSelecting_Button1  = True
        elif event.button() == 2 :
            print('mouse button2 pressed')
            self.flagSelecting_Button2  = True

        if self.flagSelecting_Button1 == True :
            self.selectedIdx = []
            self.subImages.deleteAllSelectedIdx()
            self.ImageSelection(event)
        elif self.flagSelecting_Button2 == True :
             self.ImageUnclassification(event)

    def mainImage_mouseMoveEvent(self, event):
        if self.flagSelecting_Button1 == True :
            self.ImageSelection(event)
        elif self.flagSelecting_Button2 == True :
            self.ImageUnclassification(event)

    def ImageUnclassification(self,event):
        point = ImgProc.calcMousePosToOriginalPixelPos(self._image_originSize[0], self._image_originSize[1], event.x(), event.y(), 700)

        idx = self.subImages.classIdxCheck(point)

        for i in idx :
            self.subImages.classNum[i] = 0

        self.selectImage_length = self.subImages.getSelectedIndexLength()
        scrollMax = 0 if self.selectImage_length<13 else self.selectImage_length-13
        self.selectedImageScrollBar.setRange(0, scrollMax)
        selectedImageScrollBarIndex = 0

        text = 'mainImageEventPos : [%d, %d]\ncalculatedPos : [%d, %d]' % (event.x(), event.y() , point[0], point[1] )
        self.info3.setText(text)

        self.re_draw_rawImageRect()
        self.re_draw_subImageWidget()


    def ImageSelection(self,event):
        point = ImgProc.calcMousePosToOriginalPixelPos(self._image_originSize[0], self._image_originSize[1], event.x(), event.y(), 700)

        idx = self.subImages.selectIdxCheck(point)

        for i in idx :
            self.subImages.addSelectedIdx(i)

        self.selectImage_length = self.subImages.getSelectedIndexLength()
        scrollMax = 0 if self.selectImage_length<13 else self.selectImage_length-13
        self.selectedImageScrollBar.setRange(0, scrollMax)
        selectedImageScrollBarIndex = 0

        text = 'mainImageEventPos : [%d, %d]\ncalculatedPos : [%d, %d]' % (event.x(), event.y() , point[0], point[1] )
        self.info3.setText(text)

        self.re_draw_rawImageRect()
        self.re_draw_subImageWidget()

    def mainImage_mouseReleaseEvent(self, event):
        self.flagSelecting_Button1 = False
        self.flagSelecting_Button2 = False

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_1: self.saveSelectedImage(1)
        if e.key() == Qt.Key_2: self.saveSelectedImage(2)
        if e.key() == Qt.Key_3: self.saveSelectedImage(3)
        if e.key() == Qt.Key_4: self.saveSelectedImage(4)
        if e.key() == Qt.Key_5: self.saveSelectedImage(5)
        if e.key() == Qt.Key_Q: self._unclassImage(1)
        if e.key() == Qt.Key_W: self._unclassImage(2)
        if e.key() == Qt.Key_E: self._unclassImage(3)
        if e.key() == Qt.Key_R: self._unclassImage(4)
        if e.key() == Qt.Key_T: self._unclassImage(5)

    def saveSelectedImage(self, classNumber) :
        self.subImages.classifySelectedImage(classNumber)
        self.re_draw_rawImageRect()
        self.re_draw_subImageWidget()
        self.re_draw_classWidget()

    def _unclassImage(self, classNumber) :
        self.subImages.unclassImage(classNumber)

        self.re_draw_rawImageRect()
        self.re_draw_subImageWidget()
        self.re_draw_classWidget()

    def saveImageClassToFile(self) :
        self.subImages.saveClassImage(1)


    '''User Functions'''
    def imgToUI(self) :
        #from keras.models import load_model
        #from predict_img import Predict

        self.subImglist = []
        self.subPos = []
        self.classNum = []

        self.current_filepath = '%s/%s' %(self.foldername, self.file_list[self.fileIdx])

        CvImg = cv2.imread( self.current_filepath , cv2.IMREAD_COLOR)

        self._image_originSize = [CvImg.shape[1], CvImg.shape[0]]

        self._image = ImgProc.CvImgToQPixmap(CvImg)
        self.subImglist, self.subPos, self.subEntropy =ImgProc.getSubImg(CvImg)

        self.subImages = SubImageControl()
        self.subImages._ToUpdate.connect(self._updateWidgets)


        # img predict process
        start = time.time()
        '''
        if self.semiAutoBox.isChecked() :
            if self.modelFileName == "" :
                _model = load_model('pyTest_model.h5')
            else :
                _model = load_model(self.modelFileName)
            print('read model for predict')

            # classnum 할당
            for i in self.subImglist :
                #self.classNum.append(random.randint(0, 5))
                _classnum = Predict.predict_classnum(i, _model)
                self.classNum.append(_classnum)

            print("img predict time: ", (time.time() - start), 'sec')
            print("img predict time: ", int(int((time.time() - start)/60)/60), ':',
                  int((time.time() - start)/60)%60, ':', int(time.time() - start)%60)
        else :
            for i in self.subImglist :
                self.classNum.append(0)
        '''
        for i in self.subImglist :
            self.classNum.append(0)

        for i in range(len(self.subImglist)) :
            self.subImages.setSubImage(self.subImglist[i], self.subPos[i], self.subEntropy[i], self.file_list[self.fileIdx], self.classNum[i])
        self.subImages.genLabels()

        self.info.setText('[Image Info]\nFilename : %s \nSize : [%d X %d]' %(self.file_list[self.fileIdx], self._image_originSize[0], self._image_originSize[1]))
        self.info2.setText('')
        self.load_rawImageWidget()
        self.load_subImageWidget()
        self.re_draw_classWidget()

        #del _model

    def re_draw_rawImageRect(self) :
        if self.subPos :
            CvImg = cv2.imread( self.current_filepath , cv2.IMREAD_COLOR)
            self._image = ImgProc.CvImgToQPixmap(CvImg)

            painter = QPainter(self._image)
            pen = QPen()
            painter.setRenderHint(QPainter.Antialiasing, True)

            self.drawRectOnRawImage(painter, pen)

            ###selected images
            pen.setWidth(6)
            pen.setColor(QColor(255,255,255))
            painter.setPen(pen)
            if len(self.subImages.selectedIdx) > 0  :
                for idx in self.subImages.selectedIdx :
                    painter.drawRect(self.subImages.positions[idx][0], self.subImages.positions[idx][1], self.subImages.positions[idx][2], self.subImages.positions[idx][3])

            pen.setWidth(3)
            pen.setColor(QColor(200,200,200))
            painter.setPen(pen)
            if len(self.subImages.selectedIdx) > 0  :
                for idx in self.subImages.selectedIdx :
                    painter.drawRect(self.subImages.positions[idx][0], self.subImages.positions[idx][1], self.subImages.positions[idx][2], self.subImages.positions[idx][3])

            painter.end()

            self._image = self._image.scaled(700,700, Qt.KeepAspectRatio)
            self.label.setPixmap(self._image)
            self.update()

    def load_rawImageWidget(self) :
        if self.subPos :
            CvImg = cv2.imread( self.current_filepath , cv2.IMREAD_COLOR)
            self._image = ImgProc.CvImgToQPixmap(CvImg)

            painter = QPainter(self._image)
            pen = QPen()
            painter.setRenderHint(QPainter.Antialiasing, True)

            self.subImages.makeWorkingList(self.currentGridSize, self.minEntropy)

            self.drawRectOnRawImage(painter, pen)

            painter.end()

            self._image = self._image.scaled(700,700, Qt.KeepAspectRatio)
            self.label.setPixmap(self._image)
            self.update()

    def re_draw_subImageWidget(self) :
        if self.subPos :
            UIuserFunction.clearLayout(self.selectedImageLayout)
            #print(self.subImages.selectedIdx)

            self.subImages.connectSelectedLabelToLayout(self.selectedImageLayout, self.selectedImageScrollBarIndex, self.selectedImageScrollBarIndex+13)
            self.update()

    def load_subImageWidget(self) :
        if self.subPos :
            UIuserFunction.deleteLayout(self.selectedImageLayout)
            self.selectImage_length = 0
            self.selectedImageScrollBar.setRange(0, 0)
            self.update()

    def re_draw_classWidget(self) :
        UIuserFunction.clearLayout(self.class1Layout)
        UIuserFunction.clearLayout(self.class2Layout)
        UIuserFunction.clearLayout(self.class3Layout)
        UIuserFunction.clearLayout(self.class4Layout)
        UIuserFunction.clearLayout(self.class5Layout)
        Max = 0
        length = self.subImages.connectAllLabelsToLayoutWithClass(self.class1Layout, 1, self.classedImageScrollBarIndex, self.classedImageScrollBarIndex+13)
        if length > Max : Max = length
        length = self.subImages.connectAllLabelsToLayoutWithClass(self.class2Layout, 2, self.classedImageScrollBarIndex, self.classedImageScrollBarIndex+13)
        if length > Max : Max = length
        length = self.subImages.connectAllLabelsToLayoutWithClass(self.class3Layout, 3, self.classedImageScrollBarIndex, self.classedImageScrollBarIndex+13)
        if length > Max : Max = length
        length = self.subImages.connectAllLabelsToLayoutWithClass(self.class4Layout, 4, self.classedImageScrollBarIndex, self.classedImageScrollBarIndex+13)
        if length > Max : Max = length
        length = self.subImages.connectAllLabelsToLayoutWithClass(self.class5Layout, 5, self.classedImageScrollBarIndex, self.classedImageScrollBarIndex+13)
        if length > Max : Max = length

        scrollMax = 0 if Max<13 else Max-13
        self.classedImageScrollBar.setRange(0, scrollMax)

        self.class1Layout.addStretch()
        self.class2Layout.addStretch()
        self.class3Layout.addStretch()
        self.class4Layout.addStretch()
        self.class5Layout.addStretch()

        self.update()

    def drawRectOnRawImage(self, painter, pen) :
        if self.flagViewClass[0] :
            c0_poslist = self.subImages.getImagePosWithClass(0)

            pen.setWidth(6)
            pen.setColor(QColor(255,255,255))
            painter.setPen(pen)
            for pos in c0_poslist :
                painter.drawRect(pos[0], pos[1], pos[2], pos[3])

            pen.setWidth(3)
            pen.setColor(QColor(255,0,0))
            painter.setPen(pen)
            for pos in c0_poslist :
                painter.drawRect(pos[0], pos[1], pos[2], pos[3])

        if self.flagViewClass[1] :
            c1_poslist = self.subImages.getImagePosWithClass(1)

            pen.setWidth(6)
            pen.setColor(QColor(255,255,255))
            painter.setPen(pen)
            for pos in c1_poslist :
                painter.drawRect(pos[0], pos[1], pos[2], pos[3])

            pen.setWidth(3)
            pen.setColor(QColor(200,100,0))
            painter.setPen(pen)
            for pos in c1_poslist :
                painter.drawRect(pos[0], pos[1], pos[2], pos[3])

        if self.flagViewClass[2] :
            c2_poslist = self.subImages.getImagePosWithClass(2)
            pen.setWidth(6)
            pen.setColor(QColor(255,255,255))
            painter.setPen(pen)
            for pos in c2_poslist :
                painter.drawRect(pos[0], pos[1], pos[2], pos[3])

            pen.setWidth(3)
            pen.setColor(QColor(100,200,0))
            painter.setPen(pen)
            for pos in c2_poslist :
                painter.drawRect(pos[0], pos[1], pos[2], pos[3])

        if self.flagViewClass[3] :
            c3_poslist = self.subImages.getImagePosWithClass(3)

            pen.setWidth(6)
            pen.setColor(QColor(255,255,255))
            painter.setPen(pen)
            for pos in c3_poslist :
                painter.drawRect(pos[0], pos[1], pos[2], pos[3])

            pen.setWidth(3)
            pen.setColor(QColor(50,100,150))
            painter.setPen(pen)
            for pos in c3_poslist :
                painter.drawRect(pos[0], pos[1], pos[2], pos[3])

        if self.flagViewClass[4] :
            c4_poslist = self.subImages.getImagePosWithClass(4)

            pen.setWidth(6)
            pen.setColor(QColor(255,255,255))
            painter.setPen(pen)
            for pos in c4_poslist :
                painter.drawRect(pos[0], pos[1], pos[2], pos[3])

            pen.setWidth(3)
            pen.setColor(QColor(100,100,100))
            painter.setPen(pen)
            for pos in c4_poslist :
                painter.drawRect(pos[0], pos[1], pos[2], pos[3])

        if self.flagViewClass[5] :
            c5_poslist = self.subImages.getImagePosWithClass(5)

            pen.setWidth(6)
            pen.setColor(QColor(255,255,255))
            painter.setPen(pen)
            for pos in c5_poslist :
                painter.drawRect(pos[0], pos[1], pos[2], pos[3])

            pen.setWidth(3)
            pen.setColor(QColor(100,50,150))
            painter.setPen(pen)
            for pos in c5_poslist :
                painter.drawRect(pos[0], pos[1], pos[2], pos[3])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
