import numpy as np
import cv2
import pygame
import mediapipe as mp
from cvzone.HandTrackingModule import HandDetector

width =1280
height = 720


cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)


detector = HandDetector(detectionCon=0.4, maxHands=2)

      
while True:
        
    
    ret, img = cap.read()
    #cv2.imwrite('sample.jpg',img)
    
    img = detector.findHands(img,draw=True)

    cv2.imshow('img', img)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
 