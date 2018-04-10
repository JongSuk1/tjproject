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

        connectedMsg = '{"msg" : "%s", "value" : "%s"}' %(BT_ON, NOTHING)
        msgQueue.putMsg(connectedMsg)
        rdata = None

        while rdata != BT_OFF :
            try:
                rdata = clientSock.recv(1024).decode("utf-8") # convert b_string to string
                msgQueue.putMsg(rdata)
                print("got message %s" %rdata)

            except:
                print("cannot receive data")
                break

        self.serverSock.close()
        self.Connected = False

        disconnectedMsg =  '{"msg" : "%s", "value" : "%s"}' %(BT_OFF, NOTHING)
        msgQueue.putMsg(disconnectedMsg)



