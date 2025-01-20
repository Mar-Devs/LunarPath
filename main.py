import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone
from cvs_logic import write_to_csv
from datetime import datetime
from datetime import datetime, timedelta

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

file_path = r"C:\Users\marah\OneDrive\Desktop\directory"
modePathList = os.listdir(file_path)
imgModeList = []
# importing images into a list
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(file_path,path)))

# loading the 'encoded_image' file
file = open('Encoded_image.p','rb')
encodeListKnownWithIds = pickle.load(file )
file.close()
encodeListKnown, employeeIds = encodeListKnownWithIds

last_logged_time = {}  # Tracks the last logged time for each employee
COOLDOWN_PERIOD = timedelta(seconds=30)  # Cooldown period (e.g., 30 seconds)

while True:
    success , img = cap.read()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)
    face_current_frame = face_recognition.face_locations(imgS)
    encode_current_frame = face_recognition.face_encodings(imgS,face_current_frame)
    
    for encode_face, faceLoc in zip(encode_current_frame, face_current_frame):
         matches = face_recognition.compare_faces(encodeListKnown, encode_face)
         face_distance = face_recognition.face_distance(encodeListKnown, encode_face)
         # print(face_distance)


         matchIndex = np.argmin(face_distance)

         if matches[matchIndex]:
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4

            bbox = (x1, y1, x2 - x1, y2 - y1)  # x, y, width, height

            img = cvzone.cornerRect(img, bbox, rt=0, colorR=(0, 255, 0), colorC=(0, 255, 0)) #rectangle code

            employeeId = employeeIds[matchIndex]  #label with employeeId
            cvzone.putTextRect(img, f"ID: {employeeId}", (x1, y1 - 10), scale=1, thickness=1, colorR=(0, 255, 0))

            current_time = datetime.now()

            # Cooldown check
            if employeeId not in last_logged_time or (current_time - last_logged_time[employeeId]) > COOLDOWN_PERIOD:
                # Log the recognized employee
                current_date = current_time.strftime("%d-%m-%Y")
                log_time = current_time.strftime("%H:%M:%S")  
                work_start_datetime = datetime.combine(current_time.date(), datetime.strptime("08:00:00", "%H:%M:%S").time())
                time_difference = current_time - work_start_datetime

                if time_difference <= timedelta(minutes=45):
                   status = "On Time"
                else:
                   status = "Late"
                
                action = "Clocking In"
                status = f"{action} ({status})"

                write_to_csv(employeeId, current_date, log_time, status)

                # Update last logged time for this employee
                last_logged_time[employeeId] = current_time

         
   
              


    cv2.imshow("Webcam",img) #webcam code 
    cv2.waitKey(1)