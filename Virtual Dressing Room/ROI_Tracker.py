from turtle import width
import numpy as np
import cv2
import time
import pickle


face_cascade = cv2.CascadeClassifier('.\Virtual Dressing Room\cascades\data\haarcascade_frontalface_alt2.xml')
eye_cascade = cv2.CascadeClassifier(r'.\Virtual Dressing Room\cascades\data\haarcascade_eye.xml') 
lower_body_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_lowerbody.xml')

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(r"./Virtual Dressing Room/recognizers/face-trainner.yml")

labels={"person_name":1}
with open("./Virtual Dressing Room/pickles/face-labels.pickle", 'rb') as f:
    og_labels=pickle.load(f)
    labels = {v:k for k,v in og_labels.items()}

 

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
     
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(frame, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN,2, (255, 0, 0), 1)


    cv2.imshow('frame',frame)
    


    """
    #frame dimension printing
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))   # float `width`
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # float `height`
    print(width,height,end="\r")

    """
    
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
