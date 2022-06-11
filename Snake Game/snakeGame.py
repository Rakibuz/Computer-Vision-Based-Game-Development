import math
import cv2
import cvzone
import mediapipe as mp
import numpy as np
 
cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
mpHands=mp.solutions.hands
hands=mpHands.Hands()
mpDraw= mp.solutions.drawing_utils
color=(255,0,255)



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


class SnakeGameClass:
    def __init__(self):
          
         self.points=[] # all the points of the snake 
         self.lengths=[]  # distance between each point
         self.currentLength = 0  # total length of the snake
         self.allowedLength = 150  # total allowed Length
         self.previousHead = 0, 0  # previous head point

    def update(self, imgMain, currentHead):

        px, py = self.previousHead
        cx, cy = currentHead

        self.points.append([cx, cy])
        distance = math.hypot(cx - px, cy - py)
        self.lengths.append(distance)
        self.currentLength += distance
        self.previousHead = cx, cy

        # Draw Snake
         
        for i, point in enumerate(self.points):
            if i != 0: #first one does not have previous value
                cv2.line(imgMain, self.points[i - 1], self.points[i], (0, 0, 255), 20)
        cv2.circle(imgMain, self.points[-1], 20, (0, 255, 0), cv2.FILLED)
    
        return imgMain

#game = SnakeGameClass("./Snake Game/Images/3.png")
game = SnakeGameClass()

while True:

    success,img=cap.read()
    img = cv2.flip(img, 1) 

    converted_image=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=hands.process(converted_image)
    img=Hand_Finder(img)
    lmlist=Finger_Detector(img,draw=False)

    if len(lmlist)!=0:
        pointIndex = lmlist[8][1:]
        #cv2.circle(img,pointIndex,20,(200,0,200),cv2.FILLED)
        img = game.update(img, pointIndex)
    


    cv2.imshow("Image",img)
    if cv2.waitKey(5) & 0xFF == ord("q"):
                break
  