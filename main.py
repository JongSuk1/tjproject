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
import constants as const
import logging
import logging.handlers

logger = logging.getLogger()

def set_log():
    fomatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(message)s')

    fileHandler = logging.FileHandler(const.HOME_PATH+'tjproject.log')
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

    btTh = btThread()
    btTh.start()

    period = '10'
    camTh = camThread(period)
    camTh.start()
    thList.append(camTh)
    camCheck = True

    videoTh = videoThread()
    music.play('setup.mp3')

    while (True):
        logger.debug('Main Thread running')
        if not msgQueue.isEmpty():
            msgDict = msgQueue.getMsg()
            msg = msgDict["msg"]
            value = msgDict['value']
            
            if msg == const.BT:
                if value == const.ON:
                    music.play('BLE_con.mp3')

                elif value == const.OFF:
                    soundTh = music.play('BLE_uncon.mp3')
                    for thread in thList:
                        close_Thread(thread, thList)
                    soundTh.join()

                    logger.info('BT connection released\n')

                    # reset
                    btTh = btThread()
                    btTh.start()

                    camTh = camThread(period)
                    videoTh = videoThread()
                    camCheck = False

                else:
                    logger.error('BT message cannot have other value')


            elif msg == const.CAM_CAPTURE:
                if camTh.is_running():
                    camTh.capture()
                elif videoTh.is_running():
                    videoTh.capture()
                else:
                    capture()


            elif msg == const.CAM_PERIOD:
                if value == const.ON:
                    if camTh.is_running():
                        logger.error('Open camera Thread is already exist')
                        continue

                    if videoTh.is_running():
                        logger.critical('camTh cannot open while videoTh is running')
                        continue


                    camTh = camThread(period)
                    camTh.start()
                    thList.append(camTh)
                    camCheck = True

                elif value == const.OFF:
                    if not camTh.is_running():
                        logger.error('There are no open camera Thread')
                        continue

                    close_Thread(camTh, thList)
                    camCheck = False

                else:
                    if videoTh.is_running():
                        logger.error('Cannot control period while timelapse on')
                        continue

                    if not camTh.is_running():
                        logger.error('Cannot control period without camThread')
                        continue

                    period = value
                    camTh.set_period(period)


            elif msg == const.CAM_VIDEO:
                if value == const.ON:
                    if camTh.is_running():
                        close_Thread(camTh, thList)
                    if videoTh.is_running():
                        logger.error('Open videoThread is already exist')
                        continue

                    videoTh = videoThread()
                    music.play('video_start.mp3')
                    videoTh.start()
                    thList.append(videoTh)

                elif value == const.OFF:
                    if not videoTh.is_running():
                        logger.error('There are no open video Thread')
                        continue

                    close_Thread(videoTh, thList)
                    if camCheck == True:
                        camTh = camThread(period)
                        camTh.start()
                        thList.append(camTh)

                else:
                    logger.error('Video message cannot have other value')


            elif msg == const.LD_IMAGE:
                if value == const.CAM_CAPTURE:
                    btTh.setCaptureLoad()
                elif value == const.CAM_PERIOD:
                    btTh.setPLLoad()
                elif value == '2':
                    logger.debug('Raspberry pi cannot spend video yet')
                else:
                    logger.error('LD_IMAGE message cannot have other value')

            else:
                # raise error and logging
                logger.error("Unknown message %s is coming" % msg)
                break

        time.sleep(1)


if __name__ == '__main__':
    set_log()
    controller()
    logger.info('exit\n')
