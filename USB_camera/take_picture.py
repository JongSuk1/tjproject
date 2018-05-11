# Take video from camera and show it
import cv2
import os
import datetime
import threading
import time
import logging
import sys
sys.path.insert(0, '/home/pi/tjproject')
import play_sound.music as music
sys.path.insert(0, '/home/pi/tjproject/constants')
import constants as const

logger = logging.getLogger()

def store_img(folder, img_name, frame):
    if frame == None:
        return
    if not os.path.isdir(folder):
       os.mkdir(folder)
    cv2.imwrite(folder+'/'+img_name, frame)


def setup():

    capture = cv2.VideoCapture(0)
    logger.debug('image width %d' % capture.get(3))
    logger.debug('image height %d' % capture.get(4))

    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    return capture

def capture():
    cap = setup()

    music.play('beep.mp3')
    time.sleep(0.3)
    music.play('beep.mp3')
    time.sleep(0.3)

    ret, frame = cap.read()
    music.play('shutter.mp3')
    folder, img_name = make_name()
    store_img(const.CAPTURED_IMAGE_PATH, img_name, frame)

def make_name():
    img_name = datetime.datetime.now().strftime('%y%m%d-%H%M%S%f')+'.jpg'
    folder = const.HOME_PATH+datetime.datetime.now().strftime('%y%m%d')
    return folder, img_name


class camThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.frame = None
        self.set = False
        self.clock = 0
        self.period = 50
        self.cap = None

    def run(self):
        self.set = True
        self.cap = setup()

        while(self.set):
            ret, self.frame = self.cap.read()
            time.sleep(0.1)
            self.clock = self.clock+1
            if self.clock % self.period == 0:
                folder, img_name = make_name()
                store_img(folder, img_name, self.frame)

        self.cap.release()
        cv2.destroyAllWindows() 
        logger.debug('camera closed')

    def capture(self):
        folder, img_name = make_name()
        ret, self.frame = self.cap.read()
        music.play('shutter.mp3')
        store_img(const.CAPTURED_IMAGE_PATH, img_name, self.frame)
       
    def quit(self):
        self.set = False

    def is_running(self):
        return self.set
    
    def set_period(self,period):
        self.period = int(period) * 10
        self.clock = 0

