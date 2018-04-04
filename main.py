import threading
import cv2
import os
import datetime
import time
from USB_camera.take_picture import *
from app_to_pi.rfcomm_server import *
from play_sound.music import *
import sys
sys.path.insert(0, '/Users/kakao/tjproject/msgQueue')
import msgQueue

def controller():
    msgQ = msgQueue.msgQ()
    camThread = camThread()
    btThread = btThread()
    btThread.start()
    while (True):
        print("1")
        
        if not msgQ.isEmpty():
            msg = msgQ.getMsg()
            if msg == 'N':
                pass
            elif msg == 'S':
                camThread.turnon()
                camThread.start()
            elif msg == 'C':
                camThread.capture()                
            elif msg == 'Q':
                camThread.quit()
                camThread.join()
                camThread = camThread()
            elif msg == 'E':
                break
            else:
                pass
        time.sleep(1)
        
        
if __name__ == '__main__':

    controller()
    print('exit')
