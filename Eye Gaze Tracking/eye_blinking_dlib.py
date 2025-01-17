import cv2
import numpy as np
import dlib
from math import hypot

cap=cv2.VideoCapture(0)
detector=dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("./Eye Gaze Tracking/shape_predictor_68_face_landmarks.dat")

def midpoint(p1 ,p2):
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)

font = cv2.FONT_HERSHEY_PLAIN

def get_blinking_ratio(eye_points, facial_landmarks):

    left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
    right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
    center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
    center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))

    hor_line = cv2.line(frame, left_point, right_point, (255, 0, 0), 2)
    ver_line = cv2.line(frame, center_top, center_bottom, (0, 255, 255), 2)

    ver_line_lenght = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))
    hor_line_lenght = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))

    ratio = hor_line_lenght / ver_line_lenght

    return ratio

while True:
    ret,frame= cap.read()
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    faces =detector(gray)
    for face in faces:
        x, y = face.left(), face.top()
        x1, y1 = face.right(), face.bottom()
        #print(face)
        cv2.rectangle(frame, (x, y), (x1, y1), (0, 255, 0), 2)

        landmarks = predictor(gray, face)

        #for checking a particular point
        # x_land=landmarks.part(36).x
        # y_land=landmarks.part(36).y
        # cv2.circle(frame,(x_land,y_land),3,(0,0,255),2)
         
        #Detect Blinking 
        left_eye_ratio = get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks)
        right_eye_ratio = get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks)
        blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2

        if blinking_ratio >5.7:
            cv2.putText(frame,"BLINKING",(50,150),font,7,(255,255,0))


        #print(ver_line_lenght)

   
    cv2.imshow("Frame",frame)
    if cv2.waitKey(25) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
