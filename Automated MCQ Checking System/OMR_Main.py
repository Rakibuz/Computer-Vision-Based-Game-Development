from random import choices
import cv2
import numpy as np
from sklearn import utils
import utlis

########################################################
path="./Automated MCQ Checking System/OMR_Project_Multiple_Choice.JPG"
widthImg=700
heightImg=700
questions=5
choices=5

#######################################################

img= cv2.imread(path)


#Preprocessing

img=cv2.resize(img,(widthImg,heightImg))
imgContours=img.copy()
imgBiggestContours=img.copy()
imgGray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
imgBlur=cv2.GaussianBlur(imgGray,(5,5),1) #(5,5)=kernel size, 1= sigma x
imgCanny=cv2.Canny(imgBlur,10,50)


#-------------------------Finding all contours-------------------------------------------
#Image contouring is process of identifying structural outlines of objects 
# in an image which in turn can help us identify shape of the object.

contours,hierarchy=cv2.findContours(imgCanny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
cv2.drawContours(imgContours,contours,-1,(0,255,0),10)

#Find Rectangles
rectCon=utlis.rectContour(contours)
biggestContour=utlis.getCornerPoints(rectCon[0])
gradePoints=utlis.getCornerPoints(rectCon[1])
#print(biggestContour)
if biggestContour.size !=0 and gradePoints.size!=0:
    cv2.drawContours(imgBiggestContours,biggestContour,-1,(0,0,255),20)
    cv2.drawContours(imgBiggestContours,gradePoints,-1,(255,0,0),20)
    
    biggestContour=utlis.reorder(biggestContour)
    gradePoints=utlis.reorder(gradePoints)


    pts1 = np.float32(biggestContour) # PREPARE POINTS FOR WARP
    pts2 = np.float32([[0, 0],[widthImg, 0], [0, heightImg],[widthImg, heightImg]]) # PREPARE POINTS FOR WARP
    matrix = cv2.getPerspectiveTransform(pts1, pts2) # GET TRANSFORMATION MATRIX
    imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg)) # APPLY WARP PERSPECTIVE



    ptG1 = np.float32(gradePoints) # PREPARE POINTS FOR WARP
    ptG2 = np.float32([[0, 0],[325, 0], [0, 150],[325, 150]]) # PREPARE POINTS FOR WARP
    matrixG = cv2.getPerspectiveTransform(ptG1, ptG2) # GET TRANSFORMATION MATRIX
    imgGradeDisplay = cv2.warpPerspective(img, matrixG, (325, 150)) # APPLY WARP PERSPECTIVE
    #cv2.imshow("Grade",imgGradeDisplay)


    #APPLY THRESOLD
    
    imgWarpGray=cv2.cvtColor(imgWarpColored,cv2.COLOR_BGR2GRAY)
    imgThresh=cv2.threshold(imgWarpGray,170,255,cv2.THRESH_BINARY_INV)[1]


    boxes=utlis.splitBoxes(imgThresh)
    #cv2.imshow('Test',boxes[2])
    #print(cv2.countNonZero(boxes[1]),cv2.countNonZero(boxes[2]))
    myPixelVal =np.zeros((questions,choices))
    countC=0
    countR=0
    for image in boxes:
        totalPixels=cv2.countNonZero(image)
        #print(totalPixels)
        myPixelVal[countR][countC]=totalPixels
        #print(myPixelVal)
        countC +=1
        if(countC==choices):countR +=1;countC=0
    print(myPixelVal) #pixel values of each circle




imgBlank=np.zeros_like(img)
imageArray=([img,imgGray,imgBlur,imgCanny],
            [imgContours,imgBiggestContours,imgWarpColored,imgThresh])
imgStacked=utlis.stackImages(imageArray,0.5)


cv2.imshow("Stacked Images",imgStacked)
cv2.waitKey(0)