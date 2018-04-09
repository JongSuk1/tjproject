import queue
import json   


msgQ = queue.Queue()

def putMsg(Msg):
    msgQ.put(Msg)

def getMsg():
    if not msgQ.empty():                                                                                                                                  
        msg =  msgQ.get()
        print(msg)
        msgDict = json.loads(msg)
        print("%s has popped from msgQ\n" %(msgDict["msg"]))
        return msgDict
    else:
        print("msgQ is empty")
        return None

def isEmpty():
    return msgQ.empty()
