import queue
import json   
import logging

msgQ = queue.Queue()
logger = logging.getLogger()

def putMsg(Msg):
    msgQ.put(Msg)

def getMsg():
    if not msgQ.empty():                                                                                                                                  
        msg =  msgQ.get()
        msgDict = json.loads(msg)
        return msgDict
    else:
        logger.info("msgQ is empty")
        return None

def isEmpty():
    return msgQ.empty()
