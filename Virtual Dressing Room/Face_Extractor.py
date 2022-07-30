from turtle import width
import numpy as np
import cv2
import time
import os
 


face_cascade = cv2.CascadeClassifier('.\Virtual Dressing Room\cascades\data\haarcascade_frontalface_alt2.xml')
eye_cascade = cv2.CascadeClassifier(r'.\Virtual Dressing Room\cascades\data\haarcascade_eye.xml') 
lower_body_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_lowerbody.xml')


pTime = 0
cap = cv2.VideoCapture(0)

def roi_locator(roi,color,stroke,frame):
    for (x, y, w, h) in roi:
        color = color
        stroke = stroke
        end_cord_x=x+w
        end_cord_y=y+h
        cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)


 
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    #frame = cv2.resize(frame, (420, 420))	#resizing frame 224,224 
    
    gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
    eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
    #lower_body = lower_body_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
    
    roi_locator(faces,(255,0,0),2,frame)
    roi_locator(eyes,(0,255,0),2,frame)
    #roi_locator(lower_body,(0,255,0),2,frame)
     
    
    directory = os.getcwd()+r''
    try:
        os.mkdir(directory)
    except FileExistsError as ex:
        print('Exception Occured',ex)
    os.chdir(directory)
    
    for (x, y, w, h) in faces:
        FaceImg = frame[y:y+h,x:x+w]
        # To save an image on disk
        cv2.imwrite(str(w) + str(h) + '_faces.jpg', FaceImg)

    
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(frame, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN,2, (255, 0, 0), 1)
    

    cv2.imshow('frame',frame)
    
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
