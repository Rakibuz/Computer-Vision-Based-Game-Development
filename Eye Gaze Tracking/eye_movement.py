import cv2
import numpy as np

cap=cv2.VideoCapture(0)


while True:
    ret,frame= cap.read()
    roi=frame[269: 795, 537:1416]
    cv2.imshow("Frame",roi)
    if cv2.waitKey(25) & 0xFF == ord("q"):
            break

cv2.destroyAllWindows()
