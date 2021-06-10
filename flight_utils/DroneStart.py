from djitellopy import tello



class DroneStart:
    def __init__(self):
        self.me = tello.Tello()
        self.me.connect()
        print("BATTERY IS ", self.me.get_battery())