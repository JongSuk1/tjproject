import RPi.GPIO as GPIO
import time
import threading
import sys
sys.path.insert(0, '/home/pi/tjproject/msgQueue')
sys.path.insert(0, '/home/pi/tjproject/constants')
import msgQueue
from constants import *
import logging

logger = logging.getLogger()


def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23,GPIO.IN)
    GPIO.setup(24,GPIO.IN)

class switchThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.set = True
        setup()

    def run(self):
        prev = GPIO.input(23)
        while (self.set):
            video_click = GPIO.input(23)
            cap_click = GPIO.input(24)
            if cap_click:
                cap_clickMsg = '{"msg" : "%s", "value" : "%s"}' % (CAM_CAPTURE, NOTHING)
                msgQueue.putMsg(cap_clickMsg)
                time.sleep(1)

            if (not prev) and video_click:
                video_clickMsg = '{"msg" : "%s", "value" : "%s"}' % (TIMELAPSE_ON, NOTHING)
                msgQueue.putMsg(video_clickMsg)
                time.sleep(0.2)

            if prev and (not video_click):
                video_clickMsg = '{"msg" : "%s", "value" : "%s"}' % (TIMELAPSE_OFF, NOTHING)
                msgQueue.putMsg(video_clickMsg)
                time.sleep(0.2)

            time.sleep(0.1)
            prev = video_click

    def video_state(self):
        return GPIO.input(23)

    def quit(self):
        self.set = False