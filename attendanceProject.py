import time
import cv2
import numpy as np
import face_recognition
from datetime import datetime
from encoding import imageEncodingsHardCode
from tkinter import *


encodeListStudents = imageEncodingsHardCode()
studentNames = []
studentEncodings = []
for student in encodeListStudents.keys():
    for encoding in encodeListStudents[student]:
        studentNames.append(student)
        studentEncodings.append(encoding)

print('Encoding Complete')

def markAttendance():
    drop.grid_forget()
    label.grid_forget()
    button.grid_forget()
    show_frames()
    Label(text= "Attendance Marked", font=("Arial", 40)).grid(row=8,column=0, pady=100)
    time.sleep(2)


def markAttendance1(name):
    with open('Computer Engineering Attendance.csv', 'r+') as f:
        attendanceList = f.readlines()
        studentNameList = []
        for line in attendanceList:
            entry = line.split('.')
            studentNameList.append(entry[0])

        # if student is not in the attendance list already
        # then mark attendance
        if name not in studentNameList:
            studentNameList.append(name)
            now = datetime.now()
            dateTimeString = now.strftime('%d/%m/%Y,%H:%M:%S')
            subject = clicked.get() or None
            f.writelines(f'\n{name},{dateTimeString},{subject}')


# Create an instance of Tkinter Window
root = Tk()
root.attributes('-fullscreen', True)
# escape using esc button
root.bind('<Escape>', lambda e: root.destroy())

root.title("EAttendance")
root.configure(background="lightblue")
Label(text="WELCOME TO COMPUTER ENGINEERING DEPARTMENT", font=("Arial", 36)).grid(row=0, column=0, pady=25, padx=80)

# Define function to open webcam and capture
def show_frames():
    cap = cv2.VideoCapture(0)
    while True:
        flag = 0
        success, img = cap.read()
        imgScaled = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgScaled = cv2.cvtColor(imgScaled, cv2.COLOR_BGR2RGB)

        # face in the current frame
        facesCurrentFrame = face_recognition.face_locations(imgScaled)
        encodingsCurrentFrame = face_recognition.face_encodings(imgScaled, facesCurrentFrame)

        # loop through all the faces found in the current frame
        for encodeFace, faceLocation in zip(encodingsCurrentFrame, facesCurrentFrame):
            matches = face_recognition.compare_faces(studentEncodings, encodeFace)
            faceDistance = face_recognition.face_distance(studentEncodings, encodeFace)
            # print(faceDistance)
            # match with lowest face distance is the best match
            matchedIndex = np.argmin(faceDistance)

            y1, x2, y2, x1 = faceLocation
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4

            if matches[matchedIndex]:
                name = studentNames[matchedIndex]
                # print(name)

                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(img, name, (x1, y2), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                markAttendance1(name)
                flag = 1
                break
            else:
                cv2.putText(img, "Face not detected", (x1, y2), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                break

        cv2.imshow('Webcam', img)
        cv2.waitKey(5000)
        # break out of loop when face is matched
        if flag == 1:
            cap.release()

            # Destroy all the windows
            cv2.destroyAllWindows()
            return


button = Button(text="Mark Attendance", command=markAttendance, fg="blue", font=("Arial", 22))

options = [
    "Parallel and Distributed Algorithms",
    "Advanced Computers Architecture",
    "Project",
    "Principles of Management",
    "Soft Computing",
    "Image Processing",
    "Other Class"
]

# datatype of menu text
clicked = StringVar()

# initial menu text
clicked.set("Parallel and Distributed Algorithms")

# Create Dropdown menu
drop = OptionMenu(root, clicked, *options)
drop.config(width=50, font = ('Arial', 18))
label = Label(text="Select Class", font=("Arial", 22), padx=30, anchor= "e", justify= "left")
label.grid(row=3, column=0, pady=25)
drop.grid(row=4, column=0, pady=25)

button.grid(row=5, column=0, pady=100)
Button(text="Exit Screen", font=("Arial, 18"), anchor=S, command=root.destroy).place(x=700, y= 750)#.grid(row= 6, column=0, pady=250)

root.mainloop()