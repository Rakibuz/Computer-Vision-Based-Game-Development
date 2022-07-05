import numpy as np
import cv2
import mediapipe as mp
from cvzone.HandTrackingModule import HandDetector  #cvzone==1.5.6
import socket

#parameters
width,height =1280,720 

#webcam 
cap = cv2.VideoCapture(0)
cap.set(3,width)
cap.set(4,height)

#Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

#communication--- for UDP protocol
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ("192.168.0.1", 8080)

      
while True:
    ret, img= cap.read()
    
    hands,img  = detector.findHands(img)
    data = []

    if hands:
        # Hand 1
        hand = hands[0]
        lmList = hand["lmList"]  # List of 21 Landmark points
        #print(lmList)

        for lm in lmList:
            data.extend([lm[0], height - lm[1], lm[2]])  #data.extend(x,h-y,z) h=720
        #print(data)

        sock.sendto(str.encode(str(data)), serverAddressPort)

    cv2.imshow('img', img)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
 