import bluetooth
import threading
import serial
import sys
import traceback
import subprocess
import re
import os
import select
sys.path.insert(0, '/home/pi/tjproject/msgQueue')
sys.path.insert(0, '/home/pi/tjproject/constants')
import msgQueue
import constants as const
import cv2
import logging
import time

logger = logging.getLogger()
send_list=[]

def get_baddr():
    if not os.path.exists('hciconfig.txt'):
        subprocess.call('hciconfig > hciconfig.txt', shell=True)
    hciInfo = open('hciconfig.txt','r').read()
    regex = re.compile("..:..:..:..:..:..")
    baddr = regex.search(hciInfo).group()
    return baddr

def refresh_list():
    f = open(const.HOME_PATH + 'send_imagelist.txt', 'r')
    while True:
        line=f.readline()
        if not line:
            break
        x = line.split('\n')
        send_list.append(x[0])


class btThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.address = get_baddr()
        self.port = 1
        self.Connected = False
        self.serverSock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.clientSock = None
        self.eve = threading.Event()
        file = open(const.HOME_PATH + 'send_imagelist.txt', 'a')
        file.close()

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
            logger.info('captured image is not exist')
            terminate_codon = bytes([0xFF, 0xFF, 0xFF, 0xFF])
            self.clientSock.send(terminate_codon)
            return

        capturedImageList = os.listdir(const.CAPTURED_IMAGE_PATH)
        capturedImageList.sort()

        refresh_list()

        file = open(const.HOME_PATH + 'send_imagelist.txt', 'a')

        for images in capturedImageList:
            if images in send_list:
                continue

            with open(const.CAPTURED_IMAGE_PATH + images, 'rb') as imageFile:
                f = imageFile.read()
                b = bytearray(f)

            self.clientSock.send(len(images).to_bytes(4, byteorder='big'))
            self.clientSock.send(str.encode(images))

            self.clientSock.send(len(b).to_bytes(4, byteorder='big'))
            self.clientSock.send(bytes(b))
            #time.sleep(0.1)

            print('%s was sent' % (const.CAPTURED_IMAGE_PATH + images))

            file.write(images+'\n')

        file.close()

        terminate_codon = bytes([0xFF, 0xFF, 0xFF, 0xFF])
        self.clientSock.send(terminate_codon)
        return True

    def run(self):
#        self.eve.set()
        self.serverSock.bind((self.address, self.port))
        self.serverSock.listen(1)
        self.clientSock, clientInfo = self.serverSock.accept()
        regex = re.compile("..:..:..:..:..:..")
        clientAaddr = regex.search(clientInfo).group()

        self.Connected = True

        connectedMsg = '{"msg" : "%s", "value" : "%s"}' %(const.BT_ON, const.NOTHING)
        msgQueue.putMsg(connectedMsg)
        print(self.clientSock)
        rdata = None

        while rdata != const.BT_OFF:
            print(self.clientSock)
#            self.eve.wait()
            try:
                proc = subprocess.Popen(['hcitool', 'con'], stdout=subprocess.PIPE)
                hcitoolOutput = proc.stdout.read()
                if not clientAddr in hcitoolOutput: # connection failed
                    logger.warning('connection failed')
                    rdata = const.BT_OFF

                self.clientSock.setblocking(0)
                ready = select.select([self.clientSock], [], [], 1) # settimeout for 1 sec
                if ready[0]:
                    rdata = self.clientSock.recv(1024).decode("utf-8") # convert b_string to string
                    msgQueue.putMsg(rdata)
                else:
                    logger.info('no data received')
            except Exception as e:
                #logger.warning("{}".format(str(e)))
                #logger.warning("{}".format(traceback.format_exc()))
                #logger.warning("cannot receive data")
                break
            time.sleep(1)
        self.clientSock.close()
        self.serverSock.close()
        self.Connected = False




