import bluetooth
import threading
import serial
import sys
import traceback
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
        self.eve = threading.Event()

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

#        self.eve.clear()

        for images in capturedImageList:
            img = cv2.imread(const.CAPTURED_IMAGE_PATH + images, cv2.IMREAD_COLOR)
            logger.debug('%s %s' % (const.CAPTURED_IMAGE_PATH, images))

            tf, encodedImgByte = cv2.imencode('.jpg', img)
            # lenImgByte = len(encodedImgByte)
            if tf:
                print(len(encodedImgByte))
                self.clientSock.send(str.encode(images))
                time.sleep(1)
                self.clientSock.send(encodedImgByte)
                time.sleep(1)
                self.clientSock.send(str.encode('end of image'))
                time.sleep(1)
            print('%s was sent' % (const.CAPTURED_IMAGE_PATH + images))

#        self.eve.set()
        return

    def run(self):
#        self.eve.set()
        self.serverSock.bind((self.address, self.port))
        self.serverSock.listen(1)
        self.clientSock, clientInfo = self.serverSock.accept()
        self.Connected = True

        connectedMsg = '{"msg" : "%s", "value" : "%s"}' %(const.BT_ON, const.NOTHING)
        msgQueue.putMsg(connectedMsg)
        rdata = None

        while rdata != const.BT_OFF:
#            self.eve.wait()
            try:
                rdata = self.clientSock.recv(1024).decode("utf-8") # convert b_string to string
                msgQueue.putMsg(rdata)
            except Exception as e:
                #logger.warning("{}".format(str(e)))
                #logger.warning("{}".format(traceback.format_exc()))
                #logger.warning("cannot receive data")
                break
            time.sleep(0.1)
        self.clientSock.close()
        self.serverSock.close()
        self.Connected = False




