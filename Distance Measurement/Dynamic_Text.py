import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
import time
import numpy as np


cap=cv2.VideoCapture(0)
pTime = 0

detector = FaceMeshDetector(maxFaces=1)

textList=["Welcome ","R&D Lab","Infinity Infotech Ltd."]
sen=8
while True:
    success, img = cap.read()
    imgText=np.zeros_like(img)
    img, faces= detector.findFaceMesh(img,draw=False)
 
    if faces:
            face=faces[0]
            pointLeft=face[145]
            pointRight=face[374]
            w,_=detector.findDistance(pointLeft,pointRight)
            #Finding the focal length
            W=6.3

            f=920
            d=(W*f)/w
            #print(d)
        
            cvzone.putTextRect(img,f'Depth:{int(d)}cm',(face[10][0]-100,face[10][1]-50),scale=2)
            
            for i,text in enumerate(textList):
                singleHeight=20+int((int(d/sen)*sen)/4)
                scale=0.4+(int(d/sen)*sen)/75
                cv2.putText(imgText,text,(50,50+(i*singleHeight)),cv2.FONT_ITALIC,scale,(0,0,255),2)


    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN,
                2, (255, 0, 0), 1)
    
    imgStacked=cvzone.stackImages([img,imgText],2,1)
    cv2.imshow("Image", imgStacked)
    if cv2.waitKey(5) & 0xFF == ord("q"):
            break

cv2.destroyAllWindows()
cap.release()