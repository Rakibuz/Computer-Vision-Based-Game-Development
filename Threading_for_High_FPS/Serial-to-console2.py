import serial
import time
import matplotlib.pyplot as plt

print('Make sure you have selected correct COM & Baud rate')
# make sure the 'COM#' is set according the Windows Device Manager
ser = serial.Serial('COM14', 9600, timeout=1)
time.sleep(2)

 
for i in range(50):
    line = ser.readline()   # read a byte string
    if line:
        com_string = line.decode()  # convert the byte string to a unicode string
        #num = int(string) # convert the unicode string to an int
        print(com_string)
        if "Tag UID" in com_string:
            UID=com_string.split(':',2)
            #print(UID[1])
        elif "Found ID" in com_string:
            UID_without_=com_string.replace(" ","")
            UID=UID_without_[8]
            print(UID)
ser.close()