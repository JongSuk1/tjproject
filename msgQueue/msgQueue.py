import queue

msgQ = queue.Queue()


def putMsg(Msg):
    msgQ.put(Msg)

def getMsg():
    if not msgQ.empty():
        msg =  msgQ.get()
        print("%s has popped from msgQ\n" %(msg))
        return msg
    else:
        print("msgQ is empty")
        return None

def isEmpty():
    return msgQ.empty()
