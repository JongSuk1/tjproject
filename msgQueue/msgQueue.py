import queue
    


msgQ = queue.Queue()

def putMsg(Msg):
    msgQ.put(Msg)

def getMsg():
    if not msgQ.empty():
        msg =  msgQ.get()
        print(msg)
        msgList = msg.split('_',1)
        print("%s has popped from msgQ\n" %(msgList[0]))
        return msgList
    else:
        print("msgQ is empty")
        return None

def isEmpty():
    return msgQ.empty()
