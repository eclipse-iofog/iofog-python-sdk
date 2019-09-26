from iofog_python_sdk.client import IoFogClient
from iofog_python_sdk.exception import IoFogException
from iofog_python_sdk.iomessage import IoMessage
from iofog_python_sdk.listener import *


def main():
    try:
        client = IoFogClient()
    except IoFogException as e:
        print("Failed to start client")

    while True:
        try:
            messages = client.get_next_messages()
            for message in messages:
                if message.contentdata == "python2" or message.contentdata == "python3":
                    print("It worked")
                else:
                    exit(1)
        except IoFogException as e:
            print("Could not get next message")
            exit(e)
