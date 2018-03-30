import bluetooth
import threading
import serial


class btThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
	self.address = "B8:27:EB:E6:9F:B8"
	self.port = 1
	self.Connected = False
	self.message = 'N'
	self.serverSock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.state = False
                
    def __del__(self):
	self.serverSock.close()
	
    def upstate(self):
        return self.state
            
    def downstate(self):
        self.state = False
            
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
	
	while True:
            clientSock.settimeout(1)
            try:
                rdata = clientSock.recv(1024)
                self.state=True
                if rdata == 'S':#start
                    print(rdata)
                    self.message = 'S'
                elif rdata == 'C':#capture
                    print(rdata)
                    self.message = 'C'
                elif rdata == 'Q':#quit
                    self.message = 'Q'
            except:
                pass
	self.serverSock.close()
	


