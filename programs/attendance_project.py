'''
        AUTOMATIC ATTENDANCE MONITORING SYSTEM USING FACE RECOGNITION IN PYTHON
            
            STEP 1 : Encode the image of the person whose attendance needed to be taken 
            STEP 2 : Encode the frames generated from the webcam
            STEP 3 : Compare the encodings if both are same then mark the attendance of the person with the time
            STEP 4 : Store the name of the person in an Excel sheet

'''
import face_recognition
import cv2
import numpy as np
import os
from datetime import datetime

video_capture = cv2.VideoCapture(0)

image1 = face_recognition.load_image_file(os.path.abspath("C:\\Users\\Arularasi\\Google Drive\\MY FILES\\ifet college_files\\Mini project files\\Automatic Attendance Monitoring System using Face Recognition\\mini project source code\\images\\arul.jpg"))
image1_face_encoding = face_recognition.face_encodings(image1)[0]

image2 = face_recognition.load_image_file(os.path.abspath("C:\\Users\\Arularasi\\Google Drive\\MY FILES\\ifet college_files\\Mini project files\\Automatic Attendance Monitoring System using Face Recognition\\mini project source code\\images\\abi.jpg"))
image2_face_encoding = face_recognition.face_encodings(image2)[0]

known_face_encodings = [
    image1_face_encoding,
    image2_face_encoding
]
known_face_names = [
    "Arul",
    "Abu"
]

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

# Function to mark the attendance of the student
def mark_attendance(name):
                with open ("C:\\Users\\Arularasi\\Google Drive\\MY FILES\\ifet college_files\\Mini project files\\Automatic Attendance Monitoring System using Face Recognition\\mini project source code\\attendance.csv","r+") as f:
                    my_data_list = f.readlines()
                    print(my_data_list)
                    name_list = []
                    for line in my_data_list:
                        entry = line.split(',')
                        name_list.append(entry[0])

                    if name not in name_list:
                        now = datetime.now()
                        dtString = now.strftime("%H:%M:%S")
                        f.writelines(f'\n{name},{dtString}') 



while True:
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]
    print(rgb_small_frame)
    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)
            name = "Unknown"
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            face_names.append(name)

            

    process_this_frame = not process_this_frame
    print ("Face detected -- {}".format(face_names))
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.6, (255, 255, 255), 1)
        mark_attendance('arularasi')
        
    cv2.imshow('Attendance', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()


