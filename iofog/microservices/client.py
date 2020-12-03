#********************************************************************************
#  Copyright (c) 2018 Edgeworx, Inc.
#
#  This program and the accompanying materials are made available under the
#  terms of the Eclipse Public License v. 2.0 which is available at
#  http://www.eclipse.org/legal/epl-2.0
#
#  SPDX-License-Identifier: EPL-2.0
#********************************************************************************

import logging
import os

import subprocess

from iofog.microservices.httpclient import IoFogHttpClient
from iofog.microservices.definitions import *
from iofog.microservices.wsclient import IoFogControlWsClient, IoFogMessageWsClient
from iofog.microservices.listener import *
from iofog.microservices.exception import *

class Client:
    def __init__(self, id=None, ssl=None, host=None, port=None):
        self.logger = logging.getLogger(IOFOG_LOGGER)
        ch = logging.StreamHandler()
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
        except Exception as e:
            raise IoFogException(e)

    def get_edge_resources(self):
        try:
            return self.http_client.get_edge_resources()
        except Exception as e:
            raise IoFogException(e)

    def get_next_messages(self):
        try:
            return self.http_client.get_next_messages()
        except Exception as e:
            raise IoFogException(e)

    def get_next_messages_from_publishers_within_timeframe(self, query):
        assert TIME_FRAME_START in query and TIME_FRAME_END in query and PUBLISHERS in query, 'Wrong query parameters'
        query[ID] = self.id
        try:
            return self.http_client.get_next_messages_from_publishers_within_timeframe(query)
        except Exception as e:
            raise IoFogException(e)

    def post_message(self, io_msg):
        if not io_msg.version:
            io_msg.version = IO_MESSAGE_VERSION
        io_msg.publisher = self.id
        try:
            return self.http_client.post_message(io_msg)
        except Exception as e:
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
        except Exception as e:
            raise IoFogException(e)
