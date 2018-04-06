import bluetooth
import threading
import serial
import sys
import subprocess
import re
sys.path.insert(0, '/home/pi/tjproject/msgQueue')
sys.path.insert(0, '/home/pi/tjproject/constants')
import msgQueue
from constants import *

def get_baddr():
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

    def run(self):
        self.serverSock.bind((self.address, self.port))
        self.serverSock.listen(1)
        clientSock, clientInfo = self.serverSock.accept()
        self.Connected = True
        msgQueue.putMsg(BT_ON)
        rdata = None # 'N' for None and is default
        while rdata != BT_OFF :# BT_OFF for disconnecting bluetooth
            try:
                rdata = clientSock.recv(1024).decode("utf-8") # convert b_string to string
                print(rdata)
                msgQueue.putMsg(rdata)
                print("got message %s" %rdata)

            except:
                print("cannot receive data")
                break
        self.serverSock.close()
        self.Connected = False
        msgQueue.putMsg(BT_OFF)



