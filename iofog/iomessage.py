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
        self.sequencenumber = 0
        self.sequencetotal = 0
        self.priority = 0
        self.timestamp = 0
        self.publisher = None
        self.authid = None
        self.authgroup = None
        self.chainposition = 0
        self.hash = None
        self.previoushash = None
        self.nonce = None
        self.difficultytarget = 0
        self.infotype = None
        self.infoformat = None
        self.contextdata = None
        self.contentdata = None

        #1 byte: id, tag, groupId, seqnum, seqtotal, priority, timestamp, publisher, chainpos, diftarget,infoformat, infortype
        #4 byte: context data, content data


def message2bytes(msg):
    b_head_arr = bytearray()
    b_dat_arr = bytearray()
    b_msg_arr = bytearray()
    #version
    b_head_arr.extend(int2two_bytes(msg.version))
    #id
    if msg.id is not None:
        b_head_arr.extend(int2one_bytes(len(msg.id)))
        b_dat_arr.extend(str2bytes(msg.id))
    else:
        b_head_arr.extend(int2one_bytes(0))
    #tag
    if msg.tag is not None:
        b_head_arr.extend(int2two_bytes(len(msg.tag)))
        b_dat_arr.extend(str2bytes(msg.tag))
    else:
        b_head_arr.extend(int2two_bytes(0))
    #group id
    if msg.groupid is not None:
        b_head_arr.extend(int2one_bytes(len(msg.groupid)))
        b_dat_arr.extend(str2bytes(msg.groupid))
    else:
        b_head_arr.extend(int2one_bytes(0))
    #sequencenumber
    if msg.sequencenumber is not None:
        b_head_arr.extend(int2one_bytes(4))
        b_dat_arr.extend(int2four_bytes(msg.sequencenumber))
    else:
        b_head_arr.extend(int2one_bytes(0))
    #sequencetotal
    if msg.sequencetotal is not None:
        b_head_arr.extend(int2one_bytes(4))
        b_dat_arr.extend(int2four_bytes(msg.sequencetotal))
    else:
        b_head_arr.extend(int2one_bytes(0))
    #priority
    if msg.priority is not None:
        b_head_arr.extend(int2one_bytes(1))
        b_dat_arr.extend(int2one_bytes(msg.priority))
    else:
        b_head_arr.extend(int2one_bytes(0))
    #timestamp
    if msg.timestamp is not None:
        b_head_arr.extend(int2one_bytes(8))
        b_dat_arr.extend(long2bytes(msg.timestamp))
    else:
        b_head_arr.extend(int2one_bytes(0))
    #publisher
    if msg.publisher is not None:
        b_head_arr.extend(int2one_bytes(len(msg.publisher)))
        b_dat_arr.extend(str2bytes(msg.publisher))
    else:
        b_head_arr.extend(int2one_bytes(0))
    #authid
    if msg.authid is not None:
        b_head_arr.extend(int2two_bytes(len(msg.authid)))
        b_dat_arr.extend(str2bytes(msg.authid))
    else:
        b_head_arr.extend(int2two_bytes(0))
    #authgroup
    if msg.authgroup is not None:
        b_head_arr.extend(int2two_bytes(len(msg.authgroup)))
        b_dat_arr.extend(str2bytes(msg.authgroup))
    else:
        b_head_arr.extend(int2two_bytes(0))
    #chainposition
    if msg.chainposition is not None:
        b_head_arr.extend(int2one_bytes(8))
        b_dat_arr.extend(long2bytes(msg.chainposition))
    else:
        b_head_arr.extend(int2one_bytes(0))
    #hash
    if msg.hash is not None:
        b_head_arr.extend(int2two_bytes(len(msg.hash)))
        b_dat_arr.extend(str2bytes(msg.hash))
    else:
        b_head_arr.extend(int2two_bytes(0))
    #previoushash
    if msg.previoushash is not None:
        b_head_arr.extend(int2two_bytes(len(msg.previoushash)))
        b_dat_arr.extend(str2bytes(msg.previoushash))
    else:
        b_head_arr.extend(int2two_bytes(0))
    #nonce
    if msg.nonce is not None:
        b_head_arr.extend(int2two_bytes(len(msg.nonce)))
        b_dat_arr.extend(str2bytes(msg.nonce))
    else:
        b_head_arr.extend(int2two_bytes(0))
    #difficultytarget
    if msg.difficultytarget is not None:
        b_head_arr.extend(int2one_bytes(4))
        b_dat_arr.extend(int2four_bytes(msg.difficultytarget))
    else:
        b_head_arr.extend(int2one_bytes(0))
    #infotype
    if msg.infotype is not None:
        b_head_arr.extend(int2one_bytes(len(msg.infotype)))
        b_dat_arr.extend(str2bytes(msg.infotype))
    else:
        b_head_arr.extend(int2one_bytes(0))
    #infoformat
    if msg.infoformat is not None:
        b_head_arr.extend(int2one_bytes(len(msg.infoformat)))
        b_dat_arr.extend(str2bytes(msg.infoformat))
    else:
        b_head_arr.extend(int2one_bytes(0))
    #contextdata
    if msg.contextdata is not None:
        b_head_arr.extend(int2four_bytes(len(msg.contextdata)))
        b_dat_arr.extend(msg.contextdata)
    else:
        b_head_arr.extend(int2four_bytes(0))
    #contentdata
    if msg.contentdata is not None:
        b_head_arr.extend(int2four_bytes(len(msg.contentdata)))
        b_dat_arr.extend(msg.contentdata)
    else:
        b_head_arr.extend(int2four_bytes(0))

    b_msg_arr_with_len = bytearray(int2four_bytes(len(b_head_arr) + len(b_dat_arr)))
    b_msg_arr.extend(b_head_arr)
    b_msg_arr.extend(b_dat_arr)
    b_msg_arr_with_len.extend(b_msg_arr)
    return b_msg_arr_with_len


def bytes2message(msg_bytes):
    msg = IoMessage()
    data_offset = 33
    head_offset = 0
    #version
    msg.version = two_bytes2int(msg_bytes[head_offset:2])
    head_offset = head_offset+2
    #id
    data, data_offset, head_offset = fetch_data(head_offset, 1, data_offset, msg_bytes)
    if data is not None:
        msg.id = bytes2str(data)
    #tag
    data, data_offset, head_offset = fetch_data(head_offset, 2, data_offset, msg_bytes)#2
    if data is not None:
        msg.tag = bytes2str(data)
    #group id
    data, data_offset, head_offset = fetch_data(head_offset, 1, data_offset, msg_bytes)
    if data is not None:
        msg.groupid = bytes2str(data)
    #sequencenumber
    data, data_offset, head_offset = fetch_data(head_offset, 1, data_offset, msg_bytes)
    if data is not None:
        msg.sequencenumber = four_bytes2int(data)
    #sequencetotal
    data, data_offset, head_offset = fetch_data(head_offset, 1, data_offset, msg_bytes)
    if data is not None:
        msg.sequencetotal = four_bytes2int(data)
    #priority
    data, data_offset, head_offset = fetch_data(head_offset, 1, data_offset, msg_bytes)
    if data is not None:
        msg.priority = one_bytes2int(data)
    #timestamp
    data, data_offset, head_offset = fetch_data(head_offset, 1, data_offset, msg_bytes)
    if data is not None:
        msg.timestamp = bytes2lonf(data)
    #publisher
    data, data_offset, head_offset = fetch_data(head_offset, 1, data_offset, msg_bytes)
    if data is not None:
        msg.publisher = bytes2str(data)
    #authid
    data, data_offset, head_offset = fetch_data(head_offset, 2, data_offset, msg_bytes)
    if data is not None:
        msg.authid = bytes2str(data)
    #authgroup
    data, data_offset, head_offset = fetch_data(head_offset, 2, data_offset, msg_bytes)
    if data is not None:
        msg.authgroup = bytes2str(data)
    #chainposition
    data, data_offset, head_offset = fetch_data(head_offset, 1, data_offset, msg_bytes)#1
    if data is not None:
        msg.chainposition = bytes2lonf(data)
    #hash
    data, data_offset, head_offset = fetch_data(head_offset, 2, data_offset, msg_bytes)
    if data is not None:
        msg.hash = bytes2str(data)
    #previoushash
    data, data_offset, head_offset = fetch_data(head_offset, 2, data_offset, msg_bytes)
    if data is not None:
        msg.previoushash = bytes2str(data)
    #nonce
    data, data_offset, head_offset = fetch_data(head_offset, 2, data_offset, msg_bytes)
    if data is not None:
        msg.nonce = bytes2str(data)
    #difficultytarget
    data, data_offset, head_offset = fetch_data(head_offset, 1, data_offset, msg_bytes)
    if data is not None:
        msg.difficultytarget = four_bytes2int(data)
    #infotype
    data, data_offset, head_offset = fetch_data(head_offset, 1, data_offset, msg_bytes)
    if data is not None:
        msg.infotype = bytes2str(data)
    #infoformat
    data, data_offset, head_offset = fetch_data(head_offset, 1, data_offset, msg_bytes)
    if data is not None:
        msg.infoformat = bytes2str(data)
    #contextdata
    data, data_offset, head_offset = fetch_data(head_offset, 4, data_offset, msg_bytes)
    msg.contextdata = data
    #contentdata
    data, data_offset, head_offset = fetch_data(head_offset, 4, data_offset, msg_bytes)
    msg.contentdata = data
    return msg


def json2message(json_str):
    msg = IoMessage
    json_msg = json.loads(json_str)
    msg.id = fetch_value(json_msg, "id")
    msg.tag = fetch_value(json_msg, "tag")
    msg.groupid = fetch_value(json_msg, "groupid")
    fetched_value = fetch_value(json_msg, "version")
    if fetched_value is not None:
        msg.version = fetched_value
    fetched_value = fetch_value(json_msg, "timestamp")
    if fetched_value is not None:
        msg.timestamp = fetched_value
    fetched_value = fetch_value(json_msg, "sequencenumber")
    if fetched_value is not None:
        msg.sequencenumber = fetched_value
    fetched_value = fetch_value(json_msg, "sequencetotal")
    if fetched_value is not None:
        msg.sequencetotal = fetched_value
    fetched_value = fetch_value(json_msg, "priority")
    if fetched_value is not None:
        msg.priority = fetched_value
    msg.publisher = fetch_value(json_msg, "publisher")
    msg.authid = fetch_value(json_msg, "authid")
    msg.authgroup = fetch_value(json_msg, "authgroup")
    fetched_value = fetch_value(json_msg, "chainposition")
    if fetched_value is not None:
        msg.chainposition = fetched_value
    msg.hash = fetch_value(json_msg, "hash")
    msg.previoushash = fetch_value(json_msg, "previoushash")
    msg.nonce = fetch_value(json_msg, "nonce")
    fetched_value = fetch_value(json_msg, "difficultytarget")
    if fetched_value is not None:
        msg.difficultytarget = fetched_value
    msg.infotype = fetch_value(json_msg, "infotype")
    msg.infoformat = fetch_value(json_msg, "infoformat")
    contextdata = fetch_value(json_msg, "contextdata")
    if contextdata is not None:
        msg.contextdata = base64.b64decode(contextdata)
    contentdata = fetch_value(json_msg, "contentdata")
    if contentdata is not None:
        msg.contentdata = base64.b64decode(contentdata)
    return msg


def message2json(msg):
    if msg.version is None:
        msg.version = IO_MESSAGE_VERSION
    if msg.sequencenumber is None:
        msg.sequencenumber = 0
    if msg.sequencetotal is None:
        msg.sequencetotal = 0
    if msg.priority is None:
        msg.priority = 0
    if msg.timestamp is None:
        msg.timestamp = 0
    if msg.chainposition is None:
        msg.chainposition = 0
    if msg.difficultytarget is None:
        msg.difficultytarget = 0
    msg_dict = {}
    msg_dict["id"] = msg.id
    msg_dict["tag"] = msg.tag
    msg_dict["groupid"] = msg.groupid
    msg_dict["version"] = msg.version
    msg_dict["timestamp"] = msg.timestamp
    msg_dict["sequencenumber"] = msg.sequencenumber
    msg_dict["sequencetotal"] = msg.sequencetotal
    msg_dict["priority"] = msg.priority
    msg_dict["timestamp"] = msg.timestamp
    msg_dict["publisher"] = msg.publisher
    msg_dict["authid"] = msg.authid
    msg_dict["authgroup"] = msg.authgroup
    msg_dict["chainposition"] = msg.chainposition
    msg_dict["hash"] = msg.hash
    msg_dict["previoushash"] = msg.previoushash
    msg_dict["nonce"] = msg.nonce
    msg_dict["difficultytarget"] = msg.difficultytarget
    msg_dict["infotype"] = msg.infotype
    msg_dict["infoformat"] = msg.infoformat
    if msg.contextdata is not None:
        msg_dict["contextdata"] = base64.b64encode(msg.contextdata)
    else:
        msg_dict["contextdata"] = msg.contextdata
    if msg.contentdata is not None:
        msg_dict["contentdata"] = base64.b64encode(msg.contentdata)
    else:
        msg_dict["contentdata"] = msg.contentdata
    return json.dumps(msg_dict)


def fetch_value(json_msg, field_name):
    val = None
    if field_name in json_msg:
        val = json_msg[field_name]
    return val
