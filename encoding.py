import os
import cv2
import face_recognition
from numpy import array

def imageEncodingsHardCode():
    # generated encodings from imageEncodings()
    # and hardcoded it to improve the efficiency of the application
    # The encodings will be migrated to the database sooner.
    return # return encodings of students in dictionary form


def imageEncodings():
    path = 'images'
    myList = os.listdir(path)
    print(myList)
    student = dict()

    for i in myList:
        tempPath = path + '\\' + i
        studentImage = os.listdir(tempPath)
        student[i] = list()
        for j in studentImage:
            # print(tempPath + '\\' + j)

            img = face_recognition.load_image_file(tempPath+'\\'+j)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            try:
                encode = face_recognition.face_encodings(img)[0]
                print(encode)
                student[i].append(encode)

            except IndexError:
                print("File name:", tempPath + '\\' + j)
    return student
