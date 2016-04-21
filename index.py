import json
from iofabric import *


config=None
msgClient=None
ctlClient=None

CONTAINER_ID="111111111"

class IoFabricListener:

    def onConnected(self):
        return

    def onClosed(self):
        return

    def onMessage(self, msg):
        new_msg=build_message(msg, config)
        if new_msg!=None:
            msgClient.send_message(msg)

    def onUpdateConfig(self, new_config):
        config=new_config

def build_json(origin_json, config):
    new_json={}
    subselection=config["subselection"]
    outputjsonarray=config["outputjsonarray"]
    fieldname=config["fieldname"]
    if subselection in origin_json:
        if "true"==outputjsonarray:
            val_arr=origin_json[subselection]
            if type(val_arr) is list or type(val_arr) is tuple:
                new_json[fieldname]=val_arr
            if val_arr==None:
                new_json[fieldname]=[]
            if val_arr != None:
                new_json[fieldname]=[val_arr]
        else:
            new_json[fieldname]=origin_json[subselection]
    else:
        if "true"==outputjsonarray:
            new_json[fieldname]=[]
        else:
            new_json[fieldname]=None

    return json.dumps(new_json)


def build_message(msg_old, config):
    msg=None
    try:
        for f_conf in config["selections"]:
            if msg_old.infotype==f_conf["inputtype"] and msg_old.infoformat==f_conf["inputformat"]:
                msg=iomessage.IoMessage()
                msg.infotype=f_conf["outputtype"]
                msg.infoformat=f_conf["outputformat"]
                msg.contentdata=build_json(json.loads(msg_old.contentdata), f_conf)
                msg.id=msg_old.id
                msg.tag=msg_old.tag
                msg.groupid=msg_old.groupid
                msg.version=msg_old.version
                msg.timestamp=msg_old.timestamp
                msg.sequencenumber=msg_old.sequencenumber
                msg.sequencetotal=msg_old.sequencetotal
                msg.priority=msg_old.priority
                msg.timestamp=msg_old.timestamp
                msg.publisher=msg_old.publisher
                msg.authid=msg_old.authid
                msg.authgroup=msg_old.authgroup
                msg.chainposition=msg_old.chainposition
                msg.hash=msg_old.hash
                msg.previoushash=msg_old.previoushash
                msg.nonce=msg_old.nonce
                msg.difficultytarget=msg_old.difficultytarget
                msg.contextdata=msg_old.contextdata
                break
    except:
        msg=None
    return msg


listener = IoFabricListener()
msgClient = client.Client("ws://iofabric:54321/v2/control/id/" + CONTAINER_ID, listener)
msgClient.connect()

ctlClient = client.Client("ws://iofabric:54321/v2/message/id/" + CONTAINER_ID, listener)
ctlClient.connect()