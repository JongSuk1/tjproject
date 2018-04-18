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
import constants as const
import cv2
import logging
import time

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
        if not os.path.isdir(const.CAPTURED_IMAGE_PATH):
            logger.error('cannot find \'myimage\' folder')
            return False

        capturedImageList = os.listdir(const.CAPTURED_IMAGE_PATH)
        capturedImageList.sort()

        for images in capturedImageList:
            with open(const.CAPTURED_IMAGE_PATH + images, 'rb') as imageFile:
                f = imageFile.read()
                b = bytearray(f)

            self.clientSock.send(len(images).to_bytes(4, byteorder='big'))
            self.clientSock.send(str.encode(images))

            self.clientSock.send(len(b).to_bytes(4, byteorder='big'))
            self.clientSock.send(bytes(b))
            #time.sleep(0.1)

            print('%s was sent' % (const.CAPTURED_IMAGE_PATH + images))

        terminate_codon = bytes([0xFF, 0xFF, 0xFF, 0xFF])
        self.clientSock.send(terminate_codon)
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

