from djitellopy import tello
from time import sleep


me = tello.Tello()
me.connect()
print(me.get_battery())
me.takeoff()
sleep(10)
# me.send_rc_control(0,50,0,0)
try:
    me.flip_back()
    me.flip_right()
    me.flip_forward()
except:
    pass
sleep(2)
me.send_rc_control(0,0,0,0)

me.land()