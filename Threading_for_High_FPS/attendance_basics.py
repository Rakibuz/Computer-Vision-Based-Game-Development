import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime


imgPranto=face_recognition.load_image_file('./Threading_for_High_FPS/Training_images/Pranto.jpg')
imgPranto=cv2.cvtColor(imgPranto,cv2.COLOR_BGR2RGB)


imgTest=face_recognition.load_image_file('./Threading_for_High_FPS/Test_images/pranto.jpg')
imgTest=cv2.cvtColor(imgTest,cv2.COLOR_BGR2RGB)


faceLoc=face_recognition.face_locations(imgPranto)[0]
encodePranto=face_recognition.face_encodings(imgPranto)[0]
cv2.rectangle(imgPranto,(faceLoc[3],faceLoc[0]),(faceLoc[1],faceLoc[2]),(255,0,255),2)

faceLoc_Test=face_recognition.face_locations(imgTest)[0]
encode_Test=face_recognition.face_encodings(imgTest)[0]
cv2.rectangle(imgTest,(faceLoc_Test[3],faceLoc_Test[0]),(faceLoc_Test[1],faceLoc_Test[2]),(255,0,255),2)
 
results=face_recognition.compare_faces([encodePranto],encode_Test)
faceDis=face_recognition.face_distance([encodePranto],encode_Test)
print(results,faceDis)
cv2.putText(imgTest,f'{results}{round(faceDis[0],2)}',(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)


cv2.imshow('Pranto',imgPranto)
cv2.imshow('Pranto Test',imgTest)
cv2.waitKey(0)