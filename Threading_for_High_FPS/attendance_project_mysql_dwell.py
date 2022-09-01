import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from imutils.video import WebcamVideoStream
import time
import csv  #writing  encoded list to csv
import pandas as pd



#Database connection
from datetime import datetime
import mysql.connector

db= mysql.connector.connect(

    host="localhost",
    user="root",
    passwd="MySQL",
    database="ibiofin"
)

mycursor=db.cursor()


#frame counter
pTime=0
cTime=0

path = './Threading_for_High_FPS/Training_images'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])  #only name split the .jpg
print(classNames)

# def findEncodings(images):
#     encodeList = []
    
#     for img in images:
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         encode = face_recognition.face_encodings(img)[0]
#         #writer.writerow(encode)
#         #print(encode)
#         encodeList.append(encode)


#         # with open("./Threading_for_High_FPS/Encoded.csv", 'r+') as f:
#         #     f.truncate(0)
#         #     np.savetxt("./Threading_for_High_FPS/Encoded.csv", encodeList,delimiter =", ", fmt ='% s')
#     #print(encodeList)
#     return encodeList


def encoding_reader():
    df = pd.read_csv('./Threading_for_High_FPS/Encoded.csv', delimiter=',',header=None)
    list_of_csv = [list(row) for row in df.values]
    #print(list_of_csv)
    return list_of_csv



#marking attendance
def markAttendance(name):
    with open('./Threading_for_High_FPS/Attendance.csv','r+') as f:
        myDataList = f.readlines() # if somebody already arrived we don't want to repeat it
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            Str_time = now.strftime("%H:%M:%S")
            Str_day = now.strftime("%m/%d/%Y")
            f.writelines(f'\n{name},{Str_time},{Str_day}')


#marking attendance on sql database
def markAttendance_sql(name):
     now = datetime.now()
     Str_time = now.strftime("%H:%M:%S")
     Str_day = now.strftime("%Y/%m/%d")

    #SQL Connection
     sqlform="Insert into attendance(name,date,time) values(%s,%s,%s)"
     attendances= [(name,Str_day,Str_time)]
     mycursor.executemany(sqlform,attendances)
     db.commit()




#encodeListKnown = findEncodings(images)
encodeListKnown = encoding_reader()


#print(len(encodeListKnown))
#print(encodeListKnown)
print('Encoding Complete')

#cap = cv2.VideoCapture(0)
print("[INFO] sampling THREADED frames from webcam...")
#webcamVideoStreamclass object creation
vs = WebcamVideoStream(src=0).start()

#dwell time counter
object_id_list=[]
dtime=dict()
dwell_time=dict()

while True:
    #success, img = cap.read()
    img = vs.read()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)

    for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
        #print(faceDis)
        
        matchIndex = np.argmin(faceDis)

        # if matches[matchIndex]:
        #     name = classNames[matchIndex].upper()
        #     print(name)
        #     y1,x2,y2,x1 = faceLoc
        #     y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4 #for scaling
        #     cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
        #     cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
        #     cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
        #     markAttendance(name)
        #     markAttendance_sql(name)
        #------------------------------------------------------x---------------------------------
        #unknown face detection
        if faceDis[matchIndex]< 0.50:
            name = classNames[matchIndex].upper()

            #dwell time detection 
            if name not in object_id_list:
                object_id_list.append(name)
                dtime[name]=datetime.now()
                dwell_time[name]=0
            else:
                curr_time=datetime.now()
                old_time=dtime[name]
                time_diff=curr_time-old_time
                dtime[name]=datetime.now()
                sec=time_diff.total_seconds()
                dwell_time[name] +=sec
                
                if(int(dwell_time[name])>=5):
                    markAttendance(name)
                    markAttendance_sql(name)

        else: name = 'Unknown'
        #print(name)
        y1,x2,y2,x1 = faceLoc
        y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
        cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
        cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
        text="{}|{}".format(name,int(dwell_time[name]))
        cv2.putText(img,text,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)

           
    cTime=time.time()
    fps=1/(cTime-pTime)
    #print(int(fps))
    pTime=cTime
    #print(int(fps))
    cv2.putText(img,str(int(fps)),(30,50),cv2.FONT_HERSHEY_PLAIN,3,(0,0,220),3)
    cv2.imshow('Webcam',img)
    cv2.waitKey(1)  
    
 
