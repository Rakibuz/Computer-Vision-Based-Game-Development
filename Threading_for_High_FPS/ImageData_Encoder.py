import cv2
import numpy as np
import face_recognition
import os
 
import time
import csv  #writing  encoded list to csv
import pandas as pd


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



def findEncodings(images):
    encodeList = []
    
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        #writer.writerow(encode)
        #print(encode)
        encodeList.append(encode)


        with open("./Threading_for_High_FPS/Encoded.csv", 'r+') as f:
            f.truncate(0)
        np.savetxt("./Threading_for_High_FPS/Encoded.csv", encodeList,delimiter =", ", fmt ='% s')
   
    return encodeList


def encoding_reader():
    df = pd.read_csv('./Threading_for_High_FPS/Encoded.csv', delimiter=',',header=None)
    list_of_csv = [list(row) for row in df.values]
    #print(list_of_csv)
    return list_of_csv



encodeListKnown = findEncodings(images)
encodeListKnown_new = encoding_reader()
