import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import  storage
import requests
from datetime import datetime

cred = credentials.Certificate("./Face_Recognition_with_RealTime_Database/xxxx.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://xxxxx.com/",
    'storageBucket': "xxxxxx"
})


bucket = storage.bucket()


cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
imgBackground = cv2.imread('./Face_Recognition_with_RealTime_Database/Resources/background.png')

#Mode Images Importing
folderModePath = './Face_Recognition_with_RealTime_Database/Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))


# Load the encoding file
print("Loading Encode File ...")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, employeeIds = encodeListKnownWithIds
#print(employeeIds)
print("Encode File Loaded")

modeType = 0
counter = 0
id=-1
imgEmployee = []



while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)


    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    #cv2.imshow("Webcam", img)

    if faceCurFrame:

        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            #print("matches", matches)
            #print("faceDis", faceDis)

            matchIndex = np.argmin(faceDis)
            #print("Match Index", matchIndex)

            if matches[matchIndex]:
                    # print("Known Face Detected")
                    # print(employeeIds[matchIndex])
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                    imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                    #cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                    id=employeeIds[matchIndex]
                    print(id)
                    if counter ==0:
                        cvzone.putTextRect(imgBackground,"Loading",(275,400))
                        cv2.imshow("Face Attendance",imgBackground)
                        cv2.waitKey(1)
                        counter=1
                        modeType=1

        if counter!=0:  
            if counter==1:
                employeeInfo =db.reference(f'Employees/{id}').get()
                print(employeeInfo)
                # Get the Image from the storage
                blob = bucket.get_blob(f'./Face_Recognition_with_RealTime_Database/Images/{id}.jpg')
                #print(type(blob))
                #if blob is not None:
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgEmployee= cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
                print(imgEmployee.shape)


                # Update data of attendance
                datetimeObject = datetime.strptime(employeeInfo['Last_attendance_time'], "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                print(secondsElapsed)
                if secondsElapsed > 30:
                    ref = db.reference(f'Employees/{id}')
                    employeeInfo['Total_attendance'] += 1
                    ref.child('Total_attendance').set(employeeInfo['Total_attendance'])
                    ref.child('Last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeType = 3
                    counter = 0
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
            if modeType != 3:

                if 10 < counter < 20:
                    modeType = 2

                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if counter <= 10:
                    cv2.putText(imgBackground, str(employeeInfo['Total_attendance']), (861, 125),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(employeeInfo['Dept']), (1006, 550),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(id), (1006, 493),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(employeeInfo['Company']), (910, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(employeeInfo['Last_attendance_time']), (1025, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    #cv2.putText(imgBackground, str(employeeInfo['starting_year']), (1125, 625),
                    #            cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                    (w, h), _ = cv2.getTextSize(employeeInfo['Name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414 - w) // 2
                    cv2.putText(imgBackground, str(employeeInfo['Name']), (808 + offset, 445),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                    imgBackground[175:175 + 216, 909:909 + 216] = imgEmployee

                counter += 1

                if counter >= 20:
                    counter = 0
                    modeType = 0
                    employeeInfo = []
                    imgEmployee = []
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    else:
        modeType = 0
        counter = 0

    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(1)