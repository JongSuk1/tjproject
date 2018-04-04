import bluetooth
import threading
import serial
import sys
sys.path.insert(0, '/Users/kakao/tjproject/msgQueue')
import msgQueue

class btThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.address = "B8:27:EB:9E:6F:5E"
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
        rdata = 'N' # 'N' for None and is default
        while rdata != 'E':#'E' for exit
            try:
                rdata = clientSock.recv(1024)
                msgQ.putMsg(rdata)
                print("got message %s" %rdata)

            except:
                print("cannot receive data")
                break
        self.serverSock.close()
        self.Connected = False
        print("btThread finished")



