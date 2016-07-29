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
msg=iofabric.iomessage.IoMessage()
msg.infotype="infotype"
msg.infoformat="infoformat"
msg.contentdata="sdkjhwrtiy8wrtgSDFOiuhsrgowh4touwsdhsDFDSKJhsdkljasjklweklfjwhefiauhw98p328946982weiusfhsdkufhaskldjfslkjdhfalsjdf=serg4towhr"
msg.contextdata=""
msg.tag="tag"
msg.groupid="groupid"
msg.sequencenumber=0
msg.sequencetotal=0
msg.priority=0
msg.publisher="CONTAINER'S_ID"
msg.authid="authid"
msg.authgroup="authgroup"
msg.chainposition=0
msg.hash="hash"
msg.previoushash="previoushash"
msg.nonce="nonce"
msg.difficultytarget=0
 ...
```

#### WEBSOCKET
Import ioFabric client and message util :
```python
 import iofabric.client
 import iofabric.iomessage
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
 
 ctlClient = iofabric.client.Client("ws://" + host + ":10500/v2/message/socket/id/" + CONTAINER_ID, listener, CONTAINER_ID)
 ctlClient.connect()
```
It will start clients in a separate threads in async mode.

#### REST
```python
 req = urllib2.Request("http://" + get_host() + ":54321/<URL>", "{\"id\":\"" + container_id + "\"}", {'Content-Type': 'application/json'})
 response = urllib2.urlopen(req)
 raw_msg=response.read()
```
#### Message utils
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
#### Examples
Send message via REST:
```python
new_msg=iofabric.iomessage.IoMessage()
#set any fields you need to
req = urllib2.Request("http://" + iofabric.client.get_host() + ":54321/v2/messages/new", iofabric.iomessage.message2json(new_msg), {'Content-Type': 'application/json'})
```
Send message via Socket:
```python
#initialize msgClient
new_msg=iofabric.iomessage.IoMessage()
#set any fields you need to
msgClient.send_message(new_msg)
```
