from __future__ import print_function
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import imutils
import cv2
import time

 
pTime=0
cTime=0

print("[INFO] sampling THREADED frames from webcam...")
vs = WebcamVideoStream(src=0).start()
fps = FPS().start()


print("[INFO] sampling frames from webcam...")
stream = cv2.VideoCapture(0)
fps = FPS().start()
 

while True:
    frame = vs.read()
    #frame = imutils.resize(frame, width=400)

    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    print(fps)
    cv2.putText(frame,str(int(fps)),(30,50),cv2.FONT_HERSHEY_PLAIN,3,(0,0,220),3) 
    cv2.imshow('Web Cam', frame)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break


stream.release()
cv2.destroyAllWindows()
