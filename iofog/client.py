from ws4py.client.threadedclient import WebSocketClient
import threading
import iomessage
import byteutils
import urllib2
import json
import subprocess
import time
import exceptions
from ws4py.messaging import Message, PingControlMessage, PongControlMessage


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

    def sendPing(self):
#        print "--- SENDING PING ---"
        data = bytearray([0x9])
        self.send(PingControlMessage(data.decode()))
        threading.Timer(5, self.sendPing).start()

    def ponged(self, pong):
#        print " -- GOT PONG -- "
        return

    def opened(self):
        self.cur_timeout = RECONNECT_TIMEOUT
        self.connected = True
        self.listener.onConnected()
        self.sendPing()

    def closed(self, code, reason=None):
#        print "--SDK-- : closed code = " + str(code) + " ; reason = " + str(reason)
        self.connected = False
        while not self.connected:
            time.sleep(self.cur_timeout)
            try:
                if self.cur_timeout < 10:
                    self.cur_timeout = 2*self.cur_timeout
#                print "--SDK-- : trying to connect again"
                self.connect()
            except exceptions.BaseException as e:
                print 'Reconnect exception: ' + str(e)
        self.listener.onClosed()

    def received_message(self, m):
#        print "--received_message--"
        opt_code = bytearray(m.data)[0]
        if opt_code == NEW_MESSAGE:
#            print "SDK received NEW_MESSAGE signal\n"
            msg_data = bytearray(m.data[5:])
            if len(msg_data) == 0:
                return
            msg = iomessage.bytes2message(msg_data)
            self.send(bytearray([ACK]), binary=True)
            self.listener.onMessage(msg)
        elif opt_code == ACK:
#            print "SDK received ACK signal\n"
            return
        elif opt_code == RECEIPT:
#            print "SDK received RECEIPT signal\n"
            receipt_data = bytearray(m.data)
            if len(receipt_data) == 0:
                return
            size = receipt_data[1]
            pos = 3
            message_id = str(receipt_data[pos: pos + size])
            pos += size
            size = receipt_data[2]
            timestamp = byteutils.bytes2lonf(receipt_data[pos: pos + size])
            self.listener.onMessageReceipt(message_id, timestamp)
            self.send(bytearray([ACK]), binary=True)
        elif opt_code == CONTROL:
#           print "SDK received CONTROL signal\n"
            req = urllib2.Request("http://" + get_host() + ":54321/v2/config/get", "{\"id\":\"" + self.container_id + "\"}", {'Content-Type': 'application/json'})
            response = urllib2.urlopen(req)
            self.send(bytearray([ACK]), binary=True)
            full_config_json = json.loads(response.read())
            if 'config' not in full_config_json:
                self.listener.onUpdateConfig(None)
            else:
                self.listener.onUpdateConfig(json.loads(full_config_json["config"]))

    def send_message(self, msg):
#        print "--SDK-- : sending message"
        msg.publisher = self.container_id
        raw_data = bytearray()
        raw_data += bytearray([NEW_MESSAGE])
        raw_data += iomessage.message2bytes(msg)
        self.send(raw_data, binary=True)

    def connect(self):
        try:
#            print "--SDK-- : CONNECTING"
            super(Client, self).connect()
            self.worker = threading.Thread(target=worker, args=(self,))
            self.worker.start()
        except exceptions.BaseException as e:
#            print "--SDK-- : CONNECTING Exception "
            self.listener.onError(e)

    def unhandled_error(self, error):
#        print "--SDK-- : unhandled_error"
        self.listener.onError(error)


def worker(client):
    client.run_forever()


def get_host():
    try:
        response = subprocess.check_call(
            ["ping", "-c", "3", "iofog"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if response == 0:
            return "iofog"
        else:
            print "Host 'iofog' is unreachable. Changing to default IP '127.0.0.1'"
            return "127.0.0.1"
    except subprocess.CalledProcessError as e:
        print "Error with ping process: " + str(e) + "\nChanging to default IP '127.0.0.1'"
        return "127.0.0.1"
