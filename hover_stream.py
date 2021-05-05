import time

from djitellopy import tello
import cv2
me = tello.Tello()
me.connect()
time.sleep(1)
print(me.get_battery())

me.streamon()
# me.get_udp_video_address()
# me.get_video_capture()
me.takeoff()
print(me.is_flying)
try:
    while True:
        img = me.get_frame_read().frame
        # cv2.imwrite("img.png", img)
        img = cv2.resize(img,(360,240))
        cv2.imshow("Image", img)
        cv2.waitKey(1)
except KeyboardInterrupt:
    me.streamoff()
    me.land()
    me.end()
