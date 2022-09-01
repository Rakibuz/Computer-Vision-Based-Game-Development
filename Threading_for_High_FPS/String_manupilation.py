from datetime import datetime
import csv


url = "https://www.exaple.com/index.php?id=24124"
id_number = url.split('=')[1]
print(type(id_number))
print(id_number)
if(id_number=='24124'):
    print('hello')


name=id_number
now = datetime.now()
Str_time = now.strftime("%H:%M:%S")
Str_day = now.strftime("%m/%d/%Y")
user=[name,Str_time,Str_day]

#print(type(user))
myFile = open('./Threading_for_High_FPS/Attendance.csv', 'r+')
writer = csv.writer(myFile)
writer.writerow(user)
#myFile.close()