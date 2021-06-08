#FaceTracking
# Based off of https://github.com/juanmapf97/Tello-Face-Recognition/blob/master/face_recognition/main.py
from ImageCapture import ImageStream
import cv2
import numpy as np
import time


class FaceTrack(ImageStream):
    def __init__(self):
        super().__init__()
        self.forward_backward_range = [6200, 6800]
        self.pid = [0.4, 0.4, 0]
        self.w, self.h = 360, 240
        self.pError = 0
        self.face_cascade = cv2.CascadeClassifier("ml_resources/haarcascade_frontalface_default.xml")

    def findFace(self):

        #Get frame
        frame = self.me.get_frame_read().frame

        #Get video capture
        cap = self.me.get_video_capture()

        #Calculate frame center
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        center_x = int(width/2)
        center_y = int(height/2)

        #Draw in the center of the frame
        cv2.circle(frame, (center_x, center_y), 10, (0, 255, 0))

        #Convert frame to grayscale in order to apply haar cascade
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, minNeighbors=5)

        myFaceListC = []
        myFaceListArea = []

        face_center_x = center_x
        face_center_y = center_y
        for face in faces:
            (x, y, w, h) = face
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 0), 2)

            face_center_x = x + int(h/2)
            face_center_y = y + int(w/2)
            z_area = w*h

            cv2.circle(frame, (face_center_x, face_center_y), 10, (0, 0, 255))


        # Calculate recognized face offset from center
        offset_x = face_center_x - center_x
        # add 30 so drone can see more
        offset_y = face_center_y - center_y - 30

        cv2.putText(frame, f'[{offset_x}, {offset_y}, {z_area}]', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255),
                   2, cv2.LINE_AA)

        self.track(offset_x, offset_y, z_area)

        cv2.imshow('Tello TrackFace_V2', frame)
        # @deprecated
        # for (x, y, w, h) in faces:
        #     cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
        #     cx = x + w/2
        #     cy = y + h/2
        #     area = w * h
        #
        #     myFaceListC.append([cx, cy])
        #     myFaceListArea.append(area)
        #
        # if len(myFaceListC) != 0:
        #     i = myFaceListArea.index(max(myFaceListArea))
        #     return img, [myFaceListC[i], myFaceListArea[i]]
        # else:
        #     return img, [[0, 0], 0]
        #

    def track(self, offset_x, offset_y, z_area):

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
        self.me.takeoff()
        self.me.send_rc_control(0, 0, 15, 0)
        time.sleep(2.2)
        while True:
            self.findFace()
            if cv2.waitKey(1) == ord('q'):
                break

        self.me.land()
        self.me.end()
        cv2.destroyAllWindows()

