#FaceTracking'
import cv2
import numpy as np


def findFace(img):
	faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
	imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	faces = faceCascade.detectMultiScale(imgGray, 1.2, 8.0)

	myFaceListC = []
	myFaceListArea = []

	for (x,y,w,h) in faces:
		

cap = cv2.VideoCapture(0)

while True:
	_, img = cap.read()
	cv2.imshow("Output", img)
	cv2.waitKey(1)

