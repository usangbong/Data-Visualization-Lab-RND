import cv2, enum, time, os, math
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import rankdata

#############################################################################
#   User variables (static)
#############################################################################
class PltFunc :
    def plot1row2Img(img1, img2):
        fig = plt.figure()
        fig.add_subplot(1,2,1)
        plt.imshow(img1)
        fig.add_subplot(1,2,2)
        plt.imshow(img2)
        plt.show()    

class ALG(enum.Enum):
    MAE   = 0
    MSE   = 1
    RMSE  = 2
    PSNR  = 3
    SSIM  = 4
    P_MSE = 5    
    
class ImgCompare :
    def cvt256gray(img) :
        img = cv2.resize(img, (256,256), interpolation=cv2.INTER_LINEAR )
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return img
    
    def mae(img1, img2):
        img1 = ImgCompare.cvt256gray(img1)
        img2 = ImgCompare.cvt256gray(img2)
        err = np.sum(abs((img1.astype("float") - img2.astype("float"))))
        err /= float(img1.shape[0] * img1.shape[1])
        return err

    def mse(img1, img2):
        img1 = ImgCompare.cvt256gray(img1)
        img2 = ImgCompare.cvt256gray(img2)
        err = np.sum((img1.astype("float") - img2.astype("float")) ** 2)
        err /= float(img1.shape[0] * img1.shape[1])
        return err

    def p_mse(img1, img2):
        img1 = ImgCompare.cvt256gray(img1)
        img2 = ImgCompare.cvt256gray(img2)
        maxval = np.max((img1.astype("float") - img2.astype("float")) ** 2)
        err = np.sum((img1.astype("float") - img2.astype("float")) ** 2)
        err /= float(img1.shape[0] * img1.shape[1])
        return err/maxval

    def rmse(img1, img2):
        err = ImgCompare.mse(img1, img2)
        return math.sqrt(err)

    def psnr(img1, img2):
        _rmse = ImgCompare.rmse(img1,img2)
        if _rmse == 0:
            return 100
        PIXEL_MAX = 255.0
        return 20 * math.log10(PIXEL_MAX / _rmse)

    def percent_ssim(img1, img2) :
        from skimage.measure import compare_ssim as ssim
        #img1 = cv2.resize(img1, (256,256), interpolation=cv2.INTER_LINEAR )
        #img2 = cv2.resize(img2, (256,256), interpolation=cv2.INTER_LINEAR )
        s = ssim(img1,img2, multichannel = True)
        return s

class ViewGuide :
    def mainLoop(rBase, tImgPath) :
        start = time.time()
        tempPath = rBase
        rImageList = os.listdir(tempPath)
        rImageList.sort()
        #print(tempPath+rImageList[0])
        tImg = cv2.imread(tImgPath)
        #plt.imshow(tImg)
        #plt.show()
        tImg = cv2.resize(tImg, (256,256), interpolation=cv2.INTER_LINEAR )
        tImg = cv2.cvtColor(tImg, cv2.COLOR_BGR2RGB)
        rImgs = []
        ssimArr = []
        psnrArr = []
        pmseArr = []
        
        votingArr = [[1,3,9],[0,4,2,10],[1,5,11],[0,4,6,12],[1,3,5,7],[2,4,8,13],[3,7,14],[4,6,8,15],[5,7,16],[0,10,12,17],[1,9,11,18],[2,10,13,19],[3,9,14,20],[5,11,16,22],[6,12,15,23],[7,14,16,24],[8,13,15,25],[9,18,20],[10,17,19,21],[11,18,22],[12,17,21,23],[18,20,22,24],[13,19,21,25],[14,20,24],[15,21,23,25],[16,22,24]]
        
        for filename in rImageList :
            rImg = cv2.imread(tempPath+filename)
            plt.imshow(rImg)
            plt.show()
            rImg = rImg[150:1200, 300:1600]
            rImg = cv2.resize(rImg, (256,256), interpolation=cv2.INTER_LINEAR )
            rImg = cv2.cvtColor(rImg, cv2.COLOR_BGR2RGB)
            rImgs.append(rImg)
            #PltFunc.plot1row2Img(rImg, tImg)
            ssim = ImgCompare.percent_ssim(rImg, tImg)
            psnr = ImgCompare.psnr(rImg, tImg)
            pmse = ImgCompare.p_mse(rImg, tImg)
            #print(filename)
            #print( "ssim : %.2f , psnr : %.2f, pmse : %.2f" %(ssim*100.0, psnr,pmse*100.0) )
            
            ssimArr.append(ssim)
            psnrArr.append(psnr)
            pmseArr.append(pmse)
            
        
        print("calc Total time : ", (time.time() - start), 'sec')
        print(ssimArr)
        
        ssimRank = rankdata(ssimArr)
        psnrRank = rankdata(psnrArr)
        pmseRank = rankdata(pmseArr)
        votingArrSSIM = [0 for _ in range(26)]
        votingArrPSNR = [0 for _ in range(26)]
        votingArrPMSE = [0 for _ in range(26)]
        votingArrSum = [0 for _ in range(26)]
        
        for i in range(len(ssimRank)) :
            votingArrSSIM[i] += (ssimRank[i]-1)
            votingArrPSNR[i] += (psnrRank[i]-1)
            votingArrPMSE[i] += (pmseRank[i]-1)
            
            for j in votingArr[i] :
                votingArrSSIM[j] += (ssimRank[i]-1)/2
                votingArrPSNR[j] += (psnrRank[i]-1)/2
                votingArrPMSE[j] += (pmseRank[i]-1)/2
                
        for i in range(len(votingArrSSIM)) :
            votingArrSum[i]+=votingArrSSIM[i]
            votingArrSum[i]+=votingArrPSNR[i]
            votingArrSum[i]+=votingArrPMSE[i]
            
        votingSsimRank = rankdata(votingArrSSIM)
        votingPsnrRank = rankdata(votingArrPSNR)
        votingPmseRank = rankdata(votingArrPMSE)
        votingSumRank = rankdata(votingArrSum)
        
        #print (votingArrSSIM)
        for i in range(len(rImgs)):
            PltFunc.plot1row2Img(rImgs[i], tImg)
            print( "ssim : %.2f , psnr : %.2f, pmse : %.2f" %(ssimArr[i]*100.0, psnrArr[i],pmseArr[i]*100.0) )
            print( "voting ssim : %.2f [%d]" % (votingArrSSIM[i], votingSsimRank[i]))
            print( "voting psnr : %.2f [%d]" % (votingArrPSNR[i], votingPsnrRank[i]))
            print( "voting pmse : %.2f [%d]" % (votingArrPMSE[i], votingPmseRank[i]))
            print( "voting sum : %.2f [%d]" % (votingArrSum[i], votingSumRank[i]))
        
        print("==================================================================================")
        print("Voting SSIM")
        print("==================================================================================")
        for j in range(0,10) :
            for i in range(len(votingSsimRank)) :
                if (votingSsimRank[i] == (26-j)) :
                    PltFunc.plot1row2Img(rImgs[i], tImg)
                    print( "ssim : %.2f , psnr : %.2f, pmse : %.2f" %(ssimArr[i]*100.0, psnrArr[i],pmseArr[i]*100.0) )
                    print( "voting ssim : %.2f [%d]" % (votingArrSSIM[i], votingSsimRank[i]))
                    print( "voting psnr : %.2f [%d]" % (votingArrPSNR[i], votingPsnrRank[i]))
                    print( "voting pmse : %.2f [%d]" % (votingArrPMSE[i], votingPmseRank[i]))
                    print( "voting sum : %.2f [%d]" % (votingArrSum[i], votingSumRank[i]))
        
        print("==================================================================================")
        print("Voting PSNR")
        print("==================================================================================")
        for j in range(0,10) :
            for i in range(len(votingPsnrRank)) :
                if (votingPsnrRank[i] == (26-j)) :
                    PltFunc.plot1row2Img(rImgs[i], tImg)
                    print( "ssim : %.2f , psnr : %.2f, pmse : %.2f" %(ssimArr[i]*100.0, psnrArr[i],pmseArr[i]*100.0) )
                    print( "voting ssim : %.2f [%d]" % (votingArrSSIM[i], votingSsimRank[i]))
                    print( "voting psnr : %.2f [%d]" % (votingArrPSNR[i], votingPsnrRank[i]))
                    print( "voting pmse : %.2f [%d]" % (votingArrPMSE[i], votingPmseRank[i]))
                    print( "voting sum : %.2f [%d]" % (votingArrSum[i], votingSumRank[i]))
                    
        print("==================================================================================")
        print("Voting PMSE")
        print("==================================================================================")
        for j in range(0,10) :
            for i in range(len(votingPmseRank)) :
                if (votingPmseRank[i] == (26-j)) :
                    PltFunc.plot1row2Img(rImgs[i], tImg)
                    print( "ssim : %.2f , psnr : %.2f, pmse : %.2f" %(ssimArr[i]*100.0, psnrArr[i],pmseArr[i]*100.0) )
                    print( "voting ssim : %.2f [%d]" % (votingArrSSIM[i], votingSsimRank[i]))
                    print( "voting psnr : %.2f [%d]" % (votingArrPSNR[i], votingPsnrRank[i]))
                    print( "voting pmse : %.2f [%d]" % (votingArrPMSE[i], votingPmseRank[i]))
                    print( "voting sum : %.2f [%d]" % (votingArrSum[i], votingSumRank[i]))
                    
        print("==================================================================================")
        print("Voting SUM")
        print("==================================================================================")
        for j in range(0,10) :
            for i in range(len(votingSumRank)) :
                if (votingSumRank[i] == (26-j)) :
                    PltFunc.plot1row2Img(rImgs[i], tImg)
                    print( "ssim : %.2f , psnr : %.2f, pmse : %.2f" %(ssimArr[i]*100.0, psnrArr[i],pmseArr[i]*100.0) )
                    print( "voting ssim : %.2f [%d]" % (votingArrSSIM[i], votingSsimRank[i]))
                    print( "voting psnr : %.2f [%d]" % (votingArrPSNR[i], votingPsnrRank[i]))
                    print( "voting pmse : %.2f [%d]" % (votingArrPMSE[i], votingPmseRank[i]))
                    print( "voting sum : %.2f [%d]" % (votingArrSum[i], votingSumRank[i]))
                    
                    
if __name__ == "__main__":
    renderImageBasePath = "./renderimage/bonsai1/1/"
    targetImageBasePath = "./targetimage/bonsai1/1/"
    targetImageFullPath = targetImageBasePath + 'bonsai1.jpg'
    
    ViewGuide.mainLoop(renderImageBasePath, targetImageFullPath)

    
   
