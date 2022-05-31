from sre_constants import SUCCESS
import cv2
import numpy as np

cap=cv2.VideoCapture(1)
imgTarget=cv2.imread('./Augmented Reality/Images/Dettol.jpg')
myVid=cv2.VideoCapture('./Augmented Reality/Images/Cards Animation - After Effects and Element 3d.mkv')

success,imgVideo = myVid.read()
hT,wT,cT=imgTarget.shape
imgVideo=cv2.resize(imgVideo,(wT,hT))

orb=cv2.ORB_create(nfeatures=1000)
kp1,des1=orb.detectAndCompute(imgTarget,None)

imgTarget=cv2.drawKeypoints(imgTarget,kp1,None)

while True:
    succes,imgWebcam=cap.read()
    kp2,des2=orb.detectAndCompute(imgWebcam,None)
    #imgWebcam=cv2.drawKeypoints(imgWebcam,kp2,None)

    bf=cv2.BFMatcher()
    macthes=bf.knnMatch(des1,des2,k=2)
    good=[]
    for m,n in macthes:
        if m.distance<0.75*n.distance:
            good.append(m)
    print(len(good))

    imgFeatures=cv2.drawMatches(imgTarget,kp1,imgWebcam,kp2,good,None,flags=2)
    
    if len(good)>20:
        srcPts=np.float32([kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dstPts=np.float32([kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
        

        matrix,mask =cv2.findHomography(srcPts,dstPts,cv2.RANSAC,5)
        print(matrix)

        pts=np.float32([[0,0],[0,hT],[wT,hT],[wT,0]]).reshape(-1,1,2)
        dst=cv2.perspectiveTransform(pts,matrix)
        img2=cv2.polylines(imgWebcam,[np.int32(dst)],True,(255,0,0),3)

        
        imgWarp=cv2.warpPerspective(imgVideo,matrix,(imgWebcam.shape[1],imgWebcam.shape[0]))

    cv2.imshow('imgwrap',imgWarp)
    cv2.imshow('Img2',img2)
    cv2.imshow('ImgTarget',imgFeatures)
    cv2.imshow('myVid',imgVideo)
    cv2.imshow('myWebcam',imgWebcam)
    cv2.waitKey(0)