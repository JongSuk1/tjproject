import threading
import cv2
import os
import datetime
from USB_camera.take_picture import *
from play_sound.music import *

eve = threading.Event()


th = cameraThread()
th.start()


th.join()

print('exit')