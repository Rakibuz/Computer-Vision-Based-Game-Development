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

cx,cy,w,h=100,100,200,200

class DragRect():
    def __init__(self, posCenter, size=[200, 200]):  #creating constractor no need to call it
        self.posCenter = posCenter
        self.size = size
 
    def update(self, cursor):
        cx, cy = self.posCenter
        w, h = self.size
 
        # If the index finger tip is in the rectangle region
        if cx - w // 2 < cursor[0] < cx + w // 2 and cy - h // 2 < cursor[1] < cy + h // 2:
            self.posCenter = cursor

rectList = []
for x in range(5):
    rectList.append(DragRect([x * 250 + 150, 150]))


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

def tip_cliked(tip1,tip2):

    x1,y1=lmlist[tip1][1],lmlist[tip1][2]
    x2,y2=lmlist[tip2][1],lmlist[tip2][2]
    cv2.circle(img,(x1,y1),10,(255,0,255),cv2.FILLED)
    cv2.circle(img,(x2,y2),10,(255,0,255),cv2.FILLED)
    cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
    cv2.circle(img,((x1+x2)//2,(y1+y2)//2),10,(255,0,255),cv2.FILLED)

    length=math.hypot(x2-x1,y2-y1)
    #print(length)
    if length<48:
            cv2.circle(img,((x1+x2)//2,(y1+y2)//2),10,(0,255,0),cv2.FILLED)
    return length


while True:

    success,img=cap.read()
    img = cv2.flip(img, 1) #horizontal filp=1 vertical flip=0
   
    converted_image=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=hands.process(converted_image)
    img=Hand_Finder(img)
    lmlist=Finger_Detector(img,draw=False)
    #print(lmlist)

    if len(lmlist)!=0:
        length=tip_cliked(4,8)
        if length<48:
            cursor=lmlist[8][1:] #[8, 404, 406]  cursor is having [0,1,2] 1and 2 value
            for rect in rectList:
                rect.update(cursor)

      ## Draw Transperency
    imgNew = np.zeros_like(img, np.uint8)
    for rect in rectList:
        cx, cy = rect.posCenter
        w, h = rect.size
        cv2.rectangle(imgNew, (cx - w // 2, cy - h // 2),
                      (cx + w // 2, cy + h // 2), color, cv2.FILLED)
        cvzone.cornerRect(imgNew, (cx - w // 2, cy - h // 2, w, h), 20, rt=0)
 
    out = img.copy()
    alpha = 0.1
    mask = imgNew.astype(bool)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]
    
    cv2.imshow("Image",out)
    if cv2.waitKey(5) & 0xFF == ord("q"):
                break
  
    
