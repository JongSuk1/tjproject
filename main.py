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
    btTh = btThread()
    btTh.start()
    camCheck = False
    msg = 'N'
    while (True):
        print("1")
        if not msgQueue.isEmpty():
            msg = msgQueue.getMsg()
            if msg == 'N':
                pass
            
            elif msg == 'BTconnected':
                soundTh=soundThread('BLE_con.mp3')
                soundTh.start()
                print("bluetooth connetion successful")
                
            elif msg == 'S':
                global camTh
                camTh = camThread()
                camTh.turnon()
                camTh.start()
                camCheck = True
                
            elif msg == 'C':
                print("C pressed\n")
                soundTh=soundThread('shutter.mp3')
                soundTh.start()
                if camCheck:
                    camTh.capture()
                else:
                    capture()
                    
            elif msg == 'Q':
                camTh.quit()
                camTh.join()
                camCheck = False
                
            elif msg == 'E':
                soundTh=soundThread('BLE_uncon.mp3')
                soundTh.start()
                print("bluetooth connection finished")
                if camTh.is_running():
                    camTh.quit()
                    camTh.join()
                soundTh.join()
                break
            
            else:
                print("msg is %s" %msg)
                
        time.sleep(1)

        
        
if __name__ == '__main__':

    controller()
    print('exit')
