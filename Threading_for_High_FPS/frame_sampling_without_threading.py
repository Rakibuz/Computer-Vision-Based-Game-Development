import cv2
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import time

pTime=0
cTime=0


print("[INFO] sampling frames from webcam...")
stream = cv2.VideoCapture(0)
fps = FPS().start()
 

while True:
    (grabbed, frame) = stream.read()
    # update the FPS counter
    #fps.update()

    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(frame,str(int(fps)),(30,50),cv2.FONT_HERSHEY_PLAIN,3,(0,0,220),3) 
    #print(fps)
    cv2.imshow('Web Cam', frame)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break


stream.release()
cv2.destroyAllWindows()