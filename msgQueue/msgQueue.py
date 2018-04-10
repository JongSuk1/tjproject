import queue
import json   


msgQ = queue.Queue()

def putMsg(Msg):
    msgQ.put(Msg)

def getMsg():
    if not msgQ.empty():                                                                                                                                  
        msg =  msgQ.get()
        msgDict = json.loads(msg)
        return msgDict
    else:
        print("msgQ is empty")
        return None

def isEmpty():
    return msgQ.empty()
