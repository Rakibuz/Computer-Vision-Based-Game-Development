from __future__ import print_function
from imutils.video import WebcamVideoStream
import cv2
import time

#frame counter
pTime=0
cTime=0

print("[INFO] sampling THREADED frames from webcam...")
#webcamVideoStreamclass object creation
vs = WebcamVideoStream(src=0).start()
 

while True:
    frame = vs.read()
    #frame = imutils.resize(frame, width=400)

    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    #print(fps)
    cv2.putText(frame,str(int(fps)),(30,50),cv2.FONT_HERSHEY_PLAIN,3,(0,0,220),3) 

    #display the frame
    cv2.imshow('Web Cam', frame)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break


vs.release()
cv2.destroyAllWindows()
