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
    GPIO.setup(const.VID_SWITCH,GPIO.IN)
    GPIO.setup(const.CAP_SWITCH,GPIO.IN)
    GPIO.setup(const.GREEN,GPIO.OUT)
    GPIO.setup(const.WHITE,GPIO.OUT)
    GPIO.setup(const.RED,GPIO.OUT)
    GPIO.setup(const.BLUE,GPIO.OUT)

setup()

def blink(color):
    GPIO.output(color,True)
    time.sleep(0.2)
    GPIO.output(color,False)

def on(color):
    GPIO.output(color,True)


def off(color):
    if color == 'all':
        GPIO.output(const.GREEN, False)
        GPIO.output(const.WHITE, False)
        GPIO.output(const.RED, False)
        GPIO.output(const.BLUE, False)
        return
    GPIO.output(color,False)

class switchThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.set = True
        setup()

    def run(self):
        prev = GPIO.input(const.VID_SWITCH)
        while (self.set):
            video_click = GPIO.input(const.VID_SWITCH)
            cap_click = GPIO.input(const.CAP_SWITCH)
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
        return GPIO.input(const.VID_SWITCH)

    def quit(self):
        self.set = False