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

import module:
```
  from iofabric import *
```

set up custom host, port and container's ID (in case of no params default values for host and port will be used: 'iofabric', 54321)
and pass main callback to trigger when ioFabricClient initialization is done:
```

class IoFabricListener:

    def onConnected(self):
        ```

    def onClosed(self):
        ```

    def onMessage(self, msg):
        ```

    def onUpdateConfig(self, new_config):
        ```
host = client.get_host();
listener = IoFabricListener()
msgClient = client.Client("ws://" + host + ":54321/v2/control/id/" + CONTAINER_ID, listener)
msgClient.connect()
ctlClient = client.Client("ws://" + host + ":54321/v2/message/id/" + CONTAINER_ID, listener)
ctlClient.connect()
```

#### WebSocket(WS) calls
open WS Message Channel to ioFabric with callback to send new message via this channel
```
msg=msg=iomessage.IoMessage()
```
msgClient.send_message(msg)
```

Open WS Control Channel to ioFabric
```
config=None
class IoFabricListener:
```

    def onUpdateConfig(self, new_config):
        config=new_config

ctlClient = client.Client("ws://" + host + ":54321/v2/message/id/" + CONTAINER_ID, listener)
ctlClient.connect()
