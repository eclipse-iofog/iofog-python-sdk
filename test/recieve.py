from iofog_python_sdk.microservices.client import IoFogClient
from iofog_python_sdk.microservices.exception import IoFogException
from iofog_python_sdk.microservices.iomessage import IoMessage
from iofog_python_sdk.microservices.listener import *
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


def main():
    init_logger()
    logger = logging.getLogger(__name__)
    try:
        client = IoFogClient()
    except IoFogException as e:
        logger.error("Failed to start client")
        exit(e)

    while True:
        try:
            messages = client.get_next_messages()
            for message in messages:
                if message.contentdata == "python2" or message.contentdata == "python3":
                    logger.info("It worked")
                else:
                    exit(1)
        except IoFogException as e:
            logger.error("Could not get next message")
            exit(e)



if __name__ == "__main__":
    main()