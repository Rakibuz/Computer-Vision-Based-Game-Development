import math
import cv2
import cvzone
import mediapipe as mp
import numpy as np
import math
import random
 
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
    def __init__(self,pathFood):
          
         self.points=[] # all the points of the snake 
         self.lengths=[]  # distance between each point
         self.currentLength = 0  # total length of the snake
         self.allowedLength = 150  # total allowed Length
         self.previousHead = 0, 0  # previous head point

         self.imgFood = cv2.imread(pathFood, cv2.IMREAD_UNCHANGED)
         self.hFood, self.wFood, _ = self.imgFood.shape
         self.foodPoint = 0, 0
         self.randomFoodLocation()


         self.score = 0
         self.gameOver = False
    
    def randomFoodLocation(self):
        self.foodPoint = random.randint(100, 1000), random.randint(100, 600)

    def update(self, imgMain, currentHead):
        if self.gameOver:
            cvzone.putTextRect(imgMain, "Game Over", [300, 400],
                               scale=7, thickness=5, offset=20)
            cvzone.putTextRect(imgMain, f'Your Score: {self.score}', [300, 550],
                               scale=7, thickness=5, offset=20)
        else:
            px, py = self.previousHead
            cx, cy = currentHead

            self.points.append([cx, cy])
            distance = math.hypot(cx - px, cy - py)
            self.lengths.append(distance)
            self.currentLength += distance
            self.previousHead = cx, cy

            # Length Reduction
            if self.currentLength > self.allowedLength:
                for i, length in enumerate(self.lengths):
                    self.currentLength -= length
                    self.lengths.pop(i)
                    self.points.pop(i)
                    if self.currentLength < self.allowedLength:
                        break
            
            # Check if snake ate the Food
            rx, ry = self.foodPoint
            if rx - self.wFood // 2 < cx < rx + self.wFood // 2 and  ry - self.hFood // 2 < cy < ry + self.hFood // 2:
                #print('ate')
                self.randomFoodLocation()
                self.allowedLength += 50
                self.score += 1
                #print(self.score)
                
     
            # Draw Snake
            if self.points:
                for i, point in enumerate(self.points):
                    if i != 0: #first one does not have previous value
                        cv2.line(imgMain, self.points[i - 1], self.points[i], (0, 0, 255), 20)
                cv2.circle(imgMain, self.points[-1], 20, (0, 255, 0), cv2.FILLED)

            # Draw Food
            rx, ry = self.foodPoint
            imgMain = cvzone.overlayPNG(imgMain, self.imgFood,(rx - self.wFood // 2, ry - self.hFood // 2))
            
            #Draw Score

            cv2.putText(imgMain, f'Score: {self.score}', [50, 80],scale=3, thickness=3, offset=10)



            # Check for Collision
            pts = np.array(self.points[:-2], np.int32) #ignoring last two points
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(imgMain, [pts], False, (0, 255, 0), 3)
            minDist = cv2.pointPolygonTest(pts, (cx, cy), True)
            #print(minDist)

            if -1 <= minDist <= 1:
                print("Hit")
                self.gameOver = True
                self.points = []  # all points of the snake
                self.lengths = []  # distance between each point
                self.currentLength = 0  # total length of the snake
                self.allowedLength = 150  # total allowed Length
                self.previousHead = 0, 0  # previous head point
                self.randomFoodLocation()
                self.score = 0

        return imgMain

game = SnakeGameClass("./Snake Game/Images/frog.png")
#game = SnakeGameClass()

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
  