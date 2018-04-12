import threading
import cv2
import os
import datetime
import time
from USB_camera.take_picture import *
from USB_camera.take_video import *
from app_to_pi.rfcomm_server import *
from switch.switch import *
import sys
import msgQueue
import play_sound.music as music
from constants import *
import logging
import logging.handlers

logger = logging.getLogger()

def set_log():
    fomatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(message)s')

    fileHandler = logging.FileHandler('tjproject.log')
    streamHandler = logging.StreamHandler()

    fileHandler.setFormatter(fomatter)
    streamHandler.setFormatter(fomatter)

    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)
    logger.setLevel(logging.INFO)


def close_Thread(thr,thList):
    try:
        thList.remove(thr)
        thr.quit()
        thr.join()
    except:
        logger.error('thread is not in threadlist')


def controller():
    thList = []

    global camTh
    global videoTh
    global switchTh

    btTh = btThread()
    btTh.start()

    switchTh = switchThread()
    switchTh.start()
    thList.append(switchTh)

    camTh = camThread()
    videoTh = videoThread()
    camCheck = False
    msg = None



    while (True):
        logger.debug('1')
        if not msgQueue.isEmpty():
            msgDict = msgQueue.getMsg()
            msg = msgDict["msg"]
            value = msgDict['value']
            
            if msg == BT_ON:
                music.play('BLE_con.mp3')
                logger.info("bluetooth connetion successful")
                
            elif msg == CAM_ON:
                if camTh.is_running():
                    logger.error('Open camera Thread is already exist')
                    continue

                camTh = camThread()
                camTh.start()
                thList.append(camTh)
                camCheck = True
                
            elif msg == CAM_CAPTURE:
                if camTh.is_running():
                    camTh.capture()
                elif videoTh.is_running():
                    videoTh.capture()
                else:
                    capture()

            elif msg == CAM_PERIOD:
                if videoTh.is_running():
                    logger.error('Cannot control period while timelapse on')
                    continue

                if not camTh.is_running():
                    logger.error('Cannot control period without camThread')
                    continue

                camTh.set_period(value)

            elif msg == CAM_QUIT:
                if not camTh.is_running():
                    logger.error('There are no open camera Thread')
                    continue

                close_Thread(camTh,thList)
                camCheck = False
                
            elif msg == TIMELAPSE_ON:
                if camTh.is_running():
                    close_Thread(camTh,thList)
                if videoTh.is_running():
                    logger.error('Open videoThread is already exist')
                    continue

                videoTh = videoThread()
                music.play('video_start.mp3')
                videoTh.start()
                thList.append(videoTh)
                
            elif msg == TIMELAPSE_OFF:
                if not videoTh.is_running():
                    logger.error('There are no open video Thread')
                    continue

                close_Thread(videoTh,thList)
                if camCheck == True:
                    camTh = camThread()
                    camTh.start()
                    thList.append(camTh)

            elif msg == BT_OFF:
                break

            else:
                # raise error and logging
                logger.error("Unknown message %s is coming" % msg)

        time.sleep(1)

    soundTh = music.play('BLE_uncon.mp3')
    for thread in thList:
        close_Thread(thread, thList)
    soundTh.join()

if __name__ == '__main__':
    set_log()
    controller()
    logger.info('exit\n')
