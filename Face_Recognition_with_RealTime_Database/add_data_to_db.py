import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("./Face_Recognition_with_RealTime_Database/xxxxx.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://xxxx.com/"
    })

ref = db.reference('Employees')


data={
    "432":
    {
      "Name":"Abdul Zabbar Al Naeem",
      "ID":"432",
      "Dept":"EEE R&D",
      "Company":"Tesla Lab",
      "Total_attendance":6,
      "Last_attendance_time":"2023-03-11 00:54:34"
    },
     "466":
    {
      "Name":"Md.Jobayer",
      "ID":"432",
      "Dept":"EEE R&D",
      "Company":"Tesla Lab",
      "Total_attendance":7,
      "Last_attendance_time":"2023-03-15 00:45:34"
    },
      "465":
    {
      "Name":"Md.Rabiul Islam",
      "ID":"465",
      "Dept":"EEE R&D",
      "Company":"Tesla Lab",
      "Total_attendance":4,
      "Last_attendance_time":"2023-03-15 00:35:34"
    },
    "381":
    {
      "Name":"Md Rakibuz Sultan",
      "ID":"381",
      "Dept":"EEE R&D",
      "Company":"Tesla Lab",
      "Total_attendance":2,
      "Last_attendance_time":"2023-03-16 00:25:34"
    },
    "380":
    {
      "Name":"Shikder Mejbah Ahmed Mubin",
      "ID":"380",
      "Dept":"EEE R&D",
      "Company":"Tesla Lab",
      "Total_attendance":9,
      "Last_attendance_time":"2023-03-16 00:1:34"
    }
    
}

for key, value in data.items():
    ref.child(key).set(value)