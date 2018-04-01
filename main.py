import threading
import cv2
import os
import datetime
import time
from USB_camera.take_picture import *
from app_to_pi.rfcomm_server import *
from play_sound.music import *

def controller():

    camTh = camThread()
    btTh = btThread()
    btTh.start()
    while (True):
        print("1")
        
        if (btTh.upstate()):
            msg = btTh.getMessage()
            if msg == 'N':
                pass
            elif msg == 'S':
                camTh.turnon()
                camTh.start()
            elif msg == 'C':
                camTh.capture()
                
            elif msg == 'Q':
                camTh.quit()
                camTh.join()
                camTh = camThread()
            else: #msg == 'E'
                camTh.quit()
                camTh.join()
                return
            btTh.downstate()
        time.sleep(1)
        
        
if __name__ == '__main__':

    controller()
    print('exit')
