import cv2
import mediapipe as mp

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


while True:

    success,img=cap.read()
    img = cv2.flip(img, 1) #horizontal filp=1 vertical flip=0
   
    converted_image=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=hands.process(converted_image)
    img=Hand_Finder(img)
    lmlist=Finger_Detector(img,draw=False)
    #print(lmlist)

    if len(lmlist)!=0:
        cursor=[]
        cursor=lmlist[8][1:] #[8, 404, 406]  cursor is having [0,1,2] 1and 2 value
        if 100<cursor[0]<300 and 100<cursor[1]<300:
            #color=(0,255,0)
            print('Entered')

    cv2.rectangle(img,(100,100),(300,300),color,cv2.FILLED)
   




    cv2.imshow("Image",img)
    if cv2.waitKey(5) & 0xFF == ord("q"):
                break
  
    