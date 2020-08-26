#-------------------------------------------------------------------------------
# Name:        pySaliencyMap
# Purpose:     Extracting a saliency map from a single still image
#
# Author:      Akisato Kimura <akisato@ieee.org>
#
# Created:     April 24, 2014
# Copyright:   (c) Akisato Kimura 2014-
# Licence:     All rights reserved
#-------------------------------------------------------------------------------

import cv2
import numpy as np
import pySaliencyMapDefs
import matplotlib.pyplot as plt

class pySaliencyMap:
    # initialization
    def __init__(self, width, height):
        self.width  = width
        self.height = height
        self.prev_frame = None
        self.SM = None
        #self.GaborKernel0   = np.array(pySaliencyMapDefs.GaborKernel_0)
        #self.GaborKernel45  = np.array(pySaliencyMapDefs.GaborKernel_45)
        #self.GaborKernel90  = np.array(pySaliencyMapDefs.GaborKernel_90)
        #self.GaborKernel135 = np.array(pySaliencyMapDefs.GaborKernel_135)

        # cv2.getGaborKernel(ksize, sigma, theta, lambda, gamma, psi, ktype)
        # ksize - size of gabor filter (n, n)
        # sigma - standard deviation of the gaussian function
        # theta - orientation of the normal to the parallel stripes
        # lambda - wavelength of the sunusoidal factor
        # gamma - spatial aspect ratio
        # psi - phase offset
        # ktype - type and range of values that each pixel in the gabor kernel can hold
        gabor_n = 5
        gabor_sigma = 8.0   #8.0
        gabor_lambda = 10.0 #10.0
        gabor_gamma = 0.5
        self.GaborKernel0   = cv2.getGaborKernel((gabor_n, gabor_n), gabor_sigma, np.pi*0/4, gabor_lambda, gabor_gamma, 0, ktype=cv2.CV_32F)
        self.GaborKernel45  = cv2.getGaborKernel((gabor_n, gabor_n), gabor_sigma, np.pi*1/4, gabor_lambda, gabor_gamma, 0, ktype=cv2.CV_32F)
        self.GaborKernel90  = cv2.getGaborKernel((gabor_n, gabor_n), gabor_sigma, np.pi*2/4, gabor_lambda, gabor_gamma, 0, ktype=cv2.CV_32F)
        self.GaborKernel135 = cv2.getGaborKernel((gabor_n, gabor_n), gabor_sigma, np.pi*3/4, gabor_lambda, gabor_gamma, 0, ktype=cv2.CV_32F)

        #self.GaborKernel30  = cv2.getGaborKernel((gabor_n, gabor_n), gabor_sigma, np.pi*1/6, gabor_lambda, gabor_gamma, 0, ktype=cv2.CV_32F)
        #self.GaborKernel60  = cv2.getGaborKernel((gabor_n, gabor_n), gabor_sigma, np.pi*2/6, gabor_lambda, gabor_gamma, 0, ktype=cv2.CV_32F)
        #self.GaborKernel120 = cv2.getGaborKernel((gabor_n, gabor_n), gabor_sigma, np.pi*4/6, gabor_lambda, gabor_gamma, 0, ktype=cv2.CV_32F)
        #self.GaborKernel150 = cv2.getGaborKernel((gabor_n, gabor_n), gabor_sigma, np.pi*5/6, gabor_lambda, gabor_gamma, 0, ktype=cv2.CV_32F)

    # extracting color channels
    def SMExtractRGBI(self, inputImage):
        # convert scale of array elements
        src = np.float32(inputImage) * 1./255
        # split
        (B, G, R) = cv2.split(src)

        Red = R-((G+B)/2)
        Green = G-((R+B)/2)
        Blue = B-((R+G)/2)
        Yellow = ((R+G)/2)-(abs(R-G)/2)-B
        # extract an intensity image
        #I = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        I = (B+G+R) /3
        
        # return
        return Red, Green, Blue, Yellow, I

    # feature maps
    ## constructing a Gaussian pyramid
    def FMCreateGaussianPyr(self, src):
        dst = list()
        dst.append(src)
        for i in range(1,9):
            nowdst = cv2.pyrDown(dst[i-1])
            dst.append(nowdst)
        return dst
    ## taking center-surround differences
    def FMCenterSurroundDiff(self, GaussianMaps):
        dst = list()
        for s in range(2,5):
            now_size = GaussianMaps[s].shape
            now_size = (now_size[1], now_size[0])  ## (width, height)
            tmp = cv2.resize(GaussianMaps[s+3], now_size, interpolation=cv2.INTER_LINEAR)
            nowdst = cv2.absdiff(GaussianMaps[s], tmp)
            dst.append(nowdst)
            tmp = cv2.resize(GaussianMaps[s+4], now_size, interpolation=cv2.INTER_LINEAR)
            nowdst = cv2.absdiff(GaussianMaps[s], tmp)
            dst.append(nowdst)
        return dst

    def FMCenterSurroundDiff2(self, GaussianMaps, GaussianMaps2):
        dst = list()
        for s in range(2,5):
            now_size = GaussianMaps[s].shape
            now_size = (now_size[1], now_size[0])  ## (width, height)
            tmp = cv2.resize(GaussianMaps2[s+3], now_size, interpolation=cv2.INTER_LINEAR)
            nowdst = cv2.absdiff(GaussianMaps[s], tmp)
            dst.append(nowdst)
            tmp = cv2.resize(GaussianMaps2[s+4], now_size, interpolation=cv2.INTER_LINEAR)
            nowdst = cv2.absdiff(GaussianMaps[s], tmp)
            dst.append(nowdst)
        return dst
    ## constructing a Gaussian pyramid + taking center-surround differences
    def FMGaussianPyrCSD(self, src):
        GaussianMaps = self.FMCreateGaussianPyr(src)
        dst = self.FMCenterSurroundDiff(GaussianMaps)
        return dst

    def FMGaussianPyrCSD2(self, src1, src2):
        GaussianMaps = self.FMCreateGaussianPyr(src1)
        GaussianMaps2 = self.FMCreateGaussianPyr(src2)
        dst = self.FMCenterSurroundDiff2(GaussianMaps, GaussianMaps2)
        return dst
    
    ## intensity feature maps
    def IFMGetFM(self, src):
        dst = self.FMGaussianPyrCSD(src)
        return dst

    def IFMGetFM2(self, src):
        temp = src
        dst = self.FMGaussianPyrCSD(temp)
        return dst
    ## color feature maps
    def CFMGetFM(self, R, G, B, Y):
        # max(R,G,B)
        #tmp1 = cv2.max(R, G)
        #RGBMax = cv2.max(B, tmp1)
        #RGBMax[RGBMax <= 0] = 0.0001    # prevent dividing by 0
        # min(R,G)
        #RGMin = cv2.min(R, G)
        #RGAvg = R+G/2.0
        # RG = (R-G)/max(R,G,B)
        #RG = (R - G) / RGBMax
        RG = R - G
        GR = G - R
        # BY = (B-min(R,G)/max(R,G,B)
        #BY = (B - RGMin) / RGBMax
        #BY = (B - RGAvg) / RGBMax
        BY = B-Y
        YB = Y-B
        
        # clamp nagative values to 0
        #RG[RG < 0] = 0
        #BY[BY < 0] = 0
        # obtain feature maps in the same way as intensity
        RGFM = self.FMGaussianPyrCSD2(RG, GR)
        BYFM = self.FMGaussianPyrCSD2(BY, YB)
        # return
        return RGFM, BYFM
    ## orientation feature maps
    def OFMGetFM(self, src):
        # creating a Gaussian pyramid
        GaussianI = self.FMCreateGaussianPyr(src)
        # convoluting a Gabor filter with an intensity image to extract oriemtation features
        GaborOutput0   = [ np.empty((1,1)), np.empty((1,1)) ]  # dummy data: any kinds of np.array()s are OK
        GaborOutput45  = [ np.empty((1,1)), np.empty((1,1)) ]
        GaborOutput90  = [ np.empty((1,1)), np.empty((1,1)) ]
        GaborOutput135 = [ np.empty((1,1)), np.empty((1,1)) ]
        #GaborOutput30  = [ np.empty((1,1)), np.empty((1,1)) ]
        #GaborOutput60  = [ np.empty((1,1)), np.empty((1,1)) ]
        #GaborOutput120  = [ np.empty((1,1)), np.empty((1,1)) ]
        #GaborOutput150  = [ np.empty((1,1)), np.empty((1,1)) ]

        for j in range(2,9):
            GaborOutput0.append(cv2.filter2D(GaussianI[j], cv2.CV_32F, self.GaborKernel0))
            GaborOutput45.append(cv2.filter2D(GaussianI[j], cv2.CV_32F, self.GaborKernel45))
            GaborOutput90.append(cv2.filter2D(GaussianI[j], cv2.CV_32F, self.GaborKernel90))
            GaborOutput135.append(cv2.filter2D(GaussianI[j], cv2.CV_32F, self.GaborKernel135))
           # GaborOutput30.append(  cv2.filter2D(GaussianI[j], cv2.CV_32F, self.GaborKernel30) )
           # GaborOutput60.append(  cv2.filter2D(GaussianI[j], cv2.CV_32F, self.GaborKernel60) )
           # GaborOutput120.append( cv2.filter2D(GaussianI[j], cv2.CV_32F, self.GaborKernel120) )
           # GaborOutput150.append( cv2.filter2D(GaussianI[j], cv2.CV_32F, self.GaborKernel150) )
        # calculating center-surround differences for every oriantation
        CSD0   = self.FMCenterSurroundDiff(GaborOutput0)
        CSD45  = self.FMCenterSurroundDiff(GaborOutput45)
        CSD90  = self.FMCenterSurroundDiff(GaborOutput90)
        CSD135 = self.FMCenterSurroundDiff(GaborOutput135)
        # CSD30 = self.FMCenterSurroundDiff(GaborOutput30)
        #CSD60 = self.FMCenterSurroundDiff(GaborOutput60)
        # CSD120 = self.FMCenterSurroundDiff(GaborOutput120)
        # CSD150 = self.FMCenterSurroundDiff(GaborOutput150)
        # concatenate for 0,45,90,135
        dst = list(CSD0)
        dst.extend(CSD45)
        dst.extend(CSD90)
        dst.extend(CSD135)

        # concatenate for 0,30,60,120,150
        #dst = list(CSD0)
        #dst.extend(CSD30)
        #dst.extend(CSD60)
        #dst.extend(CSD90)
        #dst.extend(CSD120)
        #dst.extend(CSD150)
        # return
        return dst
    ## motion feature maps
    def MFMGetFM(self, src):
        # convert scale
        I8U = np.uint8(255 * src)
        cv2.waitKey(10)
        # calculating optical flows
        if self.prev_frame is not None:
            farne_pyr_scale= pySaliencyMapDefs.farne_pyr_scale
            farne_levels = pySaliencyMapDefs.farne_levels
            farne_winsize = pySaliencyMapDefs.farne_winsize
            farne_iterations = pySaliencyMapDefs.farne_iterations
            farne_poly_n = pySaliencyMapDefs.farne_poly_n
            farne_poly_sigma = pySaliencyMapDefs.farne_poly_sigma
            farne_flags = pySaliencyMapDefs.farne_flags
            flow = cv2.calcOpticalFlowFarneback(\
                prev = self.prev_frame, \
                next = I8U, \
                pyr_scale = farne_pyr_scale, \
                levels = farne_levels, \
                winsize = farne_winsize, \
                iterations = farne_iterations, \
                poly_n = farne_poly_n, \
                poly_sigma = farne_poly_sigma, \
                flags = farne_flags, \
                flow = None \
            )
            flowx = flow[...,0]
            flowy = flow[...,1]
        else:
            flowx = np.zeros(I8U.shape)
            flowy = np.zeros(I8U.shape)
        # create Gaussian pyramids
        dst_x = self.FMGaussianPyrCSD(flowx)
        dst_y = self.FMGaussianPyrCSD(flowy)
        # update the current frame
        self.prev_frame = np.uint8(I8U)
        # return
        return dst_x, dst_y

    # conspicuity maps
    ## standard range normalization
    def SMRangeNormalize(self, src):
        minn, maxx, dummy1, dummy2 = cv2.minMaxLoc(src)
        if maxx!=minn:
            dst = src/(maxx-minn) + minn/(minn-maxx)
        else:
            dst = src - minn
        return dst
    ## computing an average of local maxima
    def SMAvgLocalMax(self, src):
        # size
        stepsize = pySaliencyMapDefs.default_step_local
        width = src.shape[1]
        height = src.shape[0]
        # find local maxima
        numlocal = 0
        lmaxmean = 0
        for y in range(0, height-stepsize, stepsize):
            for x in range(0, width-stepsize, stepsize):
                localimg = src[y:y+stepsize, x:x+stepsize]
                lmin, lmax, dummy1, dummy2 = cv2.minMaxLoc(localimg)
                lmaxmean += lmax
                numlocal += 1
        # averaging over all the local regions
        #print('lmaxmean :{}, numlocal: {}').format(lmaxmean, numlocal)
        return lmaxmean / numlocal
    ## normalization specific for the saliency map model
    def SMNormalization(self, src):
        dst = self.SMRangeNormalize(src)
        #dst = src        
        lmaxmean = self.SMAvgLocalMax(dst)
        normcoeff = (1-lmaxmean)*(1-lmaxmean)
        return dst * normcoeff
    ## normalizing feature maps
    def normalizeFeatureMaps(self, FM):
        NFM = list()
        for i in range(0,6):
            normalizedImage = self.SMNormalization(FM[i])
            nownfm = cv2.resize(normalizedImage, (self.width, self.height), interpolation=cv2.INTER_LINEAR)
            NFM.append(nownfm)
        return NFM

    ## intensity conspicuity map
    def ICMGetCM(self, src):
        NIFM = self.normalizeFeatureMaps(src)
        ICM = sum(NIFM)
        return ICM

    def ICMGetCM2(self, src1, src2):
        NIFM1 = self.normalizeFeatureMaps(src1)
        NIFM2 = self.normalizeFeatureMaps(src2)
        T = NIFM1+NIFM2
        NIFM = T
        #ICM = self.normalizeFeatureMaps(NIFM)
        ICM = sum(NIFM)
        return ICM
    
    ## color conspicuity map
    def CCMGetCM(self, CFM_RG, CFM_BY):
        # extracting a conspicuity map for every color opponent pair
        CCM = self.ICMGetCM2(CFM_RG, CFM_BY)
        
        # return
        return CCM
    ## orientation conspicuity map
    def OCMGetCM(self, OFM):
        OCM = np.zeros((self.height, self.width))
        for i in range (0,4):
            # slicing
            nowofm = OFM[i*6:(i+1)*6]  # angle = i*45
            # extracting a conspicuity map for every angle
            NOFM = self.ICMGetCM(nowofm)
            # normalize
            NOFM2 = self.SMNormalization(NOFM)
            # accumulate
            OCM += NOFM2
        return OCM
    ## motion conspicuity map
    def MCMGetCM(self, MFM_X, MFM_Y):
        return self.CCMGetCM(MFM_X, MFM_Y)

    def SMGetOnlySM(self, src):
        # definitions
        size = src.shape
        width  = size[1]
        height = size[0]
        # check
#        if(width != self.width or height != self.height):
#            sys.exit("size mismatch")
        # extracting individual color channels
        R, G, B, Y, I = self.SMExtractRGBI(src)
        # extracting feature maps
        IFM = self.IFMGetFM(I)
        CFM_RG, CFM_BY = self.CFMGetFM(R, G, B, Y)
        OFM = self.OFMGetFM(I)
        #MFM_X, MFM_Y = self.MFMGetFM(I)
        # extracting conspicuity maps
        ICM = self.ICMGetCM(IFM)
        CCM = self.CCMGetCM(CFM_RG, CFM_BY)
        OCM = self.OCMGetCM(OFM)
        #MCM = self.MCMGetCM(MFM_X, MFM_Y)
        # adding all the conspicuity maps to form a saliency map
        wi = pySaliencyMapDefs.weight_intensity
        wc = pySaliencyMapDefs.weight_color
        wo = pySaliencyMapDefs.weight_orientation
        #wm = pySaliencyMapDefs.weight_motion
        #SMMat = wi*ICM + wc*CCM + wo*OCM + wm*MCM
        SMMat = wi*ICM + wc*CCM + wo*OCM

        # normalize
        resSM = self.SMRangeNormalize(SMMat)
        # return
        return resSM

    # core
    def SMGetSM(self, src):
        # definitions
        size = src.shape
        width  = size[1]
        height = size[0]
        # check
#        if(width != self.width or height != self.height):
#            sys.exit("size mismatch")
        # extracting individual color channels
        R, G, B, Y, I = self.SMExtractRGBI(src)
        # extracting feature maps
        IFM = self.IFMGetFM(I)
        CFM_RG, CFM_BY = self.CFMGetFM(R, G, B, Y)
        OFM = self.OFMGetFM(I)
        #MFM_X, MFM_Y = self.MFMGetFM(I)
        # extracting conspicuity maps
        ICM = self.ICMGetCM(IFM)
        CCM = self.CCMGetCM(CFM_RG, CFM_BY)
        OCM = self.OCMGetCM(OFM)
        #MCM = self.MCMGetCM(MFM_X, MFM_Y)
        # adding all the conspicuity maps to form a saliency map
        wi = pySaliencyMapDefs.weight_intensity
        wc = pySaliencyMapDefs.weight_color
        wo = pySaliencyMapDefs.weight_orientation
        #wm = pySaliencyMapDefs.weight_motion
        #SMMat = wi*ICM + wc*CCM + wo*OCM + wm*MCM
        SMMat = wi*ICM + wc*CCM + wo*OCM
        #SMMat = OCM*0.3
        #testpix = np.array(CCM)

        #f = open("test.txt","w")
        #for i in range(0, len(testpix)):
        #    for j in range(0, len(testpix[i])):
        #        f.write("%s" % testpix[i][j])
        #        f.write("\t")
        #    f.write("\n")
        #f.close()
        #for i in range(0, len(testpix)):
        #    for j in range(0, len(testpix[i])):
        #        if testpix[i][j] < 0.04:
        #            testpix[i][j] = 0



        # normalize
        normalizedSM = self.SMRangeNormalize(SMMat)
        #normalizedSM = self.SMRangeNormalize(testpix)
        normalizedSM2 = normalizedSM.astype(np.float32)
        smoothedSM = cv2.bilateralFilter(normalizedSM2, 7, 3, 1.55)
        self.SM = cv2.resize(smoothedSM, (width,height), interpolation=cv2.INTER_NEAREST)
        # return

        ICM = self.SMRangeNormalize(ICM)
        CCM = self.SMRangeNormalize(CCM)
        OCM = self.SMRangeNormalize(OCM)
        I = self.SMRangeNormalize(I)
        return self.SM, ICM, CCM, OCM, I

    # 20180129 sangbong
    # get features: intensity
    def SMGetICM(self, src):
        # definitions
        size = src.shape
        width  = size[1]
        height = size[0]

        R, G, B, Y, I = self.SMExtractRGBI(src)

        IFM = self.IFMGetFM(I)

        # extracting feature maps
        ICM = self.ICMGetCM(IFM)
        ICM = self.SMRangeNormalize(ICM)
        return ICM

    # get features: color
    def SMGetCCM(self, src):
        # definitions
        size = src.shape
        width  = size[1]
        height = size[0]
        R, G, B, Y, I = self.SMExtractRGBI(src)
        CFM_RG, CFM_BY = self.CFMGetFM(R, G, B, Y)

        # extracting feature maps
        CCM = self.CCMGetCM(CFM_RG, CFM_BY)
        CCM = self.SMRangeNormalize(CCM)
        return CCM

    # get features: orientation
    def SMGetOCM(self, src):
        # definitions
        size = src.shape
        width  = size[1]
        height = size[0]
        R, G, B, Y, I = self.SMExtractRGBI(src)
        OFM = self.OFMGetFM(I)

        # extracting conspicuity maps
        OCM = self.OCMGetCM(OFM)
        OCM = self.SMRangeNormalize(OCM)
        return OCM
    # 20180129 sangbong


    def SMGetBinarizedSM(self, src):
        # get a saliency map
        if self.SM is None:
            self.SM = self.SMGetSM(src)
        # convert scale
        SM_I8U = np.uint8(255 * self.SM)
        # binarize
        thresh, binarized_SM = cv2.threshold(SM_I8U, thresh=0, maxval=255, type=cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        return binarized_SM

    def SMGetSalientRegion(self, src):
        # get a binarized saliency map
        binarized_SM = self.SMGetBinarizedSM(src)
        # GrabCut
        img = src.copy()
        mask =  np.where((binarized_SM!=0), cv2.GC_PR_FGD, cv2.GC_PR_BGD).astype('uint8')
        bgdmodel = np.zeros((1,65),np.float64)
        fgdmodel = np.zeros((1,65),np.float64)
        rect = (0,0,1,1)  # dummy
        iterCount = 1
        cv2.grabCut(img, mask=mask, rect=rect, bgdModel=bgdmodel, fgdModel=fgdmodel, iterCount=iterCount, mode=cv2.GC_INIT_WITH_MASK)
        # post-processing
        mask_out = np.where((mask==cv2.GC_FGD) + (mask==cv2.GC_PR_FGD), 255, 0).astype('uint8')
        output = cv2.bitwise_and(img,img,mask=mask_out)
        return output
