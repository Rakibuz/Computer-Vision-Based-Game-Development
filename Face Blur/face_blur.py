import cv2
from cvzone.FaceDetectionModule import FaceDetector

cap =cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

detector =FaceDetector(minDetectionCon=0.75)

while True:
    success, img =cap.read()
    img,bboxs=detector.findFaces(img,draw=True)
    cv2.imshow("Image",img)  

    cv2.waitKey(1)