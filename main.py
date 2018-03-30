import threading
import cv2
import os
import datetime
from USB_camera.take_picture import *
from app_to_pi.rfcomm_server import *
from play_sound.music import *


eve = threading.Event()

btTh = btThread()
btTh.start()

while True:
	if btTh.isConnected:
		print(btTh.getMessage())
	else:
		print("not connected")
	time.sleep(1)
	

btTh.join()



# camTh = cameraThread()
# camTh.start()
# 
# 
# camTh.join()
# 
print('exit')
