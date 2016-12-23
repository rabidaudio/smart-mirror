#!/usr/bin/env python2
import cv2
import time
import sys

debug = len(sys.argv) > 1 and sys.argv[1] == 'debug'

cap = cv2.VideoCapture(0)
cap.set(cv2.cv.CV_CAP_PROP_FPS, 1)

ret, frame = cap.read()

#Load a cascade file for detecting faces
#face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_alt.xml')
face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')

# source: https://github.com/Aravindlivewire/Opencv/tree/master/haarcascade
# palm_cascade = cv2.CascadeClassifier('./palm.xml')
# fist_cascade = cv2.CascadeClassifier('./fist.xml')
# closed_palm_cascase = cv2.CascadeClassifier('./closed_frontal_palm.xml')
has_faces = False

print "!c: calibrated"

while(ret):

    ret, frame = cap.read()

    #Convert to grayscale
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    #Look for faces in the image using the loaded cascade file
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    # palms = palm_cascade.detectMultiScale(gray, 1.5, 3)
    # fists = fist_cascade.detectMultiScale(gray, 1.1, 5)
    # closed_palms = closed_palm_cascase.detectMultiScale(gray, 1.1, 5)

    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),2)

    # for (x,y,w,h) in palms:
    #     cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,255),2)

    # for (x,y,w,h) in fists:
    #     cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)

    # for (x,y,w,h) in closed_palms:
    #     cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,255),2)

    if(debug):
        print str(len(faces)) + " faces"

        cv2.imshow('image', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
          break

    now_faces = (len(faces) > 0)
    if now_faces and not has_faces:
        print "!s: motionstart"
        has_faces = True
    elif has_faces and not now_faces:
        print "!e: motionend"
        has_faces = False

    #time.sleep(0.1)

cap.release()
if(debug):
    # When everything done, release the captures
    cv2.destroyAllWindows()
