#FaceTracking
from ImageCapture import ImageStream
import cv2
import numpy as np



class FaceTrack(ImageStream):
	def __init__(self):
		super().__init__()
		self.forward_backward_range = [6200, 6800]
		self.pid = [0.4, 0.4, 0]
		self.w, self.h = 360, 240
		self.pError = 0

	def findFace(self, img):
		faceCascade = cv2.CascadeClassifier("/ml_resources/haarcascade_frontalface_default.xml")
		imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		faces = faceCascade.detectMultiScale(imgGray, 1.2, int(8))

		myFaceListC = []
		myFaceListArea = []

		for (x,y,w,h) in faces:
			cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
			cx = x + w/2
			cy = y + h/2
			area = w * h
			cv2.circle(img, (int(cx), int(cy)), 5, (0, 255, 0), cv2.FILLED)
			myFaceListC.append([cx, cy])
			myFaceListArea.append(area)

		if len(myFaceListC) != 0:
			i = myFaceListArea.index(max(myFaceListArea))
			return img, [myFaceListC[i], myFaceListArea[i]]
		else:
			return img, [[0, 0], 0]


	def trackFace(self, info):

		area = info[1]
		x, y = info[0]

		#Find how far off from the center we are
		error = x - self.w//2
		yaw_speed = self.pid[0] * error + self.pid[1] * (error - self.pError)
		yaw_speed = int(np.clip(yaw_speed, -100, 100))

		forward_backward = 0
		if area > self.forward_backward_range[1]:
			forward_backward = -20
		elif area < self.forward_backward_range[0] and area != 0:
			forward_backward = 20

		if x == 0:
			yaw_speed = 0
			error = 0

		self.me.send_rc_control(0, forward_backward, 0, yaw_speed)
		return error

	def track(self):

		# cap = cv2.VideoCapture(0)
		self.stream()
		while True:
			# _, img = cap.read()
			img = self.me.get_frame_read().frame
			img = cv2.resize(img, (self.w, self.h))
			img, info = self.findFace(img)
			self.pError = self.trackFace(info)
			print("Center ", info[0], "area ", info[1])
			cv2.imshow("Output", img)
			cv2.waitKey(1)



