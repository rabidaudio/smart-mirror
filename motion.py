#!/usr/bin/env python2
import cv2
import numpy as np
from time import time

# period = 5

# http://www.pyimagesearch.com/2015/06/01/home-surveillance-and-motion-detection-with-the-raspberry-pi-python-and-opencv/

threshold = 5
minMotion = 2

cap = cv2.VideoCapture(0)

ret, frame = cap.read()

gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
avg = gray.copy().astype("float")

sensingMotion = False

while(ret):

  ret, frame = cap.read()
  #Convert to grayscale
  gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
  gray = cv2.GaussianBlur(gray, (21, 21), 0)

  cv2.accumulateWeighted(gray, avg, 0.5)
  frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))

  thresh = cv2.threshold(frameDelta, threshold, 255, cv2.THRESH_BINARY)[1]
  thresh = cv2.dilate(thresh, None, iterations=2)
  m = np.mean(thresh)

  newMotion = m > minMotion
  if newMotion and not sensingMotion:
    sensingMotion = True
    print("motionstart")
  elif not newMotion and sensingMotion:
    print("motionend")
    sensingMotion = False

  cv2.imshow('image', thresh)
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

  # time.sleep(1)
  # t = time()
  # end = t + period
  # while t < end:
  #   cap.grab()
  #   t = time()

cap.release()
cv2.destroyAllWindows()
