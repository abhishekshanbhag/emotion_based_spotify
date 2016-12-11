#!/usr/bin/env python
import cv2
from os import listdir

def detect(img, cascade):
    rects = []
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags = cv2.CASCADE_SCALE_IMAGE)
    if len(rects) == 0:
        rects = list([])
    else:
        rects[:,2:] += rects[:,:2]
    return rects

cascade_fn = "face_detection_files/haarcascades/haarcascade_frontalface_alt.xml"
cascade = cv2.CascadeClassifier(cascade_fn)

img = cv2.imread('face_detection_files/IMG_4311.JPG')
#cv2.imshow('image', img)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#cv2.imshow('gray', gray)
#gray = cv2.equalizeHist(gray)
rects = detect(gray, cascade)
if(len(rects)):
    i = 0
    biggest_sz = 0
    biggest_index = 0
    for x1, y1, x2, y2 in rects:
        temp_face = gray[y1:y2, x1:x2]
        sz1 = (y2-y1)*(x2-x1)
        if sz1 > biggest_sz:
            biggest_sz = sz1
            biggest_index = i
        i = i+1
    x1, y1, x2, y2 = rects[biggest_index]
    roi = gray[y1:y2, x1:x2]
else:
    roi = gray
    print('face not detected. Please click from another angle of lighting.')
roi = cv2.equalizeHist(roi)
roi = cv2.resize(roi, (48, 48))
cv2.imshow('facedetect', roi)
cv2.waitKey(0)

#cv2.destroyAllWindows()

