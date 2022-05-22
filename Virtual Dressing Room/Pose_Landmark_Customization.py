import cv2
import mediapipe as mp
import time

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

cap=cv2.VideoCapture(0)
pTime = 0


def pose_finder(img,draw=True):
     #print(results.pose_landmarks)
    if results.pose_landmarks:
        if draw:
            mpDraw.draw_landmarks(img,results.pose_landmarks,mpPose.POSE_CONNECTIONS)  
        return img

def position_finder(img, draw=True):
    lmList = []
    if results.pose_landmarks:
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape
            # print(id, lm)
            cx, cy = int(lm.x * w), int(lm.y * h)
            lmList.append([id, cx, cy])
            if draw:
                cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
    return lmList


while True:
    success, img=cap.read()
    img=cv2.resize(img,(720,720))
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results=pose.process(imgRGB)
    

    img=pose_finder(img)
    lmList=position_finder(img,draw=False)

    if len(lmList) != 0:
            #print(lmList[14])
            cv2.circle(img, (lmList[14][1], lmList[14][2]), 15, (0, 0, 255), cv2.FILLED)

     
    
    #frame rate printing
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,(255, 0, 0), 3)
    cv2.imshow("Image",img)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break