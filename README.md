# ioFog Python SDK

This SDK provides the following modules:
* microservices: Clients for Microservices to talk to ioFog (e.g. ioMessage and Web Socket clients)
* rest.controller: Client for Controller REST API

## Installation

Install python package:
```bash
sudo python3 -m pip install iofog
```

## Microservices

This module lets you easily build an ioElement. It gives you all the functionality to interact with ioFog via Local API. It contains all necessary methods for IoMessage transformation as well.

 - send new message to ioFog (post_message)
 - fetch next unread messages from ioFog (get_next_messages)
 - fetch messages for time period and list of accessible publishers (get_next_messages_from_publishers_within_timeframe)
 - get config options (get_config)
 - get Agent's Edge Resources (get_edge_resources)
 - create IoMessage, encode(decode) to(from) raw bytes, marshall(unmarshall) into(from) JSON object (IoMessage class methods)
 - connect to ioFog Control Channel via WebSocket (establish_control_ws_connection)
 - connect to ioFog Message Channel via WebSocket (establish_message_ws_connection) and publish new message via this channel (post_message_via_socket)

### Usage

Import iofog client and additional classes to your project:
```python
from iofog.microservices.client import Client
from iofog.microservices.exception import IoFogException
from iofog.microservices.iomessage import IoMessage
from iofog.microservices.listener import *
```

Create IoFog client with default settings:
```python
try:
    client = Client()
except IoFogException as e:
 # client creation failed, e contains description
```

Or specify host, port, and container id explicitly:
```python
try:
    client = Client(id='container_id', host='iofog_host', port=6666)
except IoFogException as e:
 # client creation failed, e contains description
```

##### REST calls

Get list of next unread IoMessages:
```python
try:
    messages = client.get_next_messages()
except IoFogException as e:
 # some error occurred, e contains description
```

Post new IoMessage to ioFog via REST call:
```python
msg=IoMessage()
msg.infotype="infotype"
msg.infoformat="infoformat"
msg.contentdata="sdkjhwrtiy8wrtgSDFOiuhsrgowh4touwsdhsDFDSKJhsdkljasjklweklfjwhefiauhw98p328946982weiusfhsdkufhaskldjfslkjdhfalsjdf=serg4towhr"
msg.contextdata=""
msg.tag="tag"
msg.groupid="groupid"
msg.authid="authid"
msg.authgroup="authgroup"
msg.hash="hash"
msg.previoushash="previoushash"
msg.nonce="nonce"

try:
    receipt = client.post_message(msg)
except IoFogException, e:
 # some error occurred, e contains description
```

Get an array of IoMessages from specified publishers within given timeframe:
```python
query = {
    	'timeframestart': 1234567890123,
    	'timeframeend': 1234567890123,
    	'publishers': ['sefhuiw4984twefsdoiuhsdf', 'd895y459rwdsifuhSDFKukuewf', 'SESD984wtsdidsiusidsufgsdfkh']
}
try:
    query_response = client.get_next_messages_from_publishers_within_timeframe(query)
except IoFogException, e:
 # some error occurred, e contains description
```

Get container's config:
```python
try:
    config = client.get_config()
except IoFogException, ex:
 # some error occurred, ex contains description
```

Get Agent's Edge Resources:
```python
try:
    edge_resources = client.get_edge_resources()
except IoFogException, ex:
 # some error occurred, ex contains description
```

##### WebSocket calls

To use websocket connections you should implement listeners as follows:
```python
class MyControlListener(IoFogControlWsListener):
    def on_control_signal(self):
        # do smth on control signal
    def on_edge_resources_signal(self):
        # Agent's Edge Resource list has been updated


class MyMessageListener(IoFogMessageWsListener):
    def on_receipt(self, message_id, timestamp):
        # do smth with message receipt

    def on_message(self, io_msg):
        # do smth with new message

```

After that you can establish websocket connections:
```python
client.establish_message_ws_connection(MyMessageListener())
client.establish_control_ws_connection(MyControlListener())
```
Each of those connections will be managed in a separate thread.
 
 
After successful connection to message websocket you can send to it:
```python
client.post_message_via_socket(io_msg_instance)
```


##### Message utils

Construct IoMessage from JSON(both json string and python dictionary are acceptable):
```python
msg = IoMessage.from_json(json_msg)
 ```

IoMessage to JSON:
```python
json_str = io_msg_instance.to_json()
```

Construct IoMessage from raw bytes:
```python
msg = IoMessage.from_bytearray([0, 4, ...])
```

Pack IoMessage into bytearray:
```python
msg_bytes = io_msg_instance.to_bytearray()
```

#### Logging

```python
from iofog.microservices.log import Logger

log = Logger("first")
log.debug("hello")
log.info("world")
log.warn("good")
log.error("bye")
```

## Controller REST API Client

This module provides a client for talking to [ioFog Controller's REST API](https://iofog.org/docs/2/reference-controller/rest-api.html).

### Usage

```python
# Import Client class
from iofog.rest.controller.client import Client

# Instantiate Client
client = Client(
    host="123.123.123.123",
    port=51121,
    email="hello@world.io"
    password="2uhi40ghas9"

# Get Controller status and API version
status = client.get_status()
print(status['versions']['controller'])

# Create an Agent
name = "agent1"
host = "123.123.123.124"
resp = client.create_agent(name, host)

# Upgrade an Agent
resp = client.upgrade_agent(name)

# Create an Application
yaml_file = "/tmp/app.yaml"
resp = client.create_app_from_yaml(yaml_file)

# Get an Application
app_name = "app1"
resp = client.get_app(app_name)

# Delete an Application
resp = client.delete_app(app_name)
```
 