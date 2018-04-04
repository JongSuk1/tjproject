import threading
import cv2
import os
import datetime
import time
from USB_camera.take_picture import *
from app_to_pi.rfcomm_server import *
from play_sound.music import *
import sys
sys.path.insert(0, '/home/pi/tjproject/msgQueue')
import msgQueue
def controller():
    camTh = camThread()
    btTh = btThread()
    btTh.start()
    msg = 'N'
    while (True):
        print("1")
        if not msgQueue.isEmpty():
            msg = msgQueue.getMsg()
            if msg == 'N':
                pass
            elif msg == 'BTconnected':
                print("bluetooth connetion successful")
            elif msg == 'S':
                camTh.turnon()
                camTh.start()
            elif msg == 'C':
                print("C pressed\n")
                camTh.capture()                
            elif msg == 'Q':
                camTh.quit()
                camTh.join()
                camTh = camThread()
            elif msg == 'E':
                print("bluetooth connection finished")
#                camTh.quit()
#                camTh.join()
                break
            else:
                print("msg is %s" %msg)
        time.sleep(1)

        
        
if __name__ == '__main__':

    controller()
    print('exit')
