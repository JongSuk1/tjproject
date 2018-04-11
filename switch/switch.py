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
    GPIO.setup(24,GPIO.IN)

class switchThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.set = True

    def run(self):
        setup()
        while (self.set):
            click = GPIO.input(24)
            if click:
                clickMsg = '{"msg" : "%s", "value" : "%s"}' % (CAM_CAPTURE, NOTHING)
                msgQueue.putMsg(clickMsg)
                logger.info("got message %s"%clickMsg)
                time.sleep(1)

            time.sleep(0.1)


    def quit(self):
        self.set = False