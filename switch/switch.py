import RPi.GPIO as GPIO
import time
import threading
import sys
sys.path.insert(0, '/home/pi/tjproject/msgQueue')
sys.path.insert(0, '/home/pi/tjproject/constants')
import msgQueue
import constants as const
import logging

logger = logging.getLogger()


def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23,GPIO.IN)
    GPIO.setup(24,GPIO.IN)
    GPIO.setup(14,GPIO.OUT)
    GPIO.setup(15,GPIO.OUT)
    GPIO.setup(17,GPIO.OUT)

setup()

def white_blink():
    GPIO.output(15,True)
    time.sleep(0.2)
    GPIO.output(15,False)

def on(color):
    if color == 'green':
        GPIO.output(14,True)
    elif color == 'red':
        GPIO.output(17,True)
    else:
        logger.error('wrong led color')

def off(color):
    if color == 'green':
        GPIO.output(14,False)
    elif color == 'red':
        GPIO.output(17,False)
    elif color == 'all':
        GPIO.output(14, False)
        GPIO.output(15, False)
        GPIO.output(17, False)
    else:
        logger.error('wrong led color')

class switchThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.set = True

    def run(self):
        prev = GPIO.input(23)
        while (self.set):
            video_click = GPIO.input(23)
            cap_click = GPIO.input(24)
            if cap_click:
                cap_clickMsg = '{"msg" : "%s", "value" : "%s"}' % (const.CAM_CAPTURE, const.NOTHING)
                msgQueue.putMsg(cap_clickMsg)
                time.sleep(1)

            if (not prev) and video_click:
                video_clickMsg = '{"msg" : "%s", "value" : "%s"}' % (const.TIMELAPSE_ON, const.NOTHING)
                msgQueue.putMsg(video_clickMsg)
                time.sleep(0.2)

            if prev and (not video_click):
                video_clickMsg = '{"msg" : "%s", "value" : "%s"}' % (const.TIMELAPSE_OFF, const.NOTHING)
                msgQueue.putMsg(video_clickMsg)
                time.sleep(0.2)

            time.sleep(0.1)
            prev = video_click
        GPIO.cleanup()

    def video_state(self):
        return GPIO.input(23)

    def quit(self):
        self.set = False