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
sys.path.insert(0, '/home/pi/tjproject/msgQueue')
import msgQueue

logger = logging.getLogger()

def setup():
    capture = cv2.VideoCapture(0)
    folder, video_name = make_name()
    if not os.path.isdir(folder):
        os.mkdir(folder)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(folder+ '/'+video_name, fourcc, 20.0, (640, 480))
    return capture,out


def make_name():
    video_name = datetime.datetime.now().strftime('%y%m%d-%H%M%S%f') + '.avi'
    folder = const.HOME_PATH+'myvideo'
    return folder, video_name

def store_img(folder, img_name, frame):
    if frame == None:
        return
    if not os.path.isdir(folder):
       os.mkdir(folder)
    cv2.imwrite(folder+'/'+img_name, frame)



class videoThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.frame = None
        self.set = False

    def run(self):
        self.set = True
        capture, out = setup()
        ret, self.frame = capture.read()

        while (self.set and self.frame != None):
            ret, self.frame = capture.read()
            frame = cv2.flip(self.frame,1)
            out.write(frame)

        capture.release()
        out.release()
        cv2.destroyAllWindows()

    def capture(self):
        img_name = datetime.datetime.now().strftime('%y%m%d-%H%M%S%f')+'.jpg'
        music.play('shutter.mp3')
        store_img(const.CAPTURED_IMAGE_PATH, img_name, self.frame)

        LDmsg = '{"msg" : "%s", "value" : "%s"}' % (const.LD_IMAGE, const.CAM_CAPTURE)
        msgQueue.putMsg(LDmsg)

    def quit(self):
        self.set = False

    def is_running(self):
        return self.set