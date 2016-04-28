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

def convert(cur_format, new_format, value):
    new_value=value
    if cur_format == 'decimal/kelvin' and new_format == 'fahrenheit':
        new_value = (value * (9 / 5)) - 459.67

    if cur_format == 'decimal/kelvin' and new_format == 'celcius':
        new_value = value - 273.15

    if cur_format == 'decimal/fahrenheit' and new_format == 'kelvin':
        new_value = (value + 459.67) * (5 / 9)

    if cur_format == 'decimal/fahrenheit' and new_format == 'celcius':
        new_value = (value - 32) * (5 / 9)

    if cur_format == 'decimal/celcius' and new_format == 'kelvin':
        new_value = value + 273.15

    if cur_format == 'decimal/celcius' and new_format == 'fahrenheit':
        new_value = (value * (9 / 5)) + 32

    return new_value


def build_message(msg_old, config):
    msg=None
    try:
        if msg_old.infoformat == "decimal/kelvin" or msg_old.infoformat == "decimal/celcius" or msg_old.infoformat == "decimal/fahrenheit":
            format=msg_old.infoformat.split("/")[1]
            if format != config.outputformat:
                new_val=convert(msg_old.infoformat, config.outputformat, msg_old.contentdata)
                msg=iomessage.IoMessage()
                msg.infotype=msg_old.infotype
                msg.infoformat="decimal/" + config.outputformat
                msg.contentdata=new_val
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

    except:
        msg=None
    return msg


listener = IoFabricListener()
msgClient = client.Client("ws://iofabric:54321/v2/control/id/" + CONTAINER_ID, listener)
msgClient.connect()

ctlClient = client.Client("ws://iofabric:54321/v2/message/id/" + CONTAINER_ID, listener)
ctlClient.connect()