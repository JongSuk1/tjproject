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
import play_sound.music as music
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
    global videoTh
    btTh = btThread()
    btTh.start()
    camTh = camThread()
    videoTh = videoThread()
    camCheck = False
    msg = None

    thList = []

    while (True):
        print("1")
        if not msgQueue.isEmpty():
            msgDict = msgQueue.getMsg()
            msg = msgDict["msg"]
            value = msgDict['value']
            
            if msg == BT_ON:
                music.play('BLE_con.mp3')
                print("bluetooth connetion successful")
                
            elif msg == CAM_ON:
                camTh = camThread()
                camTh.start()
                thList.append(camTh)
                camCheck = True
                
            elif msg == CAM_CAPTURE:
                music.play('shutter.mp3')
                if camTh.is_running():
                    camTh.capture()
                elif videoTh.is_running():
                    videoTh.capture()
                else:
                    capture()

            elif msg == CAM_PERIOD:
                if videoTh.is_running():
                    print('cannot control period while timelapse on')
                if not camTh.is_running():
                    print('cannot control period without camThread')

                camTh.set_period(value)

            elif msg == CAM_QUIT:
                close_Thread(camTh,thList)
                camCheck = False
                
            elif msg == TIMELAPSE_ON:
                music.play('video_start.mp3')
                if camTh.is_running():
                    close_Thread(camTh,thList)
                videoTh = videoThread()
                videoTh.start()
                thList.append(videoTh)
                
            elif msg == TIMELAPSE_OFF:
                close_Thread(videoTh,thList)
                if camCheck == True:
                    camTh = camThread()
                    camTh.start()
                    thList.append(camTh)


            elif msg == BT_OFF:
                break
            else:
                # raise error and logging
                print("Unknown message %s is coming" % msg)

        time.sleep(1)

    soundTh = music.play('BLE_uncon.mp3')
    for thread in thList:
        close_Thread(thread, thList)
    soundTh.join()

if __name__ == '__main__':

    controller()
    print('exit')
