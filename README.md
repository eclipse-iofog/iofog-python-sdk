# container-sdk-python

This module lets you easily build an ioElement. It gives you all the functionality to interact with ioFog via Local API. Additionally some useful methods to work with ioMessage.

 - send new message to ioFog (sendNewMessage)
 - fetch next unread messages from ioFog (getNextMessages)
 - fetch messages for time period and list of accessible publishers (getMessagesByQuery)
 - get config options (getConfig)
 - create ioMessage JSON object (ioMessage)
 - connect to ioFog Control Channel via WebSocket (wsControlConnection)
 - connect to ioFog Message Channel via WebSocket (wsMessageConnection) and publish new message via this channel (wsSendMessage)

## Code snippets: 
Create ioMessage: 
```python
msg=iofog.iomessage.IoMessage()
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
Import ioFog client and message util :
```python
 import iofog.client
 import iofog.iomessage
 import iofog.byteutils
```
Set up a global variables for config and ws clients:
```python
 config=None
 msgClient=None
 ctlClient=None
```
Implement a WS listener:
```python
class ioFogListener:
 
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
 host = iofog.client.get_host();
 listener = ioFogListener()
 
 msgClient = iofog.client.Client("ws://" + host + ":54321/v2/control/socket/id/" + CONTAINER_ID, listener, CONTAINER_ID)
 msgClient.connect()
 
 ctlClient = iofog.client.Client("ws://" + host + ":54321/v2/message/socket/id/" + CONTAINER_ID, listener, CONTAINER_ID)
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
 msg=iofog.iomessage.json2message(json_msg, decode) // decode - flag which indicates if context and content data need to be decoded from base64 format
```
IoMessage to JSON:
```python
 json_msg=iofog.iomessage.message2json(msg, encode) // decode - flag which indicates if context and content data need to be encoded to base64 format
```
Byte Array to IoMessage:
```python
 msg=iofog.iomessage.bytes2message(byte_array_msg)
```
IoMessage To Byte Array:
```python
 byte_array_msg=iofog.iomessage.message2bytes(msg)
```
#### Examples
Send message via REST:
```python
new_msg=iofog.iomessage.IoMessage()
#set any fields you need to
req = urllib2.Request("http://" + iofog.client.get_host() + ":54321/v2/messages/new", data=iofog.iomessage.message2json(new_msg, True), headers={"content-Type": "application/json"})
response = urllib2.urlopen(req)
responseJson = json.loads(response.read())
```
Send message via Socket:
```python
#initialize msgClient
new_msg=iofog.iomessage.IoMessage()
#set any fields you need to
msgClient.send_message(new_msg)
```
