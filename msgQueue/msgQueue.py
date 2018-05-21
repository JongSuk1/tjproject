import queue
import json   
import logging

msgQ = queue.Queue()
logger = logging.getLogger()

def putMsg(Msg):
    Msg_array = Msg.split('}{')
    for message in Msg_array:
        if not message.startswith('{'):
            message = '{' + message

        if not message.endswith('}'):
            message = message + '}'

        msgQ.put(message)
    logger.info("got message %s" % Msg)


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
