import sys
import os
import cv2
import numpy as np
import math
import random
import copy
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from functools import partial
from numpy import unique
from scipy.stats import entropy as scipy_entropy
from math import log, e

from imgproc import ImgProc


class SubImageControl(QObject) :
    _ToUpdate = pyqtSignal(int)
    def __init__(self, parent = None):
        super(SubImageControl,self).__init__(parent)
        self.classNum = []
        self.Images = []
        self.labels = []
        self.workingLabelIndexes = []
        self.qpixmaps = []
        self.positions = []
        self.selectedIdx = []
        self.indexs = []
        self.subEntropy = []
        self.originfilename = []

    def subImageMousePressEvent(self, i, event) :
        self.classNum[i] = 0
        for idx in range(len(self.selectedIdx)) :
            if self.selectedIdx[idx] == i:
                del self.selectedIdx[idx]
                break
        self._ToUpdate.emit(i)

    def setSubImage(self, Image, position, entropy, filelabel,__classNum) :
        self.classNum.append(__classNum)
        self.Images.append(Image)
        temp = ImgProc.CvImgToQPixmap(Image)
        temp = temp.scaled(64,64, Qt.KeepAspectRatio)
        self.qpixmaps.append(temp)
        self.positions.append(position)
        self.subEntropy.append(entropy)
        self.originfilename.append(filelabel)

    def makeWorkingList(self, size, entropy) :
        self.workingLabelIndexes = []
        for i in range(len(self.labels)) :
            if self.positions[i][2] == size :
                if self.subEntropy[i] > entropy :
                    self.workingLabelIndexes.append(i)
    def saveClassImage(self, classNum) :
        for index in range(len(self.classNum)) :
            if self.classNum[index] == 0 :
                continue
            tempfilename = '%s_%d_%d_%d_%d_%d.png' % (self.originfilename[index], self.classNum[index], self.positions[index][0], self.positions[index][1],self.positions[index][2],self.positions[index][3])
            ImgProc.SaveSubImg(tempfilename, self.Images[index], self.classNum[index])


    def getImagePos(self) :
        pos = []
        for i in range(len(self.workingLabelIndexes)) :
            pos.append(self.positions[self.workingLabelIndexes[i]])
        return pos

    def getImagePosWithClass(self, _classNum) :
        pos = []
        for i in range(len(self.workingLabelIndexes)) :
            if self.classNum[self.workingLabelIndexes[i]]==_classNum :
                pos.append(self.positions[self.workingLabelIndexes[i]])
        return pos

    def getWorkingLabelsWithClass(self, _classNum) :
        labels = []
        for i in range(len(self.workingLabelIndexes)) :
            if self.classNum[self.workingLabelIndexes[i]]==_classNum :
                labels.append(self.labels[self.workingLabelIndexes[i]])
        return labels

    def getAllLabelsWithClass(self, _classNum) :
        labels = []
        for i in range(len(self.labels)) :
            if self.classNum[i]==_classNum :
                labels.append(self.labels[i])
        return labels

    def connectAllLabelsToLayoutWithClass(self, layout, _classNum, startIdx, endIdx) :
        labels = self.getAllLabelsWithClass(_classNum)
        index = startIdx
        for i in range(len(labels)) :
            if index >= len(labels) : break
            elif index >= endIdx : break
            else :
                layout.addWidget(labels[index])
            index+=1
        return len(labels)

    def genLabels(self) :
        self.labels = []
        for i in range(len(self.classNum)) :
            temp = QLabel()
            temp.setPixmap(self.qpixmaps[i])

            temp.mousePressEvent = partial(self.subImageMousePressEvent, i)
            self.labels.append(temp)

    def connectToLayout(self, layout, index) :
        if len(self.labels) < index or index < 0 :
            return
        else :
            if self.classNum[index] == 0 :
                layout.addWidget(self.labels[index])

    def connectSelectedLabelToLayout(self, layout, startIdx, endIdx) :
        if len(self.selectedIdx)==0 :
            NullImg64 = QPixmap(64,64)
            NullImg64.fill(QColor(240,240,240))
            temp = QLabel()
            temp.setPixmap(NullImg64)
            layout.addWidget(temp)
        else :
            for i in range(len(self.selectedIdx)) :
                if (i+startIdx) >= endIdx : break
                elif (i+startIdx) >= len(self.selectedIdx) :  break
                self.connectToLayout(layout, self.selectedIdx[i+startIdx])

    def getSelectedIndexLength(self) :
        return len(self.selectedIdx)

    def addSelectedIdx(self, idx) :
        self.selectedIdx.append(idx)
        self.selectedIdx = list(set(self.selectedIdx))
        self.selectedIdx = sorted(self.selectedIdx)

    def removeSelectedIdx(self, idx) :
        for i in range(len(self.selectedIdx)) :
            if self.selectedIdx[i] == idx :
                del self.selectedIdx[i]
                break

    def deleteAllSelectedIdx(self) :
        self.selectedIdx=[]

    def selectIdxCheck(self, point) :
        indexlist = []
        #print('indexcheck start')
        for i in range(len(self.workingLabelIndexes)) :
            if self.classNum[self.workingLabelIndexes[i]] ==0 :
                x1 = self.positions[self.workingLabelIndexes[i]][0]
                x2 = self.positions[self.workingLabelIndexes[i]][0]+self.positions[self.workingLabelIndexes[i]][2]
                y1 = self.positions[self.workingLabelIndexes[i]][1]
                y2 = self.positions[self.workingLabelIndexes[i]][1]+self.positions[self.workingLabelIndexes[i]][3]

                if  x1 <=  point[0]  and x2 >= point[0] :
                    if  y1 <=  point[1]  and y2 >= point[1] :
                        indexlist.append(self.workingLabelIndexes[i])
                        #print('[%d](%d,%d,%d,%d), point[%d,%d]' %(self.workingLabelIndexes[i], x1,x2,y1,y2, point[0], point[1]))
        #print('indexcheck done')

        return indexlist

    def classIdxCheck(self, point) :
        indexlist = []
        #print('indexcheck start')
        for i in range(len(self.workingLabelIndexes)) :
            if self.classNum[self.workingLabelIndexes[i]] !=0 :
                x1 = self.positions[self.workingLabelIndexes[i]][0]
                x2 = self.positions[self.workingLabelIndexes[i]][0]+self.positions[self.workingLabelIndexes[i]][2]
                y1 = self.positions[self.workingLabelIndexes[i]][1]
                y2 = self.positions[self.workingLabelIndexes[i]][1]+self.positions[self.workingLabelIndexes[i]][3]

                if  x1 <=  point[0]  and x2 >= point[0] :
                    if  y1 <=  point[1]  and y2 >= point[1] :
                        indexlist.append(self.workingLabelIndexes[i])
                        #print('[%d](%d,%d,%d,%d), point[%d,%d]' %(self.workingLabelIndexes[i], x1,x2,y1,y2, point[0], point[1]))
        #print('indexcheck done')

        return indexlist

    def classifySelectedImage(self, _classNum) :
        for i in self.selectedIdx :
            self.classNum[i] = _classNum
        self.selectedIdx=[]

    def unclassImage(self, _classNum) :
        for i in range(len(self.classNum)) :
            if self.classNum[i] == _classNum :
                self.classNum[i] = 0
