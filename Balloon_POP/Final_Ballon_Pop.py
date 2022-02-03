from random import randint, random
import pygame
import cv2
import numpy as np 
import mediapipe as mp
#from Hand_Tracking import Hand_Finder


#Initialize
pygame.init()

#Create window/Display
width,height= 1280,720
window=pygame.display.set_mode((width,height))
pygame.display.set_caption("Balloon Pop")


#Initialize Clock for fps
fps=30
clock=pygame.time.Clock()


#webcam
cap =cv2.VideoCapture(0)
cap.set(3,1280) #width
cap.set(4,720) #height


#Hand Tracking
mpHands=mp.solutions.hands
hands=mpHands.Hands()
mpDraw= mp.solutions.drawing_utils
 
 
def Hand_Finder(img,draw=True):
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            if draw:
                mpDraw.draw_landmarks(img, handLms,mpHands.HAND_CONNECTIONS)
    return img


def Finger_Detector(img,handNo=0,draw=True):
    landmark_List=[]
    if results.multi_hand_landmarks:
        myHand=results.multi_hand_landmarks[handNo]

        for id, lm in enumerate(myHand.landmark):
            h,w,c =img.shape
            cx,cy =int(lm.x*w),int(lm.y*h)
            landmark_List.append([id,cx,cy])
            if draw:
                cv2.circle(img,(cx,cy),5,(255,0,255),cv2.FILLED)
    return landmark_List

#Images
imgBallon=pygame.image.load('C:/Users/User/Game_Development/BalloonRed.png').convert_alpha()
rectBalloon=imgBallon.get_rect()
rectBalloon.x,rectBalloon.y=500,300


#Variables
speed=20


def resetBalloon():
    rectBalloon.x = randint(100,img.shape[1] -100)
    rectBalloon.y = img.shape[0]+50
    #rectBalloon.x=random.randint(100,img.shape[1] -100)


#Main Loop

start=True
while start:
    #Gets Events
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            start=False
            pygame.quit()


    #Apply Logic



    #OpenCv

    success, img =cap.read()
    img=cv2.flip(img,1)

    #Hand tracking on the succeed frame
    results=hands.process(img)
    img=Hand_Finder(img)


    rectBalloon.y -=speed
    

    #check if ballon has reached the top without pop
    if rectBalloon.y<0:
        resetBalloon()
        #speed +=1
    

    landmark_List=Finger_Detector(img,draw=False)

    if len(landmark_List)!=0: 
        x, y = landmark_List[8][1:]
        if rectBalloon.collidepoint(x,y):
           resetBalloon()


    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    imgRGB=np.rot90(imgRGB)
    frame=pygame.surfarray.make_surface(imgRGB).convert()
    frame=pygame.transform.flip(frame,True,False)
    window.blit(frame,(0,0))
    window.blit(imgBallon,rectBalloon)

    #update Display
    pygame.display.update()
   

    #set fps
    clock.tick(fps)