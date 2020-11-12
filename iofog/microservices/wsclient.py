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
import threading

import time

import iofog.microservices.util as util
from iofog.microservices.iomessage import IoMessage
from iofog.microservices.definitions import *
from ws4py.client.threadedclient import WebSocketClient
from ws4py.framing import OPCODE_PONG


class IoFogWsClient(WebSocketClient):
    def __init__(self, container_id, ssl, host, port, url, listener):
        protocol_ws = WS
        if ssl:
            protocol_ws = WSS

        self.logger = logging.getLogger(IOFOG_LOGGER)
        self.url_base_ws = '{}://{}:{}'.format(protocol_ws, host, port)
        self.url_ws = self.url_base_ws + url + container_id
        self.wsAttempt = 0
        self.listener = listener
        self.worker = None
        self.is_open = False
        super(IoFogWsClient, self).__init__(self.url_ws)

    def _reconnect(self, code=None, reason=None):
        self.is_open = False
        self.logger.info('WebSocket connection is closed{}{}. Reconnecting...'.format(
            '' if not code else ' with code {}'.format(code),
            '' if not reason else '({})'.format(reason)))
        sleep_time = 1 << self.wsAttempt * WS_CONNECT_TIMEOUT
        if self.wsAttempt < WS_ATTEMPT_LIMIT:
            self.wsAttempt += 1
        try:
            time.sleep(sleep_time)
        except KeyboardInterrupt:
            pass

    def process(self, bytes):
        s = self.stream

        if not bytes and self.reading_buffer_size > 0:
            return False

        from ws4py.websocket import DEFAULT_READING_SIZE
        self.reading_buffer_size = s.parser.send(bytes) or DEFAULT_READING_SIZE

        if s.closing is not None:
            self.logger.debug("Closing message received (%d) '%s'" % (s.closing.code, s.closing.reason))
            if not self.server_terminated:
                self.close(s.closing.code, s.closing.reason)
            else:
                self.client_terminated = True
            return False

        if s.errors:
            for error in s.errors:
                self.logger.debug("Error message received (%d) '%s'" % (error.code, error.reason))
                self.close(error.code, error.reason)
            s.errors = []
            return False

        if s.has_message:
            self.received_message(s.message)
            if s.message is not None:
                s.message.data = None
                s.message = None
            return True

        if s.pings:
            for _ in s.pings:
                self.logger.debug('Got ping from iofog')
                self._write(s.pong(bytearray([OPCODE_PONG])))
            s.pings = []

        if s.pongs:
            for pong in s.pongs:
                self.ponged(pong)
            s.pongs = []

        return True

    def opened(self):
        self.wsAttempt = 0
        self.is_open = True

    def connect(self):
        self.logger.debug('Starting connect')
        self.worker = threading.Thread(target=self._serve, name='WS Server')
        self.worker.start()

    def _serve(self):
        self.logger.debug('Starting serving')
        while True:
            try:
                super(IoFogWsClient, self).connect()
            except Exception as e:
                self._reconnect(reason=e.message)
                continue
            self.run_forever()
            self.logger.debug('Loop exited')
            super(IoFogWsClient, self).__init__(self.url_ws)
            self._reconnect(reason='Connection terminated')


class IoFogControlWsClient(IoFogWsClient):
    def __init__(self, container_id, ssl, host, port, url, listener):
        super(IoFogControlWsClient, self).__init__(container_id, ssl, host, port, url, listener)

    def received_message(self, message):
        opt_code = bytearray(message.data)[0]
        if opt_code == CODE_CONTROL_SIGNAL:
            self.logger.debug('Received control')
            self.listener.on_control_signal()
            self.send(bytearray([CODE_ACK]), binary=True)
        elif opt_code == CODE_EDGE_RESOURCE_SIGNAL:
            self.logger.debug('Received Edge Resource Signal')
            self.listener.on_edge_resources_signal()
            self.send(bytearray([CODE_ACK]), binary=True)


class IoFogMessageWsClient(IoFogWsClient):
    def __init__(self, container_id, ssl, host, port, url, listener):
        super(IoFogMessageWsClient, self).__init__(container_id, ssl, host, port, url, listener)

    def received_message(self, message):
        data = bytearray(message.data)
        opt_code = data[0]
        if opt_code == CODE_MSG:
            self.logger.debug('Received message')
            msg_data = data[5:]
            if len(msg_data) == 0:
                return
            msg = IoMessage.from_bytearray(msg_data)
            self.send(bytearray([CODE_ACK]), binary=True)
            self.listener.on_message(msg)
        elif opt_code == CODE_RECEIPT:
            self.logger.debug('Received receipt')
            receipt_data = data[1:]
            if len(receipt_data) == 0:
                return
            id_len = receipt_data[0]
            ts_len = receipt_data[1]
            pos = 2
            message_id = str(receipt_data[pos: pos + id_len])
            pos += id_len
            timestamp = util.bytearray_to_num(receipt_data[pos: pos + ts_len])
            self.send(bytearray([CODE_ACK]), binary=True)
            self.listener.on_receipt(message_id, timestamp)

    def send_message(self, io_msg):
        self.logger.debug('Sending message')
        self.send(util.prepare_iomessage_for_sending_via_socket(io_msg), binary=True)
        self.logger.debug('Sent message')
