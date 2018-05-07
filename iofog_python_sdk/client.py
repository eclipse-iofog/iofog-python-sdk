import argparse
import logging
import os

import subprocess

from httpclient import IoFogHttpClient
from definitions import *
from wsclient import IoFogControlWsClient, IoFogMessageWsClient
from listener import *
from exception import *

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--log", dest="logLevel", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                    help="Set the logging level", default='INFO')
args = parser.parse_args()


class IoFogClient:
    def __init__(self, id=None, ssl=None, host=None, port=None):
        self.logger = logging.getLogger(IOFOG_LOGGER)
        self.logger.setLevel(args.logLevel)
        ch = logging.StreamHandler()
        ch.setLevel(args.logLevel)
        formatter = logging.Formatter(
            '%(levelname)5s [%(asctime)-15s] %(module)10s - <Thread: %(threadName)15s> - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        if id:
            self.id = id
        else:
            self.id = os.getenv(SELFNAME)
            if not self.id:
                raise IoFogException('Cannot create client with empty id: ' +
                                     SELFNAME + ' environment variable is not set')

        if ssl:
            self.ssl = ssl
        else:
            self.ssl = os.getenv(SSL)
            if not self.ssl:
                self.logger.info('Empty or malformed ' + SSL
                                 + ' environment variable. Using default value of ' + str(SSL_DEFAULT))
                self.ssl = SSL_DEFAULT

        if host:
            self.host = host
        else:
            self.host = IOFOG
            with open(os.devnull, 'w') as FNULL:
                resp = subprocess.call(['ping', '-c', '3', self.host], stdout=FNULL, stderr=FNULL)
            if resp:
                self.logger.info('Host ' + IOFOG + ' is unreachable. Switching to ' + HOST_DEFAULT)
                self.host = HOST_DEFAULT

        self.port = port if port else PORT_IOFOG

        self.message_ws_client = None
        self.control_ws_client = None
        self.http_client = IoFogHttpClient(self.id, self.ssl, self.host, self.port)

    def establish_message_ws_connection(self, listener):
        if listener is not None and not isinstance(listener, IoFogMessageWsListener):
            raise IoFogException('Invalid listener instance')
        if self.message_ws_client:
            raise IoFogException('Connection has been already established')
        self.message_ws_client = IoFogMessageWsClient(self.id, self.ssl, self.host,
                                                      self.port, URL_GET_MESSAGE_WS, listener)
        self.message_ws_client.connect()

    def establish_control_ws_connection(self, listener):
        if listener is not None and not isinstance(listener, IoFogControlWsListener):
            raise IoFogException('Invalid listener instance')
        if self.control_ws_client:
            raise IoFogException('Connection has been already established')
        self.control_ws_client = IoFogControlWsClient(self.id, self.ssl, self.host,
                                                      self.port, URL_GET_CONTROL_WS, listener)
        self.control_ws_client.connect()

    def get_config(self):
        try:
            return self.http_client.get_config()
        except Exception, e:
            raise IoFogException(e)

    def get_next_messages(self):
        try:
            return self.http_client.get_next_messages()
        except Exception, e:
            raise IoFogException(e)

    def get_next_messages_from_publishers_within_timeframe(self, query):
        assert TIME_FRAME_START in query and TIME_FRAME_END in query and PUBLISHERS in query, 'Wrong query parameters'
        query[ID] = self.id
        try:
            return self.http_client.get_next_messages_from_publishers_within_timeframe(query)
        except Exception, e:
            raise IoFogException(e)

    def post_message(self, io_msg):
        if not io_msg.version:
            io_msg.version = IO_MESSAGE_VERSION
        io_msg.publisher = self.id
        try:
            return self.http_client.post_message(io_msg)
        except Exception, e:
            raise IoFogException(e)

    def post_message_via_socket(self, io_msg):
        if not self.message_ws_client:
            raise IoFogException('Establish message websocket connection first!')
        while not self.message_ws_client.is_open:
            pass
        io_msg.id = ''
        io_msg.timestamp = 0
        io_msg.publisher = self.id
        if io_msg.version == 0:
            io_msg.version = IO_MESSAGE_VERSION
        try:
            self.message_ws_client.send_message(io_msg)
        except Exception, e:
            raise IoFogException(e)
