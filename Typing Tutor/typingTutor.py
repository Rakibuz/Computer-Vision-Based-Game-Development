import numpy as np
import cv2
import pygame
import mediapipe as mp
#from cvzone.HandTrackingModule import HandDetector


width =1280
height = 720


mpHands=mp.solutions.hands
hands=mpHands.Hands(static_image_mode=True,max_num_hands=2,min_detection_confidence=0.5)
mpDraw= mp.solutions.drawing_utils
  
cap = cv2.VideoCapture(1)
cap.set(3,1280)
cap.set(4,720)

scale=4
widthKeybord = 287*scale
heightKeybord = 72*scale

#initialWarpPoints = [[122, 272], [1192, 258], [136, 541], [1192, 516]]
initialWarpPoints = [[176, 218], [1244, 213], [182, 484], [1238, 479]]
pts1 = np.float32(initialWarpPoints)
pts2 = np.float32([[0, 0], [widthKeybord, 0], [0, heightKeybord], [widthKeybord, heightKeybord]])


# Variables
isFirstFrame = True
currentKey = 'y'
currentKeyPressed = False
scoreCorrect = 0
scoreWrong = 0
delayCount = 0



# Bounding box of each key and the correct finger
keyLocations = {
    # First Row
    'q': [28, 0, 16, 15, 'left_pinky'],
    'w': [47, 0, 16, 15, 'left_ring'],
    'e': [67, 0, 16, 15, 'left_middle'],
    'r': [86, 0, 16, 15, 'left_index'],
    't': [105, 0, 16, 15, 'left_index'],
    'y': [124, 0, 16, 15, 'right_index'],
    'u': [143, 0, 16, 15, 'right_index'],
    'i': [162, 0, 16, 15, 'right_middle'],
    'o': [182, 0, 16, 15, 'right_ring'],
    'p': [201, 0, 16, 15, 'right_pinky'],
    # Second Row
    'a': [32, 19, 16, 15, 'left_pinky'],
    's': [52, 19, 16, 15, 'left_ring'],
    'd': [71, 19, 16, 15, 'left_middle'],
    'f': [90, 19, 16, 15, 'left_index'],
    'g': [109, 19, 16, 15, 'left_index'],
    'h': [129, 19, 16, 15, 'right_index'],
    'j': [148, 19, 16, 15, 'right_index'],
    'k': [167, 19, 16, 15, 'right_middle'],
    'l': [187, 19, 16, 15, 'right_ring'],
    # Third Row
    'z': [42, 37, 16, 16, 'left_pinky'],
    'x': [62, 37, 16, 16, 'left_ring'],
    'c': [81, 37, 16, 16, 'left_middle'],
    'v': [100, 37, 16, 16, 'left_index'],
    'b': [119, 37, 16, 16, 'left_index'],
    'n': [138, 37, 16, 16, 'right_index'],
    'm': [158, 37, 16, 16, 'right_index']
}

pygame.init()
# Create Window/Display
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ai Typing Tutor")

# Initialize Clock for FPS
fps = 30
clock = pygame.time.Clock()


# Creating a dic for positions of the keys in the background image
rows = [['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
        ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
        ['z', 'x', 'c', 'v', 'b', 'n', 'm']]

rowsStart = [192, 214, 235]
keyLocationsBackground = {}
for i, row in enumerate(rows):
    for j, alphabet in enumerate(row):
        keyLocationsBackground[alphabet] = [rowsStart[i] + 76 * j, 364 + 74 * i, 62, 62]



#detector = HandDetector(detectionCon=0.4, maxHands=2)
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

while(cap.isOpened()):
      
    while True:
        imgBackground = cv2.imread("./Typing Tutor/Background.png")
        currentKeyPressed = False


        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                myKey = getattr(pygame, 'K_{}'.format(currentKey))
                if event.key == myKey:
                    print(f'{currentKey} key was pressed')
                    currentKeyPressed = True
             
          
        ret, img = cap.read()
        #cv2.imwrite('sample.jpg',img)
        converted_image=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        results=hands.process(converted_image)
        #hands, img = detector.findHands(img, flipType=False)
        img=Hand_Finder(img)
        lmlist=Finger_Detector(img,draw=False)

        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        imgWarp = cv2.warpPerspective(img, matrix, (widthKeybord, heightKeybord))
        #imgWarp = cv2.flip(imgWarp, 1)
        
        for point in initialWarpPoints:
            cv2.circle(img,point,5,(0,0,255),cv2.FILLED)
        
        
        if hands:
            print(len(lmlist))
            if len(lmlist) >=21:
                cv2.putText(imgBackground, "Detection: Solid", (50, 50), cv2.FONT_HERSHEY_PLAIN,
                            2, (0, 255, 0), 2)
            else:
                cv2.putText(imgBackground, "Detection: Weak", (50, 50), cv2.FONT_HERSHEY_PLAIN,
                            2, (0, 0, 255), 2)



        
        # Draw the bounding bbox on the warp image
        for key, value in keyLocations.items():
            x, y, w, h = value[0] * scale, value[1] * scale, value[2] * scale, value[3] * scale
            cv2.rectangle(imgWarp, (x, y), (x + w, y + h), (255, 0, 255), 2)
        
        cv2.putText(imgBackground, currentKey, (590, 260), cv2.FONT_HERSHEY_PLAIN,
                10, (255, 255, 255), 20)

        cv2.imshow('img', img)
        cv2.imshow('img warp', imgWarp)
        if cv2.waitKey(10) & 0xff == ord('q'):
            break
        
        # Draw on the Background image
        if currentKeyPressed:
            valueCurrent=keyLocationsBackground[currentKey]
            x,y,w,h=valueCurrent
            cv2.rectangle(imgBackground,(x,y),(x+w,y+h),(0,255,0),cv2.FILLED)

        
         # Draw all the alphabets on the background image
        for key, val in keyLocationsBackground.items():
            x, y, w, h = val
            cv2.putText(imgBackground, key, (x + 15, y + 45), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255))





         # OpenCV  Display
        imgRGB = cv2.cvtColor(imgBackground, cv2.COLOR_BGR2RGB)
        imgRGB = np.rot90(imgRGB)
        frame = pygame.surfarray.make_surface(imgRGB).convert()
        frame = pygame.transform.flip(frame, True, False)
        window.blit(frame, (0, 0))


        # Update Display
        pygame.display.update()
        # Set FPS
        clock.tick(fps)
                
    cap.release()
    cv2.destroyAllWindows()
else:
    print("Alert ! Camera disconnected")