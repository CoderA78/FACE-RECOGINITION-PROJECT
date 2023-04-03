import face_recognition
import cv2
import csv
import numpy as np
from datetime import datetime

video_capture= cv2.VideoCapture(1)

# Load known Faces

anup_image= face_recognition.load_image_file("Faces/anup.jpeg")
anup_encoding= face_recognition.face_encodings(anup_image)[0]

arpita_image= face_recognition.load_image_file("Faces/arpita.jpeg")
arpita_encoding= face_recognition.face_encodings(arpita_image)[0]

known_face_encodings=[arpita_encoding, anup_encoding]
known_faces_names= ["Arpita", "Anup"]

#list of expected students
students= known_faces_names.copy()

face_locations=[]

face_encodings=[]

#get the current date and time
now= datetime.now()
current_date= now.strftime("%d-%m-%y")

f= open(f"{current_date}.csv", "w", newline="")
lineWriter= csv.writer(f)

while True:
    _, frame= video_capture.read()
    small_frame=cv2.resize(frame,(0,0), fx=0.25,fy=0.25)
    rgb_small_frame= cv2.cvtColor(small_frame,cv2.COLOR_BGR2RGB)

    #Recognize faces
    face_locations= face_recognition.face_locations(rgb_small_frame)
    face_encodings=face_recognition.face_encodings(rgb_small_frame, face_locations)

    for face_encoding in face_encodings:
        matches= face_recognition.compare_faces(known_face_encodings, face_encoding)
        face_distance= face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index= np.argmin(face_distance)

        if matches[best_match_index]:
            name=known_faces_names[best_match_index]

        #Add the text if the person is present
        if name in known_faces_names:
            font = cv2.FONT_HERSHEY_SIMPLEX
            bottomLeftCornerOfText = (10,100)
            fontScale=1.5
            fontColor= (255,0,0)
            thickness=3
            lineType=2
            cv2.putText(frame,name+"Present", bottomLeftCornerOfText, font, fontScale, fontColor, thickness, lineType)
        
        if name in students:
            students.remove(name)
            current_time=now.strftime("%H-%M-%S")
            lineWriter.writerow([name, current_time])


        cv2.imshow("Attendence", frame)
        if cv2.waitKey(1) & 0xFF==ord("q"):
            break

video_capture.release()
cv2.destroyAllWindows()
f.close()