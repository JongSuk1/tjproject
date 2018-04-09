import threading
import cv2
import os
import datetime
import time
from USB_camera.take_picture import *
from USB_camera.take_video import *
from app_to_pi.rfcomm_server import *
import sys
import msgQueue
import play_sound as music
from constants import *


def close_Thread(thr,thList):
    try:
        thList.remove(thr)
        thr.quit()
        thr.join()
    except:
        print('thread is not in threadlist')



def controller():
    global camTh
    btTh = btThread()
    btTh.start()
    camTh = camThread()
    # camCheck = False
    msg = None

    thList = []

    while (True):
        print("1")
        if not msgQueue.isEmpty():
            msgList = msgQueue.getMsg()
            msg = msgList[0]
            print(msgList)
            
            if msg == BT_ON:
                music.play_music('BLE_con.mp3')
                print("bluetooth connetion successful")
                
            elif msg == CAM_ON:
                camTh = camThread()
                camTh.start()
                thList.append(camTh)
                camCheck = True
                
            elif msg == CAM_CAPTURE:
                music.play_music('shutter.mp3')
                if camCheck:
                    camTh.capture()
                else:
                    capture()

            elif msg == CAM_PERIOD:
                camTh.set_period(value)

            elif msg == CAM_QUIT:
                close_Thread(camTh,thList)
                camCheck = False
                
            elif msg == TIMELAPSE_ON:
                music.play_music('video_start.mp3')
                if camCheck == True:
                    close_Thread(camTh,thList)
                videoTh = videoThread()
                videoTh.start()
                thList.append(videoTh)
                
            elif msg == TIMELAPSE_OFF:
                close_Thread(videoTh,thList)
                if camCheck == True:
                    camTh = camThread()
                    camTh.start()


            elif msg == BT_OFF:
                music.play_music('BLE_uncon.mp3')
                print("bluetooth connection finished")
                for thread in thList:
                    close_Thread(thread,thList)
                soundTh.join()
                break

            else:
                # raise error and logging
                print("Unknown message %s is coming" % msg)

        time.sleep(1)
        
if __name__ == '__main__':

    controller()
    print('exit')
