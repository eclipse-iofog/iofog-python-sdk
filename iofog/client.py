from ws4py.client.threadedclient import WebSocketClient
import threading
import iomessage
import urllib2
import json
import os
import time


NEW_MESSAGE = 13
RECEIPT = 14
ACK = 11
CONTROL = 12
RECONNECT_TIMEOUT = 1


class Client(WebSocketClient):
    def __init__(self, url, listener, container_id):
        super(Client, self).__init__(url)
        self.listener = listener
        self.url = url
        self.container_id = container_id
        self.cur_timeout = RECONNECT_TIMEOUT
        self.connected = None

    def opened(self):
        self.cur_timeout = RECONNECT_TIMEOUT
        self.connected = True
        self.listener.onConnected()

    def closed(self, code, reason=None):
        self.connected = False
        while not self.connected:
            time.sleep(self.cur_timeout)
            try:
                if self.cur_timeout < 10:
                    self.cur_timeout = 2*self.cur_timeout
                self.connect()
            except Exception as e:
                print 'Reconnect exception: ' + str(e)
        self.listener.onClosed()

    def received_message(self, m):
        opt_code = bytearray(m.data)[0]
        if opt_code == NEW_MESSAGE:
            #print "SDK received NEW_MESSAGE signal\n"
            msg_data = bytearray(m.data[5:])
            if len(msg_data) == 0:
                return
            msg = iomessage.bytes2message(msg_data)
            self.send(bytearray([ACK]), binary=True)
            self.listener.onMessage(msg)
        if opt_code == ACK:
            print "SDK received ACK signal\n"
        if opt_code == RECEIPT:
            print "SDK received RECEIPT signal\n"
            self.send(bytearray([ACK]), binary=True)
        if opt_code == CONTROL:
            #print "SDK received CONTROL signal\n"
            req = urllib2.Request("http://" + get_host() + ":54321/v2/config/get", "{\"id\":\"" + self.container_id + "\"}", {'Content-Type': 'application/json'})
            response = urllib2.urlopen(req)
            self.send(bytearray([ACK]), binary=True)
            full_config_json = json.loads(response.read())
            if 'config' not in full_config_json:
                self.listener.onUpdateConfig(None)
            else:
                self.listener.onUpdateConfig(json.loads(full_config_json["config"]))

    def send_message(self, msg):
        raw_data = bytearray()
        raw_data += bytearray([NEW_MESSAGE])
        raw_data += iomessage.message2bytes(msg)
        self.send(raw_data, binary=True)

    def connect(self):
        try:
            super(Client, self).connect()
            self.worker = threading.Thread(target=worker, args=(self,))
            self.worker.start()
        except Exception as e:
            self.listener.onError(e)

    def unhandled_error(self, error):
        self.listener.onError(error)


def worker(client):
    client.run_forever()


def get_host():
    response = os.system("ping -c 1 " + "iofog")
    if response == 0:
        return "iofog"
    else:
        return "127.0.0.1"
