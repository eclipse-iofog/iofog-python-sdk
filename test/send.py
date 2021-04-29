from iofog_python_sdk.microservices.client import IoFogClient
from iofog_python_sdk.microservices.exception import IoFogException
from iofog_python_sdk.microservices.iomessage import IoMessage
from iofog_python_sdk.microservices.listener import *
from iofog_python_sdk.microservices.definitions import *

import sys
import time
import logging

def init_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel('DEBUG')
    ch = logging.StreamHandler()
    ch.setLevel('DEBUG')
    formatter = logging.Formatter(
        '%(levelname)5s [%(asctime)-15s] %(module)10s - <Thread: %(threadName)15s> - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)


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
    logger = logging.getLogger(__name__)
    try:
        client = IoFogClient()
    except IoFogException as e:
        logger.error("Client Failed on Python3")
        exit(e)

    msg = build_message()
    msg.contentdata = "python3"

    try:
        receipt = client.post_message(msg)
    except IoFogException as e:
        logger.error("Message Failed on Python3")
        exit(e)

    logger.info("Python3 working with SDK")


def python2():
    logger = logging.getLogger(__name__)
    try:
        client = IoFogClient()
    except IoFogException as e:
        logger.error("Client Failed on Python2")
        exit(e)

    msg = build_message()
    msg.contentdata = "python2"

    try:
        receipt = client.post_message(msg)
    except IoFogException as e:
        logger.error("Message Failed on Python2")
        exit(e)

    logger.info("Python2 working with SDK")



def main():
    init_logger()
    if sys.version_info[0] >= 3:
        print("test python3")
        while True:
            time.sleep(2)
            python3()
    else:
        print("test python2")
        while True:
            time.sleep(2)
            python2()



if __name__ == "__main__":
    main()