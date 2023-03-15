import cv2
import face_recognition
import pickle
import os

# Importing  images
folderPath = './Face_Recognition_with_RealTime_Database/Images'
pathList = os.listdir(folderPath)
print(pathList)
imgList = []
employeeIds = []
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    employeeIds.append(os.path.splitext(path)[0])

print(len(imgList))