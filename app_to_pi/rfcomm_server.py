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
import datetime

logger = logging.getLogger()
send_list=[]

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
        self.CaptureLoad = False
        self.PLLoad = False
        self.serverSock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.clientSock = None
        self.eve = threading.Event()
        self.terminate_codon = bytes([0xFF, 0xFF, 0xFF, 0xFF])
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

    def setCaptureLoad(self):
        self.CaptureLoad=True

    def setPLLoad(self):
        self.PLLoad = True

    def LoadCaptureImage(self):
        if not self.isConnected():
            logger.error('bt is not connected')
            return False
        if not os.path.isdir(const.CAPTURED_IMAGE_PATH):
            logger.info('captured image is not exist')
            self.clientSock.send(self.terminate_codon)
            return

        capturedImageList = os.listdir(const.CAPTURED_IMAGE_PATH)
        capturedImageList.sort()

        try:
            images = capturedImageList[-1]

            with open(const.CAPTURED_IMAGE_PATH + images, 'rb') as imageFile:
                f = imageFile.read()
                b = bytearray(f)

            self.clientSock.send(len(images).to_bytes(4, byteorder='big'))
            self.clientSock.send(str.encode(images))

            self.clientSock.send(len(b).to_bytes(4, byteorder='big'))
            self.clientSock.send(bytes(b))

            logger.info('%s was sent' % (const.CAPTURED_IMAGE_PATH + images))



        except:
            self.clientSock.send(self.terminate_codon)
            return

        self.clientSock.send(self.terminate_codon)
        return True

    def LoadPhotoLog(self):
        count = 0
        folder = const.HOME_PATH+datetime.datetime.now().strftime('%y%m%d')+'/'
        PhotoLogList = os.listdir(folder)
        PhotoLogList.sort(reverse=True)

        if not os.path.isdir(folder):
            logger.info('PhotoLog is not exist')
            self.clientSock.send(self.terminate_codon)
            return
        try:
            for images in PhotoLogList:
                if os.path.isdir(images):
                    continue

                if count >= 5:
                    break

                if images in send_list:
                    count += 1
                    continue

                with open(folder + images, 'rb') as imageFile:
                    f = imageFile.read()
                    b = bytearray(f)

                self.clientSock.send(len(images).to_bytes(4, byteorder='big'))
                self.clientSock.send(str.encode(images))

                self.clientSock.send(len(b).to_bytes(4, byteorder='big'))
                self.clientSock.send(bytes(b))

                logger.info('%s was sent' % (folder + images))
                send_list.append(images)

                count += 1


        except:
            self.clientSock.send(self.terminate_codon)
            return

        self.clientSock.send(self.terminate_codon)
        return

    def run(self):
        self.serverSock.bind((self.address, self.port))
        self.serverSock.listen(1)
        self.clientSock, clientInfo = self.serverSock.accept()

        self.Connected = True

        while self.Connected:
            try:
                proc = subprocess.Popen(['hcitool', 'con'], stdout=subprocess.PIPE)

                hcitoolOutput = proc.stdout.read().decode("utf-8")
                regex = re.compile("..:..:..:..:..:..")
                paddr = regex.search(hcitoolOutput).group()

                if not paddr in hcitoolOutput: # connection failed
                    logger.warning('connection failed')
                    self.Connected = False

                if self.CaptureLoad:
                    self.LoadCaptureImage()
                    self.CaptureLoad = False

                if self.PLLoad:
                    self.LoadPhotoLog()
                    self.PLLoad = False

                ready = select.select([self.clientSock], [], [], 1) # settimeout for 1 sec
                if ready[0]:
                    rdata = self.clientSock.recv(1024).decode("utf-8") # convert b_string to string
                    msgQueue.putMsg(rdata)
                else:
                    logger.info('no data received')

            except Exception as e:
                logger.info("{}".format(str(e)))
                logger.info("{}".format(traceback.format_exc()))
                logger.info("cannot receive data")

                disconnectedMsg = '{"msg" : "%s", "value" : "%s"}' % (const.BT, const.OFF)
                msgQueue.putMsg(disconnectedMsg)

                self.Connected = False

            time.sleep(1)

        self.clientSock.close()
        self.serverSock.close()
        self.Connected = False




