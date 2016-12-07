#!/usr/bin/env python
import cv2


def detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags = cv2.CASCADE_SCALE_IMAGE)
    if len(rects) == 0:
        rects = []
    rects[:,2:] += rects[:,:2]
    return rects


cascade_fn = "face_detection_files/haarcascades/haarcascade_frontalface_alt.xml"
cascade = cv2.CascadeClassifier(cascade_fn)
img = cv2.imread('face_detection_files/20110204.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.equalizeHist(gray)
rects = detect(gray, cascade)
if(len(rects)):
    for x1, y1, x2, y2 in rects:
        roi = gray[y1:y2, x1:x2]
else:
    roi = gray

#cv2.imshow('facedetect', roi)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
