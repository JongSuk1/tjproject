import threading
import cv2
import os
import datetime
from USB_camera.take_picture import *
from app_to_pi.rfcomm_server import *
from play_sound.music import *

if __name__ == '__main__':
    thlist = []
    camTh = camThread()
    btTh = btThread()
    btTh.start()
    while (True):
        if (btTh.upstate()):
            msg = btTh.getMessage()
            if msg == 'N':
                pass
            elif msg == 'S':
                camTh.start()
                camTh.turnon()
            elif msg == 'C':
                camTh.capture()
                
            elif msg == 'Q':
                camTh.quit()
            else:
                break;
            btTh.downstate()

# camTh = camThread()
# camTh.start()
# 
# 
# camTh.join()
# 
print('exit')
