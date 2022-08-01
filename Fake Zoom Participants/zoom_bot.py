import subprocess
from cv2 import imshow, waitKey
import pyautogui
import time
import pandas as pd
from datetime import datetime
import os
import cv2


# img = cv2.imread("./Fake Zoom Participants/join-1.png")jXm9m1
# cv2.imshow("Sheep", img)
 

def join(id, password):
    subprocess.call("C:\\Users\\rakib\\AppData\\Roaming\\Zoom\\bin\\Zoom.exe")
    time.sleep(5)

    while True:
            join1 = pyautogui.locateOnScreen('./Fake Zoom Participants/join_1.png')
            #make sure zoom app interface is opened on your primary screen

            if join1 != None:
                pyautogui.click(join1)
                print("Clicked Join 1")
                break  
            else:
                print("Could not find join 1")
                time.sleep(2)
    
    while True:
            meeting_id = pyautogui.locateOnScreen('./Fake Zoom Participants/meeting_id.png')
            #make sure zoom app interface is opened on your primary screen
            
            if meeting_id != None:
                pyautogui.click(meeting_id)
                print("Made field active")
                pyautogui.typewrite(id)
                pyautogui.click(pyautogui.locateOnScreen('./Fake Zoom Participants/join_2.png'))
                break  
            else:
                print("Could not find meeting id")
                time.sleep(2)
                 
    while True:
        meeting_pass = pyautogui.locateOnScreen('./Fake Zoom Participants/meeting_pass.png')
        #make sure zoom app interface is opened on your primary screen
        
        if meeting_pass != None:
            pyautogui.click(meeting_pass)
            print("Made field active")
            pyautogui.typewrite(password)
            pyautogui.click(pyautogui.locateOnScreen('./Fake Zoom Participants/join_3.png'))
            break  
        else:
            print("Could not find meeting password")
            time.sleep(1)
   
   
    while True:
            join_video = pyautogui.locateOnScreen('./Fake Zoom Participants/join_video.png')
            #make sure zoom app interface is opened on your primary screen
            
            if join_video != None:
                pyautogui.click(join_video)
                print("Made field active")
                #pyautogui.typewrite(password)
                pyautogui.click(pyautogui.locateOnScreen('./Fake Zoom Participants/join_video.png'))
                break  
            else:
                print("Could not find meeting password")
                time.sleep(2)



try:
    join("xxx 69x xxx","xxxx")
except:
    print("Error occured")
