#FaceTracking
# Based off of https://github.com/juanmapf97/Tello-Face-Recognition/blob/master/face_recognition/main.py
from flight_utils.ImageCapture import ImageStream
import cv2
import time


class FaceTrack(ImageStream):
    def __init__(self):
        super().__init__()
        self.forward_backward_range = [6200, 6800]
        self.w, self.h = 360, 240
        self.pError = 0
        self.face_cascade = cv2.CascadeClassifier("ml_resources/haarcascade_frontalface_default.xml")

    def find_face(self):
        """
        Finds faces in frame

        :return: None
        """
        print("attempting to find face....")
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

        # while len(faces) == 0:
        #     self.rotate_in_place()
        #     faces = self.face_cascade.detectMultiScale(gray, 1.3, minNeighbors=5)

        face_center_x = center_x
        face_center_y = center_y
        z_area = 0
        for face in faces:
            print("Face Found!")
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

        self.adjust_tello_position(offset_x, offset_y, z_area)

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

    def adjust_tello_position(self, offset_x, offset_y, offset_z):
        """
            Adjusts the position of the tello drone based on the offset values given from the frame
            :param offset_x: Offset between center and face x coordinates
            :param offset_y: Offset between center and face y coordinates
            :param offset_z: Area of the face detection rectangle on the frame
        """
        print("adjusting drone position")

        if not -90 <= offset_x <= 90 and offset_x is not 0:
            if offset_x < 0:
                self.me.rotate_counter_clockwise(10)
            elif offset_x > 0:
                self.me.rotate_clockwise(10)

        if not -70 <= offset_y <= 70 and offset_y is not -30:
            if offset_y < 0:
                self.me.move_up(20)
            elif offset_y > 0:
                self.me.move_down(20)

        if not 15000 <= offset_z <= 30000 and offset_z is not 0:
            if offset_z < 15000:
                self.me.move_forward(20)
            elif offset_z > 30000:
                self.me.move_back(20)

    def rotate_in_place(self):
        print("rotating.......")
        self.me.rotate_counter_clockwise(10)

    def track(self):

        # cap = cv2.VideoCapture(0)
        self.stream()
        self.me.takeoff()
        self.me.send_rc_control(0, 0, 20, 0)
        time.sleep(2.2)
        while True:
            self.find_face()
            if cv2.waitKey(1) == ord('q'):
                break

        self.me.land()
        self.me.end()
        cv2.destroyAllWindows()

