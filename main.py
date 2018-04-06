import threading
import cv2
import os
import datetime
import time
from USB_camera.take_picture import *
from USB_camera.take_video import *
from app_to_pi.rfcomm_server import *
from play_sound.music import *
import sys
import msgQueue
from constants import *


def controller():
    btTh = btThread()
    btTh.start()
    camCheck = False
    msg = None
    thList = []
    while (True):
        print("1")
        if not msgQueue.isEmpty():
            msg, value = msgQueue.getMsg()

            if msg == None:
                pass
            
            elif msg == BT_ON:
                soundTh=soundThread('BLE_con.mp3')
                soundTh.start()
                print("bluetooth connetion successful")
                
            elif msg == CAM_ON:
                global camTh
                camTh = camThread()
                camTh.start()
                thList.append(camTh)
                camCheck = True
                
            elif msg == CAM_CAPTURE:
                soundTh=soundThread('shutter.mp3')
                soundTh.start()
                if camCheck:
                    camTh.capture()
                else:
                    capture()

            elif msg == CAM_PERIOD:
                camTh.set_period(value)

            elif msg == CAM_QUIT:
                camTh.quit()
                camTh.join()
                camCheck = False
                
            elif msg == TIMELAPSE_ON:
                soundTh = soundThread('video_start.mp3')
                soundTh.start()
                if camCheck == True:
                    camTh.quit()
                    camTh.join()
                videoTh = videoThread()
                videoTh.start()
                thList.append(videoTh)
                
            elif msg == TIMELAPSE_OFF:
                videoTh.quit()
                videoTh.join()
                if camCheck == True:
                    camTh = camThread()
                    camTh.start()


            elif msg == BT_OFF:
                soundTh=soundThread('BLE_uncon.mp3')
                soundTh.start()
                print("bluetooth connection finished")
                for thread in thList:
                    thread.quit()
                    thread.join()
                soundTh.join()
                break

            else:
                print("msg is %s" %msg)

        time.sleep(1)
        
if __name__ == '__main__':

    controller()
    print('exit')
