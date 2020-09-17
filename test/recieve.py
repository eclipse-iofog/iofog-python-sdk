from iofog.microservices import IoFogClient
from iofog.exception import IoFogException
from iofog.iomessage import IoMessage
from iofog.listener import *


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
