import bluetooth
import threading
import serial
import sys
import subprocess
import re
import os
sys.path.insert(0, '/home/pi/tjproject/msgQueue')
sys.path.insert(0, '/home/pi/tjproject/constants')
import msgQueue
from constants import *
import cv2
import logging

logger = logging.getLogger()

def get_baddr():
    if not os.path.exists('hciconfig.txt'):
        subprocess.call('hciconfig > hciconfig.txt', shell=True)
    hciInfo = open('hciconfig.txt','r').read()
    regex = re.compile("..:..:..:..:..:..")
    baddr = regex.search(hciInfo).group()
    return baddr

class btThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.address = get_baddr()
        self.port = 1
        self.Connected = False
        self.serverSock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.clientSock = None

    def __del__(self):
        self.serverSock.close()

    def setAddr(self, addr):
        self.address = addr

    def setPort(self, port):
        self.port = port

    def isConnected(self):
        return self.Connected
    

    def getMessage(self):
        return self.message

    def startLoadingImage(self):
        if not self.isConnected():
            logger.error('bt is not connected')
            return False
        if not os.path.isdir(CAPTURED_IMAGE_PATH):
            logger.error('cannot find \'myimage\' folder')
            return False
        
        capturedImageList = os.listdir(CAPTURED_IMAGE_PATH)
        capturedImageList.sort()

        for images in capturedImageList:
            img = cv2.imread(images, cv2.IMREAD_COLOR)
# resize
            cv2.resize(img, None, fx=0.1, fy=0.1, interpolation=cv2.INTER_AREA)
            b = cv2.imencode('.jpg', img).tostring()
            self.clientSock.send(b)
            logger.info('%s was sent' % images)
        return True
        

    def run(self):
        self.serverSock.bind((self.address, self.port))
        self.serverSock.listen(1)
        self.clientSock, clientInfo = self.serverSock.accept()
        self.Connected = True

        self.startLoadingImage()


        self.clientSock.close()
        self.serverSock.close()
        self.Connected = False

print('start')
btTh = btThread()
btTh.start()
btTh.join()

