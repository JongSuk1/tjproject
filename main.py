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
        logger.debug('1')
        if not msgQueue.isEmpty():
            msgDict = msgQueue.getMsg()
            msg = msgDict["msg"]
            value = msgDict['value']
            
            if msg == BT_ON:
                music.play('BLE_con.mp3')
                logger.info("bluetooth connetion successful")
                
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
                    logger.error('cannot control period while timelapse on')
                if not camTh.is_running():
                    logger.error('cannot control period without camThread')

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

            elif msg == LD_IMAGE: #do something
                if btTh.isConnected() :
                    if not btTh.startLoadingImage() :
                        logger.error('loading images failed')
                        break
                else :
                    logger.error('bluetooth is not connected')
                    break

            else:
                # raise error and logging
                logger.error("Unknown message %s is coming" % msg)
                break

        time.sleep(1)

    soundTh = music.play('BLE_uncon.mp3')
    for thread in thList:
        close_Thread(thread, thList)
    soundTh.join()

if __name__ == '__main__':
    set_log()
    controller()
    logger.info('exit\n')
