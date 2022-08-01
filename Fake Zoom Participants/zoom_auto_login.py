import subprocess
import pyautogui
import time
import pandas as pd
from datetime import datetime

def sign_in(meetingid, pswd):
  
    subprocess.call("C:\\Users\\rakib\\AppData\\Roaming\\Zoom\\bin\\Zoom.exe")
    time.sleep(5)
    
    #clicks the join button
    join_1_btn = pyautogui.locateCenterOnScreen('./Fake Zoom Participants/join_1.png')
    pyautogui.moveTo(join_1_btn)
    pyautogui.click()

    # Type the meeting ID
    meeting_id_btn =  pyautogui.locateCenterOnScreen('./Fake Zoom Participants/meeting_id.png')
    pyautogui.moveTo(meeting_id_btn)
    pyautogui.click()
    pyautogui.write(meetingid)
    #time.sleep(10)

    # # Disables both the camera and the mic
    # media_btn = pyautogui.locateAllOnScreen('media_btn.png')
    # for btn in media_btn:
    #     pyautogui.moveTo(btn)
    #     pyautogui.click()
    #     time.sleep(2)

    # # Hits the join button
    # join_btn = pyautogui.locateCenterOnScreen('join_btn.png')
    # pyautogui.moveTo(join_btn)
    # pyautogui.click()
    
    # time.sleep(5)
    # #Types the password and hits enter
    # meeting_pswd_btn = pyautogui.locateCenterOnScreen('meeting_pswd.png')
    # pyautogui.moveTo(meeting_pswd_btn)
    # pyautogui.click()
    # pyautogui.write(pswd)
    # pyautogui.press('enter')



sign_in('xxxx xxx xxx','xxxx')