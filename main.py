import threading
import cv2
import os
import datetime
import time
from USB_camera.take_picture import *
from app_to_pi.rfcomm_server import *
from play_sound.music import *
import sys
import msgQueue
from constants import *


def controller():
    btTh = btThread()
    btTh.start()
    while (True):
        print("1")
        if not msgQueue.isEmpty():
            msg = msgQueue.getMsg()
            elif msg == BT_ON:
                soundTh=soundThread('BLE_con.mp3')
                soundTh.start()
                print("bluetooth connetion successful")
            elif msg == CAM_ON:
                camTh = camThread()
                camTh.turnon()
                camTh.start()
            elif msg == CAM_CAPTURE:
                print("C pressed\n")
                soundTh=soundThread('shutter.mp3')
                soundTh.start()
                camTh.capture()                
            elif msg == CAM_QUIT:
                camTh.quit()
                camTh.join()
            elif msg == BT_OFF:
                soundTh=soundThread('BLE_uncon.mp3')
                soundTh.start()
                print("bluetooth connection finished")
                if camTh.is_running()               
                    camTh.quit()
                    camTh.join()
                break
            else:
                print("msg is %s" %msg)
        time.sleep(1)

        
        
if __name__ == '__main__':

    controller()
    print('exit')
