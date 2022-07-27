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
ans=[1,2,0,1,4]
webcamFeed=True
cameraNo=1
#######################################################

cap=cv2.VideoCapture(cameraNo)
cap.set(10,150)



while True:
    # if webcamFeed:success, img =cap.read()
    # else:img= cv2.imread(path)
        
    img= cv2.imread(path)
    #Preprocessing

    img=cv2.resize(img,(widthImg,heightImg))
    imgContours=img.copy()
    imgBiggestContours=img.copy()
    imgFinal=img.copy()
    imgGray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur=cv2.GaussianBlur(imgGray,(5,5),1) #(5,5)=kernel size, 1= sigma x
    imgCanny=cv2.Canny(imgBlur,10,50)

    try:
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

            #Getting non zero pixel values of each box

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
            #print(myPixelVal) #pixel values of each circle 
        
            #finding the maximum pixel values
            #Finding Index values
            myIndex=[]
            for x in range(0,questions):
                arr=myPixelVal[x]
                #print("arr",arr)
                myIndexVal = np.where(arr==np.amax(arr))
                #print(myIndexVal[0])
                myIndex.append(myIndexVal[0][0])
            #print(myIndex)


            #GRADING

            grading=[]

            for x in range (0,questions):
                if ans[x] == myIndex[x]:
                    grading.append(1)
                else:
                    grading.append(0)
            #print(grading)
            score= (sum(grading)/questions)*100    #Final Grade   sum(grading)=4, number of questions=5, 4/5=0.8
            print(score)

            
            #Displaying Answer
            imgResult=imgWarpColored.copy()
            imgResult=utlis.showAnswers(imgResult,myIndex,grading,ans,questions,choices)
            imRawDrawing=np.zeros_like(imgWarpColored)
            imRawDrawing=utlis.showAnswers(imRawDrawing,myIndex,grading,ans,questions,choices)
            invMatrix = cv2.getPerspectiveTransform(pts2, pts1)  
            imgInvWarp = cv2.warpPerspective(imRawDrawing, invMatrix, (widthImg, heightImg)) # correction projecting on orginal image

            imgRawGrade=np.zeros_like(imgGradeDisplay)
            cv2.putText(imgRawGrade,str(int(score))+"%",(60,100),cv2.FONT_HERSHEY_COMPLEX,3,(0,255,255),3)
            #cv2.imshow("Grade",imgRawGrade)

            invMatrixG = cv2.getPerspectiveTransform(ptG2, ptG1)  
            imgInvGradeDisplay= cv2.warpPerspective(imgRawGrade, invMatrixG, (widthImg, heightImg)) # correction projecting on orginal image


            imgFinal=cv2.addWeighted(imgFinal,1,imgInvWarp,1,0)
            imgFinal=cv2.addWeighted(imgFinal,1,imgInvGradeDisplay,1,0)



        imgBlank=np.zeros_like(img)
        imageArray=([img,imgGray,imgBlur,imgCanny],
                    [imgContours,imgBiggestContours,imgWarpColored,imgThresh],
                    [imgResult,imRawDrawing,imgInvWarp,imgFinal])
    except:
        imgBlank=np.zeros_like(img)
        imageArray=([img,imgGray,imgBlur,imgCanny],
                    [imgBlank,imgBlank,imgBlank,imgBlank],
                    [imgBlank,imgBlank,imgBlank,imgBlank])

    labels=[["Original","Gray","Blur","Canny"],
    ["Contours","Biggest Contour","Warp","Threshold"],
    ["Result","Raw Drawing","Inv Warp","Final"]]
    imgStacked=utlis.stackImages(imageArray,0.4)

    cv2.imshow("Final Result",imgFinal)
    cv2.imshow("Stacked Images",imgStacked)
    #cv2.waitKey(0)
    if cv2.waitKey(1)& 0xFF == ord('s'):
        cv2.imwrite("FinalResult.jpg",imgFinal)
        cv2.waitKey(300)
