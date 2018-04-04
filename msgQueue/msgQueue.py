import queue

global msgQ

class msgQ(queue.Queue):
    def __init__(self):
        queue.Queue.__init__(self)

    def putMsg(self, Msg):
        self.put(Msg)

    def getMsg(self):
        if not self.isEmpty():
            msg =  self.get()
            print("%s has popped from msgQ\n" %(msg))
            return msg
        else:
            print("msgQ is empty")
            return None

    def isEmpty(self):
        return self.empty()

    def size(self):
        return self.qsize()

if __name__ == "__main__":
    msg = msgQ()
    msg.putMsg("yyy")
    msg.putMsg("nnn")
    print(msg.size())
    msg.getMsg()
    msg.getMsg()
    print(msg.size())
    print(msg.isEmpty())

