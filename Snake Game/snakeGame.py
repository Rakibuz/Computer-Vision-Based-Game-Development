import math
import cv2
import cvzone
import mediapipe as mp
import numpy as np
import sys


cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

while True:

    success,img=cap.read()
    img = cv2.flip(img, 1) 
    


    cv2.imshow("Image",img)
    if cv2.waitKey(5) & 0xFF == ord("q"):
                break
  