from DroneStart import DroneStart
import cv2




class ImageStream(DroneStart):
    def __init__(self):
        super().__init__()

    def stream(self):
        self.me.streamon()
        img = self.me.get_frame_read().frame
        return img

    def test_stream(self):
        img = self.stream()
        img = cv2.resize(img, (360, 240))
        cv2.imshow("image", img)
        cv2.waitKey(1)