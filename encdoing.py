import cv2
import face_recognition
import pickle
import os

file_path = r"C:\Users\marah\OneDrive\Desktop\directory" #image directory
PathList = os.listdir(file_path)
imgList = []
employeeId = []
# importing the employee images
for path in PathList:
    imgList.append(cv2.imread(os.path.join(file_path,path)))
    employeeId.append(os.path.splitext(path)[0])  #splitting the filename. so 'Vader.png' would turn into 'Vader'
    

def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList
print("Encoding Started")
encodeListKnown = findEncodings(imgList)
encodeListKnow_with_id = [encodeListKnown, employeeId]
print(encodeListKnown)
print("Encoding Complete") 

file = open("Encoded_image.p", 'wb')
pickle.dump(encodeListKnow_with_id,file)  #storing the encodings in a pickle
file.close()
print("File Saved")