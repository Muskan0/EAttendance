import ast
import time
from datetime import datetime
from tkinter import *
from tkinter import messagebox

import cv2
import face_recognition
import numpy as np

from encoding import imageEncodingsHardCode

root = Tk()
root.title("EAttendance")
root.geometry('925x500')
root.configure(bg='#fff')
root.resizable(False, False)


def signin():
    username = user.get()
    password = passCode.get()

    file = open('data.txt', 'r')
    d = file.read()
    r = ast.literal_eval(d)
    file.close()

    if username in r.keys() and password == r[username]:

        global headcount

        encodeListStudents = imageEncodingsHardCode()
        studentNames = []
        studentEncodings = []
        # for student in encodeListStudents.keys():
        #     for encoding in encodeListStudents[student]:
        #         studentNames.append(student)
        #         studentEncodings.append(encoding)

        for student in encodeListStudents.keys():
            studentNames.append(student)
            studentEncodings.append(encodeListStudents[student][0])
        print('Encoding Complete')

        def markAttendance():
            show_frames()
            finalmsg = Label(screen, text="(Mark Another Student or exit)", fg='#57a1f8', bg='white',
                             font=('Helvetica', 18, 'bold'))
            finalmsg.place(x=50, y=450)
            time.sleep(2)

        def markAttendance1(name):
            global headcount
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
                    headcount += 1
                    Label(screen, text=str(headcount), fg="#57a1f8", bg="white", font=('Helvetica', 12, 'bold')).place(
                        x=30, y=150)
                    # messagebox.showinfo('Attendance Marked', 'Attendance of Student ' + name + ' Marked for class ' + subject)

        # Create an instance of Tkinter Window
        screen = Toplevel(root)
        root.withdraw()
        # screen.attributes('-fullscreen', True)
        screen.title("EAttendance")
        screen.geometry('925x500')
        screen.configure(bg='#fff')
        screen.resizable(False, False)
        # escape using esc button
        screen.bind('<Escape>', lambda e: screen.destroy())

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
                if facesCurrentFrame is None or facesCurrentFrame == [] or encodingsCurrentFrame == []:
                    continue
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
                        subject = clicked.get() or None
                        markAttendance1(name)

                        flag = 1
                        break
                    else:
                        cv2.putText(img, "Face not found", (x1, y2), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                        break

                cv2.imshow('Webcam', img)
                cv2.waitKey(5000)
                # break out of loop when face is matched
                if flag == 1:
                    messagebox.showinfo('Attendance Marked',
                                        'Attendance of Student ' + name + ' Marked for class ' + subject)
                    cap.release()

                    # Destroy all the windows
                    cv2.destroyAllWindows()
                    return

        headcount = 0
        frame = Frame(screen, width=800, height=400, bg="white")
        frame.place(x=80, y=50)
        heads = Label(screen, text="Head count", fg="#57a1f8", bg="white", font=('Helvetica', 15, 'bold'))
        heads.place(x=30, y=100)

        Label(screen, text=str(headcount), fg="#57a1f8", bg="white", font=('Helvetica', 12, 'bold')).place(x=30, y=150)
        heading = Label(frame, text="DEPARTMENT OF COMPUTER ENGINEERING", fg='#57a1f8', bg='white',
                        font=('Helvetica', 23, 'bold'))
        heading.place(x=90, y=5)

        # Label(text="WELCOME TO COMPUTER ENGINEERING DEPARTMENT", font=("Arial", 36)).grid(row=0, column=0, pady=25, padx=80)

        label = Label(frame, text="Select Course:", font=('Helvetica', 14, 'bold'), fg='#57a1f8', bg='white').place(
            x=120,
            y=100)
        Button(frame, width=50, pady=7, text='Mark Attendance', command=markAttendance, bg='#57a1f8', fg='white',
               border=0,
               font=('Helvetica', 14, 'bold')).place(x=120, y=280)

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
        drop = OptionMenu(frame, clicked, *options)
        drop.config(width=50, font=('Helvetica', 14, 'bold'))
        drop.place(x=120, y=140)

        def exitScreen():
            screen.destroy()
            root.destroy()
        Button(screen, text="Exit Screen", font=('Helvetica', 14, 'bold'), bg='#57a1f8', fg='white',
               command=exitScreen).place(x=700, y=450)

        screen.mainloop()
    else:
        messagebox.showerror("Invalid", "invalid username or password")


def register_command():
    window = Toplevel(root)
    window.title("EAttendance")
    window.geometry('925x500')
    window.configure(bg='#fff')
    window.resizable(False, False)

    def register():
        username = user.get()
        password = passCode.get()
        confirm_password = confirmpassCode.get()

        if password == confirm_password:
            # print("yo")
            try:
                file = open('data.txt', 'r+')
                d = file.read()
                r = ast.literal_eval(d)

                dict2 = {username: password}
                r.update(dict2)
                file.truncate(0)
                file.close()

                file = open('data.txt', 'w')
                w = file.write(str(r))

                messagebox.showinfo('register', 'Successfully registered')
                window.destroy()
            except:
                file = open('data.txt', 'w')
                p = str({'username': 'password'})
                file.write(p)
                file.close()

        else:
            messagebox.showerror('Invalid', 'Both password should match')

    def sign():
        window.destroy()

    img = PhotoImage(file='loginPage.png')
    Label(window, image=img, bg='white').place(x=50, y=90)
    frame = Frame(window, width=350, height=390, bg="white")
    frame.place(x=480, y=50)

    heading = Label(frame, text="Register", fg='#57a1f8', bg='white', font=('Helvetica', 23, 'bold'))
    heading.place(x=100, y=5)

    def on_enter(e):
        user.delete(0, 'end')

    def on_leave(e):
        name = user.get()
        if name == '':
            user.insert(0, 'Username')

    user = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Helvetica', 11))
    user.place(x=30, y=80)
    user.insert(0, 'Username')
    Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)
    user.bind('<FocusIn>', on_enter)
    user.bind('<FocusOut>', on_leave)

    def on_enter(e):
        passCode.delete(0, 'end')

    def on_leave(e):
        password = passCode.get()
        if password == '':
            passCode.insert(0, 'Password')

    passCode = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Helvetica', 11))
    passCode.place(x=30, y=150)
    passCode.insert(0, 'Password')
    Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)
    passCode.bind('<FocusIn>', on_enter)
    passCode.bind('<FocusOut>', on_leave)

    def on_enter(e):
        confirmpassCode.delete(0, 'end')

    def on_leave(e):
        confirmpassword = confirmpassCode.get()
        if confirmpassword == '':
            confirmpassCode.insert(0, 'Confirm Password')

    confirmpassCode = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Helvetica', 11))
    confirmpassCode.place(x=30, y=220)
    confirmpassCode.insert(0, 'Confirm Password')
    Frame(frame, width=295, height=2, bg='black').place(x=25, y=247)
    confirmpassCode.bind('<FocusIn>', on_enter)
    confirmpassCode.bind('<FocusOut>', on_leave)

    Button(frame, width=39, pady=7, text='Register', bg='#57a1f8', fg='white', border=0, command=register).place(x=35,
                                                                                                                 y=280)
    label = Label(frame, text="I have an account", fg="black", bg="white", font=('Helvetica', 9))
    label.place(x=90, y=340)

    sign_up = Button(frame, width=6, text="Sign in", border=0, bg="white", fg='#57a1f8', cursor='hand2', command=sign)
    sign_up.place(x=200, y=340)

    window.mainloop()


img = PhotoImage(file='loginPage.png')
Label(root, image=img, bg='white').place(x=50, y=90)
frame = Frame(root, width=350, height=350, bg="white")
frame.place(x=480, y=70)

heading = Label(frame, text="Sign in", fg='#57a1f8', bg='white', font=('Helvetica', 23, 'bold'))
heading.place(x=100, y=5)


def on_enter(e):
    user.delete(0, 'end')


def on_leave(e):
    name = user.get()
    if name == '':
        user.insert(0, 'Username')


user = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Helvetica', 11))
user.place(x=30, y=80)
user.insert(0, 'Username')
Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)


def on_enter(e):
    passCode.delete(0, 'end')


def on_leave(e):
    password = passCode.get()
    if password == '':
        passCode.insert(0, 'Password')


passCode = Entry(frame, show="*", width=25, fg='black', border=0, bg='white', font=('Helvetica', 11))
passCode.place(x=30, y=150)
passCode.insert(0, 'Password')
Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)
passCode.bind('<FocusIn>', on_enter)
passCode.bind('<FocusOut>', on_leave)

Button(frame, width=39, pady=7, text='Sign in', bg='#57a1f8', fg='white', border=0, command=signin).place(x=35, y=204)
label = Label(frame, text="Dont have an account?", fg="black", bg="white", font=('Helvetica', 9))
label.place(x=75, y=270)

sign_up = Button(frame, width=6, text="Sign up", border=0, bg="white", fg='#57a1f8', cursor='hand2',
                 command=register_command)
sign_up.place(x=215, y=270)

root.mainloop()
