# container-sdk-python

This module lets you easily build an ioElement. It gives you all the functionality to interact with ioFabric via Local API. Additionally some useful methods to work with ioMessage.

 - send new message to ioFabric (sendNewMessage)
 - fetch next unread messages from ioFabric (getNextMessages)
 - fetch messages for time period and list of accessible publishers (getMessagesByQuery)
 - get config options (getConfig)
 - create ioMessage JSON object (ioMessage)
 - connect to ioFabric Control Channel via WebSocket (wsControlConnection)
 - connect to ioFabric Message Channel via WebSocket (wsMessageConnection) and publish new message via this channel (wsSendMessage)

## Code snippets: 
Create ioMessage: 
```python
 msg=IoMessage
 msg.id ="MyId"
 msg.tag="MyTag"
 msg.groupid="MyGroupId"
 ...
```

#### WEBSOCKET
Import iofabric.client:
```python
 import iofabric.client
```
Set up a global variables for config and ws clients:
```python
 config=None
 msgClient=None
 ctlClient=None
```
Implement a WS listener:
```python
class IoFabricListener:
 
    def onConnected(self):
        return
 
    def onClosed(self):
        return
 
    def onMessage(self, msg):
        print(msg)
        #Do some stuff
 
    def onUpdateConfig(self, new_config):
        config=new_config
```
Initialize a WS clients:
```python
 host = iofabric.client.get_host();
 listener = IoFabricListener()
 msgClient = iofabric.client.Client("ws://" + host + ":10500/v2/control/socket/id/" + CONTAINER_ID, listener, CONTAINER_ID)
 msgClient.connect()
```
```python
 ctlClient = iofabric.client.Client("ws://" + host + ":10500/v2/message/socket/id/" + CONTAINER_ID, listener, CONTAINER_ID)
 ctlClient.connect()
```
It will be start a clients in a separate threads in async mode.

#### REST
```python
 req = urllib2.Request("http://" + get_host() + ":54321/<URL>", "{\"id\":\"" + container_id + "\"}", {'Content-Type': 'application/json'})
 response = urllib2.urlopen(req)
 raw_msg=response.read()
```
Message converting
JSON to IoMessage:
```python
 msg=iofabric.iomessage.json2message(json_msg)
```
IoMessage to JSON:
```python
 json_msg=iofabric.iomessage.message2json(msg)
```
Byte Array to IoMessage:
```python
 msg=iofabric.iomessage.bytes2message(byte_array_msg)
```
IoMessage To Byte Array:
```python
 byte_array_msg=iofabric.iomessage.message2bytes(msg)
```
