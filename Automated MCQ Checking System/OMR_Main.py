import cv2
import numpy as np
import utlis

########################################################
path="./Automated MCQ Checking System/OMR_Project_Multiple_Choice.JPG"
widthImg=700
heightImg=700

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

countours,hierarchy=cv2.findContours(imgCanny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
cv2.drawContours(imgContours,countours,-1,(0,255,0),10)

#Find Rectangles
rectCon=utlis.rectContour(countours)
biggestContour=utlis.getCornerPoints(rectCon[0])
gradePoints=utlis.getCornerPoints(rectCon[1])
#print(biggestContour)
if biggestContour.size !=0 and gradePoints.size!=0:
    cv2.drawContours(imgBiggestContours,biggestContour,-1,(0,0,255),10)
    cv2.drawContours(imgBiggestContours,gradePoints,-1,(255,0,0),10)


imgBlank=np.zeros_like(img)
imageArray=([img,imgGray,imgBlur,imgCanny],
            [imgContours,imgBiggestContours,imgBlank,imgBlank])
imgStacked=utlis.stackImages(imageArray,0.5)


cv2.imshow("Stacked Images",imgStacked)
cv2.waitKey(0)