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

class ImgProc():
    def Init() :
        ImgProc.makeClassifiedDir()

    def CvImgToQPixmap(CvImg) :
        img = cv2.cvtColor(CvImg, cv2.COLOR_BGR2RGB)
        img_h = img.shape[0]
        img_w = img.shape[1]
        size = img.size

        ratio_x = 700
        ratio_y = int(700*img_h/img_w)

        ratio_img = cv2.resize(img, (ratio_x,ratio_y), interpolation=cv2.INTER_CUBIC)

        return QPixmap.fromImage(QImage(ratio_img.data,ratio_x,ratio_y, QImage.Format_RGB888))

    def ImgObjTest(Img) :
        orb = cv2.ORB_create()
        Img2 = cv2.resize(Img, (128,128), interpolation=cv2.INTER_LINEAR )
        kp1, des1 = orb.detectAndCompute(Img2,None)

        if (len(kp1) > 0) :
            return True
        return False

    def shannon_entropy(image, base=e) :
        _, counts = unique(image, return_counts=True)
        return scipy_entropy(counts, base=base)

    def makedirectory(path) :
        if not(os.path.isdir(path)):
            os.makedirs(os.path.join(path))
    def makeClassifiedDir() :
        ImgProc.makedirectory('D:/SVN/vis_research/deepStyleVolumeRendering/imgs/bonsai/classified/img_type2_check')
        ImgProc.makedirectory('D:/SVN/vis_research/deepStyleVolumeRendering/imgs/bonsai/classified/img_type2_check/1')
        ImgProc.makedirectory('D:/SVN/vis_research/deepStyleVolumeRendering/imgs/bonsai/classified/img_type2_check/2')
        ImgProc.makedirectory('D:/SVN/vis_research/deepStyleVolumeRendering/imgs/bonsai/classified/img_type2_check/3')
        ImgProc.makedirectory('D:/SVN/vis_research/deepStyleVolumeRendering/imgs/bonsai/classified/img_type2_check/4')
        ImgProc.makedirectory('D:/SVN/vis_research/deepStyleVolumeRendering/imgs/bonsai/classified/img_type2_check/5')

    def SaveSubImg(filename, CvImg, classNum) :
        path = 'D:/SVN/vis_research/deepStyleVolumeRendering/imgs/bonsai/classified/img_type2_check/'
        path += str(classNum)
        path += '/'
        path += filename
        #print(path)
        print(path)
        cv2.imwrite(path, CvImg)




    def getSubImg(CvImg) :
        img_h = CvImg.shape[0]
        img_w = CvImg.shape[1]
        sizearray = [32,64,128]
        subImglist=[]
        subImgPos=[]
        subImgEntropy = []

        ratio_x = 700
        ratio_y = int(700*img_h/img_w)

        ratio_img = cv2.resize(CvImg, (ratio_x,ratio_y), interpolation=cv2.INTER_CUBIC)
        ratio_img_h = ratio_img.shape[0]
        ratio_img_w = ratio_img.shape[1]

        for gridsize in sizearray :
            if ratio_img_w > gridsize and ratio_img_h > gridsize :
                # crop 할 사이즈 : grid_w, grid_h
                grid_w = gridsize # crop width
                grid_h = gridsize # crop height
                range_w = int(ratio_img_w/grid_w)
                range_h = int(ratio_img_h/grid_h)

                i = 0
                for w in range(range_w):
                    for h in range(range_h):
                        if ( int((h+1)*grid_h) <=ratio_img_h and int((w+1)*(grid_w))<=ratio_img_w ) :
                            if (1) :
                                crop_img = ratio_img[ int(h*grid_h) : int((h+1)*(grid_h)), int(w*grid_w) : int((w+1)*(grid_w)) ]
                                if ImgProc.ImgObjTest(crop_img)==True :
                                    subImglist.append(crop_img)
                                    entropy = ImgProc.shannon_entropy(crop_img)
                                    subImgEntropy.append(entropy)
                                    subImgPos.append([(w*grid_w), (h*grid_h), grid_w, grid_h])
                            if ( int(w*grid_w+(grid_w/2))<= ratio_img_w) :
                                crop_img = ratio_img[ int(h*grid_h) : int((h+1)*(grid_h)) , int(w*grid_w+(grid_w/2)) : int((w+1)*(grid_w)+(grid_w/2)) ]
                                if ImgProc.ImgObjTest(crop_img)==True :
                                    subImglist.append(crop_img)
                                    entropy = ImgProc.shannon_entropy(crop_img)
                                    subImgEntropy.append(entropy)
                                    subImgPos.append([(w*grid_w+(grid_w/2)), (h*grid_h), grid_w, grid_h])
                            if( int(h*grid_h+(grid_h/2)) <= ratio_img_h  ) :
                                crop_img = ratio_img[ int(h*grid_h+(grid_h/2)) : int((h+1)*(grid_h)+(grid_h/2)) , int(w*grid_w) : int((w+1)*(grid_w)) ]
                                if ImgProc.ImgObjTest(crop_img)==True :
                                    subImglist.append(crop_img)
                                    entropy = ImgProc.shannon_entropy(crop_img)
                                    subImgEntropy.append(entropy)
                                    subImgPos.append([(w*grid_w), int(h*grid_h+(grid_h/2)), grid_w, grid_h])
                            if(int((w*grid_w+(grid_w/2)) <= ratio_img_w ) and int((h*grid_h+(grid_h/2)) <= ratio_img_h)) :
                                crop_img = ratio_img[ int(h*grid_h+(grid_h/2)) : int((h+1)*(grid_h)+(grid_h/2)), int(w*grid_w+(grid_w/2)) : int((w+1)*(grid_w)+(grid_w/2)) ]
                                if ImgProc.ImgObjTest(crop_img)==True :
                                    subImglist.append(crop_img)
                                    entropy = ImgProc.shannon_entropy(crop_img)
                                    subImgEntropy.append(entropy)
                                    subImgPos.append([(w*grid_w+(grid_w/2)), int(h*grid_h+(grid_h/2)), grid_w, grid_h])

        return subImglist, subImgPos, subImgEntropy

    def calcMousePosToOriginalPixelPos(originalWidth, originalHeight, px, py, transMaxSize) :

        ratio_x = 700
        ratio_y = int(700*originalHeight/originalWidth)

        if originalWidth > originalHeight :
            val = (ratio_x / transMaxSize )
        else :
            val = (ratio_y / transMaxSize )

        point = [ px*val,  py*val]
        return point
