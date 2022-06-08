import math
import cv2
import cvzone
import mediapipe as mp
import numpy as np
import os


mpHands=mp.solutions.hands
hands=mpHands.Hands()
mpDraw= mp.solutions.drawing_utils
color=(255,0,255)

cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

class DragImg():
    def __init__(self,path,posOrigin,imgType):
        self.path=path
        self.posOrigin=posOrigin
        self.imgType=imgType
        
        if self.imgType=='png':
            self.img=cv2.imread(self.path,cv2.IMREAD_UNCHANGED)
        else:
            self.img=cv2.imread(self.path)
        
        self.size=self.img.shape[:2]

    def update(self, cursor):
        ox, oy = self.posOrigin
        h, w = self.size
 
        # Check if in region
        if ox < cursor[0] < ox + w and oy < cursor[1] < oy + h:
            self.posOrigin = cursor[0] - w // 2, cursor[1] - h // 2


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


#img1=cv2.imread('Augmented Reality/ImagesJPG/1.jpg')
#img1=cv2.imread('Augmented Reality/ImagesPNG/1.png',cv2.IMREAD_UNCHANGED)

#ox,oy=500,200
path="Augmented Reality/ImagesPNG"
myList=os.listdir(path)
#print(myList)

listImg=[]
for x, pathImg in enumerate(myList):  #x holds the mylist count using enumerate
    if 'png' in pathImg:
        imgType='png'
    else:
        imgType='jpg'
    listImg.append(DragImg(f'{path}/{pathImg}',[50+x*300,50],imgType))
#print(len(listImg))  

while True:

    success,img=cap.read()
    img = cv2.flip(img, 1) #horizontal filp=1 vertical flip=0
    converted_image=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=hands.process(converted_image)
    img=Hand_Finder(img)
    lmlist=Finger_Detector(img,draw=False)
    
    if len(lmlist)!=0:
        length=tip_cliked(4,8)
        if length<48:
            cursor=lmlist[8][1:]
            # if ox<cursor[0]<ox+w and oy<cursor[1]<oy+h:
            #     ox,oy=cursor[0]-w//2,cursor[1]-h//2
            #     #print('Inside Image')
            for imgObject in listImg:
                imgObject.update(cursor)

    try:
        for imgObject in listImg:
            #Draw for JPG Image
            h,w=imgObject.size
            ox,oy=imgObject.posOrigin
            if imgObject.imgType =='png':
                   #Draw for PNG Image
                img=cvzone.overlayPNG(img,imgObject.img,[ox,oy])
            else:
                img[oy:oy+h,ox:ox+w]=imgObject.img

    except:
        pass


    cv2.imshow("Image",img)
    if cv2.waitKey(5) & 0xFF == ord("q"):
                break