from datetime import datetime
import json
from byteutils import *
import base64

IO_MESSAGE_VERSION = 4

class IoMessage:
    def __init__(self):
        self.id = None
        self.tag = None
        self.groupid = None
        self.version = IO_MESSAGE_VERSION
        self.timestamp = datetime.now()
        self.sequencenumber = None
        self.sequencetotal = None
        self.priority = None
        self.timestamp = None
        self.publisher = None
        self.authid = None
        self.authgroup = None
        self.chainposition = None
        self.hash = None
        self.previoushash = None
        self.nonce = None
        self.difficultytarget = None
        self.infotype = None
        self.infoformat = None
        self.contextdata = None
        self.contentdata = None

        #1 byte: id, tag, groupId, seqnum, seqtotal, priority, timestamp, publisher, chainpos, diftarget,infoformat, infortype
        #4 byte: context data, content data

def message2bytes(msg):
    bHeadArr = bytearray()
    bDatArr = bytearray()
    bMsgArr = bytearray()
    #version
    bHeadArr.extend(int2two_bytes(msg.version))
    #id
    if msg.id is not None:
        bHeadArr.extend(int2one_bytes(len(msg.id)))
        bDatArr.extend(str2bytes(msg.id))
    else:
        bHeadArr.extend(int2one_bytes(0))
    #tag
    if msg.tag is not None:
        bHeadArr.extend(int2two_bytes(len(msg.tag)))
        bDatArr.extend(str2bytes(msg.tag))
    else:
        bHeadArr.extend(int2two_bytes(0))
    #group id
    if msg.groupid is not None:
        bHeadArr.extend(int2one_bytes(len(msg.groupid)))
        bDatArr.extend(str2bytes(msg.groupid))
    else:
        bHeadArr.extend(int2one_bytes(0))
    #sequencenumber
    if msg.sequencenumber is not None:
        bHeadArr.extend(int2one_bytes(4))
        bDatArr.extend(int2four_bytes(msg.sequencenumber))
    else:
        bHeadArr.extend(int2one_bytes(0))
    #sequencetotal
    if msg.sequencetotal is not None:
        bHeadArr.extend(int2one_bytes(4))
        bDatArr.extend(int2four_bytes(msg.sequencetotal))
    else:
        bHeadArr.extend(int2one_bytes(0))
    #priority
    if msg.priority is not None:
        bHeadArr.extend(int2one_bytes(1))
        bDatArr.extend(int2one_bytes(msg.priority))
    else:
        bHeadArr.extend(int2one_bytes(0))
    #timestamp
    if msg.timestamp is not None:
        bHeadArr.extend(int2one_bytes(8))
        bDatArr.extend(long2bytes(msg.timestamp))
    else:
        bHeadArr.extend(int2one_bytes(0))
    #publisher
    if msg.publisher is not None:
        bHeadArr.extend(int2one_bytes(len(msg.publisher)))
        bDatArr.extend(str2bytes(msg.publisher))
    else:
        bHeadArr.extend(int2one_bytes(0))
    #authid
    if msg.authid is not None:
        bHeadArr.extend(int2two_bytes(len(msg.authid)))
        bDatArr.extend(str2bytes(msg.authid))
    else:
        bHeadArr.extend(int2two_bytes(0))
    #authgroup
    if msg.authgroup is not None:
        bHeadArr.extend(int2two_bytes(len(msg.authgroup)))
        bDatArr.extend(str2bytes(msg.authgroup))
    else:
        bHeadArr.extend(int2two_bytes(0))
    #chainposition
    if msg.chainposition is not None:
        bHeadArr.extend(int2one_bytes(8))
        bDatArr.extend(long2bytes(msg.chainposition))
    else:
        bHeadArr.extend(int2one_bytes(0))
    #hash
    if msg.hash is not None:
        bHeadArr.extend(int2two_bytes(len(msg.hash)))
        bDatArr.extend(str2bytes(msg.hash))
    else:
        bHeadArr.extend(int2two_bytes(0))
    #previoushash
    if msg.previoushash is not None:
        bHeadArr.extend(int2two_bytes(len(msg.previoushash)))
        bDatArr.extend(str2bytes(msg.previoushash))
    else:
        bHeadArr.extend(int2two_bytes(0))
    #nonce
    if msg.nonce is not None:
        bHeadArr.extend(int2two_bytes(len(msg.nonce)))
        bDatArr.extend(str2bytes(msg.nonce))
    else:
        bHeadArr.extend(int2two_bytes(0))
    #difficultytarget
    if msg.difficultytarget is not None:
        bHeadArr.extend(int2one_bytes(4))
        bDatArr.extend(int2four_bytes(msg.difficultytarget))
    else:
        bHeadArr.extend(int2one_bytes(0))
    #infotype
    if msg.infotype is not None:
        bHeadArr.extend(int2one_bytes(len(msg.infotype)))
        bDatArr.extend(str2bytes(msg.infotype))
    else:
        bHeadArr.extend(int2one_bytes(0))
    #infoformat
    if msg.infoformat is not None:
        bHeadArr.extend(int2one_bytes(len(msg.infoformat)))
        bDatArr.extend(str2bytes(msg.infoformat))
    else:
        bHeadArr.extend(int2one_bytes(0))
    #contextdata
    if msg.contextdata is not None:
        bHeadArr.extend(int2four_bytes(len(msg.contextdata)))
        bDatArr.extend(msg.contextdata)
    else:
        bHeadArr.extend(int2four_bytes(0))
    #contentdata
    if msg.contentdata is not None:
        bHeadArr.extend(int2four_bytes(len(msg.contentdata)))
        bDatArr.extend(msg.contentdata)
    else:
        bHeadArr.extend(int2four_bytes(0))

    bMsgArrWithLen = bytearray(int2four_bytes(len(bHeadArr) + len(bDatArr) - 1))
    bMsgArr.extend(bHeadArr)
    bMsgArr.extend(bDatArr)
    bMsgArrWithLen.extend(bMsgArr)
    return bMsgArrWithLen

def bytes2message(msgBytes):
    msg = IoMessage()
    data_offset = 33
    head_offset = 0
    #version
    msg.version = two_bytes2int(msgBytes[head_offset:2])
    head_offset = head_offset+2
    #id
    data, data_offset, head_offset = fetch_data(head_offset, 1, data_offset, msgBytes)
    if data is not None:
        msg.id = bytes2str(data)
    #tag
    data, data_offset, head_offset = fetch_data(head_offset, 2, data_offset, msgBytes)#2
    if data is not None:
        msg.tag = bytes2str(data)
    #group id
    data, data_offset, head_offset = fetch_data(head_offset, 1, data_offset, msgBytes)
    if data is not None:
        msg.groupid = bytes2str(data)
    #sequencenumber
    data, data_offset, head_offset = fetch_data(head_offset, 1, data_offset, msgBytes)
    if data is not None:
        msg.sequencenumber = four_bytes2int(data)
    #sequencetotal
    data, data_offset, head_offset = fetch_data(head_offset, 1, data_offset, msgBytes)
    if data is not None:
        msg.sequencetotal = four_bytes2int(data)
    #priority
    data, data_offset, head_offset = fetch_data(head_offset, 1, data_offset, msgBytes)
    if data is not None:
        msg.priority = one_bytes2int(data)
    #timestamp
    data, data_offset, head_offset = fetch_data(head_offset, 1, data_offset, msgBytes)
    if data is not None:
        msg.timestamp = bytes2lonf(data)
    #publisher
    data, data_offset, head_offset = fetch_data(head_offset, 1, data_offset, msgBytes)
    if data is not None:
        msg.publisher = bytes2str(data)
    #authid
    data, data_offset, head_offset = fetch_data(head_offset, 2, data_offset, msgBytes)
    if data is not None:
        msg.authid = bytes2str(data)
    #authgroup
    data, data_offset, head_offset = fetch_data(head_offset, 2, data_offset, msgBytes)
    if data is not None:
        msg.authgroup = bytes2str(data)
    #chainposition
    data, data_offset, head_offset = fetch_data(head_offset, 1, data_offset, msgBytes)#1
    if data is not None:
        msg.chainposition = bytes2lonf(data)
    #hash
    data, data_offset, head_offset = fetch_data(head_offset, 2, data_offset, msgBytes)
    if data is not None:
        msg.hash = bytes2str(data)
    #previoushash
    data, data_offset, head_offset = fetch_data(head_offset, 2, data_offset, msgBytes)
    if data is not None:
        msg.previoushash = bytes2str(data)
    #nonce
    data, data_offset, head_offset = fetch_data(head_offset, 2, data_offset, msgBytes)
    if data is not None:
        msg.nonce = bytes2str(data)
    #difficultytarget
    data, data_offset, head_offset = fetch_data(head_offset, 1, data_offset, msgBytes)
    if data is not None:
        msg.difficultytarget = four_bytes2int(data)
    #infotype
    data, data_offset, head_offset = fetch_data(head_offset, 1, data_offset, msgBytes)
    if data is not None:
        msg.infotype = bytes2str(data)
    #infoformat
    data, data_offset, head_offset = fetch_data(head_offset, 1, data_offset, msgBytes)
    if data is not None:
        msg.infoformat = bytes2str(data)
    #contextdata
    data, data_offset, head_offset = fetch_data(head_offset, 4, data_offset, msgBytes)
    msg.contextdata = data
    #contentdata
    data, data_offset, head_offset = fetch_data(head_offset, 4, data_offset, msgBytes)
    msg.contentdata = data
    return msg

def json2message(jsonStr):
    msg = IoMessage
    jsonMsg = json.loads(jsonStr)
    msg.id = fetch_value(jsonMsg, "id")
    msg.tag = fetch_value(jsonMsg, "tag")
    msg.groupid = fetch_value(jsonMsg, "groupid")
    msg.version = fetch_value(jsonMsg, "version")
    msg.timestamp = fetch_value(jsonMsg, "timestamp")
    msg.sequencenumber = fetch_value(jsonMsg, "sequencenumber")
    msg.sequencetotal = fetch_value(jsonMsg, "sequencetotal")
    msg.priority = fetch_value(jsonMsg, "priority")
    msg.timestamp = fetch_value(jsonMsg, "timestamp")
    msg.publisher = fetch_value(jsonMsg, "publisher")
    msg.authid = fetch_value(jsonMsg, "authid")
    msg.authgroup = fetch_value(jsonMsg, "authgroup")
    msg.chainposition = fetch_value(jsonMsg, "chainposition")
    msg.hash = fetch_value(jsonMsg, "hash")
    msg.previoushash = fetch_value(jsonMsg, "previoushash")
    msg.nonce = fetch_value(jsonMsg, "nonce")
    msg.difficultytarget = fetch_value(jsonMsg, "difficultytarget")
    msg.infotype = fetch_value(jsonMsg, "infotype")
    msg.infoformat = fetch_value(jsonMsg, "infoformat")
    contextdata = fetch_value(jsonMsg, "contextdata")
    if contextdata is not None:
        msg.contextdata = base64.b64decode(contextdata)
    else:
        msg.contextdata = contextdata
    contentdata = fetch_value(jsonMsg, "contentdata")
    if contentdata is not None:
        msg.contentdata = base64.b64decode(fetch_value(jsonMsg, "contentdata"))
    else:
        msg.contentdata = contentdata
    return msg

def message2json(msg):
    msgDict = {}
    msgDict["id"] = msg.id
    msgDict["tag"] = msg.tag
    msgDict["groupid"] = msg.groupid
    msgDict["version"] = msg.version
    msgDict["timestamp"] = msg.timestamp
    msgDict["sequencenumber"] = msg.sequencenumber
    msgDict["sequencetotal"] = msg.sequencetotal
    msgDict["priority"] = msg.priority
    msgDict["timestamp"] = msg.timestamp
    msgDict["publisher"] = msg.publisher
    msgDict["authid"] = msg.authid
    msgDict["authgroup"] = msg.authgroup
    msgDict["chainposition"] = msg.chainposition
    msgDict["hash"] = msg.hash
    msgDict["previoushash"] = msg.previoushash
    msgDict["nonce"] = msg.nonce
    msgDict["difficultytarget"] = msg.difficultytarget
    msgDict["infotype"] = msg.infotype
    msgDict["infoformat"] = msg.infoformat
    if msg.contextdata is not None:
        msgDict["contextdata"] = base64.b64encode(msg.contextdata)
    else:
        msgDict["contextdata"] = msg.contextdata
    if msg.contentdata is not None:
        msgDict["contentdata"] = base64.b64encode(msg.contentdata)
    else:
        msgDict["contentdata"] = msg.contentdata
    return json.dumps(msgDict)

def fetch_value(jsonMsg, fieldName):
    val = None
    if fieldName in jsonMsg:
        val = jsonMsg[fieldName]
    return val
