from iofog_python_sdk.microservices import IoFogClient
from iofog_python_sdk.exception import IoFogException
from iofog_python_sdk.iomessage import IoMessage
from iofog_python_sdk.listener import *

import sys

def build_message():
    msg = IoMessage()
    msg.infotype = "infotype"
    msg.infoformat = "infoformat"
    msg.contextdata = ""
    msg.tag = "tag"
    msg.groupid = "groupid"
    msg.authid = "authid"
    msg.authgroup = "authgroup"
    msg.hash = "hash"
    msg.previoushash = "previoushash"
    msg.nonce = "nonce"

    return msg

def python3():
    try:
        client = IoFogClient()
    except IoFogException as e:
        print("Client Failed on Python3")
        exit(e)

    msg = build_message()
    msg.contentdata = "python3"

    try:
        receipt = client.post_message(msg)
    except IoFogException as e:
        print("Message Failed on Python3")
        exit(e)

    print("Python3 working with SDK")


def python2():
    try:
        client = IoFogClient()
    except IoFogException as e:
        print("Client Failed on Python2")
        exit(e)

    msg = build_message()
    msg.contentdata = "python2"

    try:
        receipt = client.post_message(msg)
    except IoFogException as e:
        print("Message Failed on Python2")
        exit(e)

    print("Python2 working with SDK")

def main():
    if sys.version_info[0] > 3:
        print("test python3")
        while True:
            python3()
    else:
        print("test python2")
        while True:
            python2()