#!/usr/bin/env python2
import cv2
import numpy as np
from time import time

threshold = 5
minMotion = 2
motionTimeout = 15

cap = cv2.VideoCapture(0)

ret, frame = cap.read()

gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
avg = gray.copy().astype("float")

# http://www.pyimagesearch.com/2015/06/01/home-surveillance-and-motion-detection-with-the-raspberry-pi-python-and-opencv/
sensingMotion = False
lastMotion = 0

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

  t = time()
  if m > minMotion:
    if not sensingMotion:
      sensingMotion = True
      print("motionstart")

    lastMotion = t
  else:
    if sensingMotion and (t - lastMotion) > motionTimeout:
      print("motionend")
      sensingMotion = False
  # (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  # for c in cnts:
  #   if cv2.contourArea(c) > 50:
  #     (x, y, w, h) = cv2.boundingRect(c)
  #     cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

  # diff = gray - background
  # e = cv2.erode(np.float8(diff), 5)
  # t, diff = cv2.threshold((gray - background), 0, 255, cv2.THRESH_BINARY_INV)

  # dist = cv2.distanceTransform(diff, cv2.cv.CV_DIST_L2, 5)

  cv2.imshow('image', thresh)
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

  background = gray

  # time.sleep(1)
  # t = time()
  # end = t + period
  # while t < end:
  #   cap.grab()
  #   t = time()

cap.release()
cv2.destroyAllWindows()
