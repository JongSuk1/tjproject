import bluetooth
import threading
import serial


class btThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.address = "B8:27:EB:9E:6F:5E"
		self.port = 1
		self.Connected = False
		self.message = 'N'
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

		while True:
			rdata = clientSock.recv(1024)
			if rdata == 'S':#start
				print(rdata)
				self.message = 'S'
			elif rdata == 'C':#capture
				print(rdata)
				self.message = 'C'
			elif rdata == 'Q':#quit
				self.message = 'Q'

# echo
			clientSock.send(rdata)
		self.serverSock.close()
		self.Connected = False
	


