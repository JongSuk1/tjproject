#
# 180327 Jaylen
# This is test code proceding following tasks :
# 1. pi camera captures #PHOTOCOUNT images every time_delay sec.
# 2. send it into phone of address 'address with BT opex protocol
# 3. phone user should push 'accept' button for each send request from pi

  

import subprocess
import os
import picamera
import time

address = "1C:AF:05:90:F1:6C@12"
camera = picamera.PiCamera()
PHOTOCOUNT = 5
photo_index = 0
time_delay = 1

#BT auto pairing

#photo shoot
while photo_index < PHOTOCOUNT :
	camera.capture("image%d.jpg"%photo_index, resize = (320,240))
	photo_index = photo_index + 1
	time.sleep(time_delay)
	print("%d th image captured"%photo_index)

print("capture done")


for i in range(1,PHOTOCOUNT):
	filename = "image{}.jpg".format(i)
	path_to_file = os.path.join("/home/pi/Jaylen",filename)
	cmd = ["ussp-push", address, path_to_file, filename]
	subprocess.call(" ".join(cmd), shell=True)

print("image sent")




