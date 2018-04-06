# Take video from camera and show it
import cv2
import os
import datetime
import threading
import time

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
    folder = 'myvideo'
    return folder, video_name


class videoThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.frame = None
        self.set = True

    def run(self):
        capture, out = setup()
        while (self.set):
            ret, self.frame = capture.read()
            frame = cv2.flip(self.frame,0)
            out.write(frame)
        capture.release()
        out.release()
        cv2.destroyAllWindows()

    def turnon(self):
        self.set = True

    def quit(self):
        self.set = False

    def is_running(self):
        return self.set