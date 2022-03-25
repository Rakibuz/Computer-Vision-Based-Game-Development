import mediapipe as mp
import cv2
import time
import math
import cvzone
from cvzone.PlotModule import LivePlot


mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=2)
drawSpec = mpDraw.DrawingSpec(thickness=1, circle_radius=2)

cap = cv2.VideoCapture(0)
pTime = 0
plotY = LivePlot(640,360,[20,50],invert=True)

#--------------------------Right Eye-----------------------
#idList=[22,23,24,26,110,157,158,159,160,161,130,243]

#-----------------------------LeftEye-----------------------
#idList=[466,388,387,386,385,384,398,263,249,390,373,374,380,381,382,362]

#---------------------------------Combine------------------------
idList=[22,23,24,26,110,157,158,159,160,161,130,243,466,388,387,386,385,384,398,263,249,390,373,374,380,381,382,362]

ratiolist=[]
blinkCounter=0
counter=0
color=(255,0,255)

def findDistance(p1,p2):
     distance = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )
     return distance


while True:
    success, img = cap.read()
    #img=cv2.resize(img,(640,360))
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results =  faceMesh.process(imgRGB)

    faces = []
    if results.multi_face_landmarks:
        for faceLms in results.multi_face_landmarks:
            #mpDraw.draw_landmarks(img, faceLms, mpFaceMesh.FACEMESH_CONTOURS, drawSpec,drawSpec)

            face = [] 
            for id,lm in enumerate(faceLms.landmark): 
                #lm is normalized value from 0 to 1
                #print(lm)
                ih, iw, ic = img.shape  #image height,width,channel
                x,y = int(lm.x*iw), int(lm.y*ih)  #converting to pixel
                #print(id,x,y)
                face.append([x,y])
            faces.append(face)
    
            if faces:
                face=faces[0]
                for id in idList:
                    cv2.circle(img,tuple(face[id]),2,color,cv2.FILLED)

                leftUp=face[159]
                leftDown=face[23]
                leftLeft=face[130]
                leftRight=face[243]
                #print(leftUp)
                #cv2.line(img,tuple(leftUp),tuple(leftDown),(0,200,0),3)
                #cv2.line(img,tuple(leftLeft),tuple(leftRight),(0,200,0),3)
                length_Ver=findDistance(leftUp,leftDown)
                length_Hor=findDistance(leftLeft,leftRight)

                ratio=int((length_Ver/length_Hor)*100)
                ratiolist.append(ratio)
                
                if len(ratiolist)>3:
                    ratiolist.pop(0)
                
                ratioAvg=sum(ratiolist)/len(ratiolist)
                
                if ratioAvg<35 and counter==0:
                    blinkCounter +=1
                    color=(0,200,0)
                    counter=1
                if counter !=0:
                    counter +=1
                    if counter>10:
                        counter=0
                        color=(255,0,255)
                
                cvzone.putTextRect(img,f'Blink Count:{blinkCounter}',(50,100),colorR=color)
                   
                imgPlot=plotY.update(ratioAvg,color)
                img=cv2.resize(img,(640,360))
                imgStack=cvzone.stackImages([img,imgPlot],2,1)
            else:
                img=cv2.resize(img,(640,360))
                imgStack=cvzone.stackImages([img,imgPlot],2,1)
                
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN,
                3, (255, 0, 0), 3)

    cv2.imshow("Image", imgStack)
    if cv2.waitKey(25) & 0xFF == ord("q"):
            break

cv2.destroyAllWindows()
 