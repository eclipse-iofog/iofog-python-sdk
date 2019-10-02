# iofog-python-sdk

This SDK is divided in two parts: client and deploy.

## Installation

Install python package:
```bash
sudo python2 -m pip install iofog-python-sdk
```

## Client

This module lets you easily build an ioElement. It gives you all the functionality to interact with ioFog via Local API. It contains all necessary methods for IoMessage transformation as well.

 - send new message to ioFog (post_message)
 - fetch next unread messages from ioFog (get_next_messages)
 - fetch messages for time period and list of accessible publishers (get_next_messages_from_publishers_within_timeframe)
 - get config options (get_config)
 - create IoMessage, encode(decode) to(from) raw bytes, marshall(unmarshall) into(from) JSON object (IoMessage class methods)
 - connect to ioFog Control Channel via WebSocket (establish_control_ws_connection)
 - connect to ioFog Message Channel via WebSocket (establish_message_ws_connection) and publish new message via this channel (post_message_via_socket)

### Code snippets: 

Import iofog client and additional classes to your project:
```python
from iofog_python_sdk.client.client import IoFogClient
from iofog_python_sdk.client.exception import IoFogException
from iofog_python_sdk.client.iomessage import IoMessage
from iofog_python_sdk.client.listener import *
```

Create IoFog client with default settings:
```python
try:
    client = IoFogClient()
except IoFogException as e:
 # client creation failed, e contains description
```

Or specify host, port, ssl and container id explicitly:
```python
try:
    client = IoFogClient(id='container_id', host='iofog_host', port=6666)
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


##### WebSocket calls

To use websocket connections you should implement listeners as follows:
```python
class MyControlListener(IoFogControlWsListener):
    def on_control_signal(self):
        # do smth on control signal


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
## Deploy

This module lets you easily communicate with the [Controller REST API](https://iofog.org/docs/1.3.0/controllers/rest-api.html).

 - Deploy flow, microservices, agents, etc.
 - Edit microservice configuration
 - Edit flow routing
 
 ### Code snippets
 
Import iofog deploy client
```python
from iofog_python_sdk.deploy.create_rest_call import rest_call
from iofog_python_sdk.deploy.microservice_service import microservices
```

Update microservice config
```python
controller_address = http://localhost:51121/api/v3
microservice_service = microservices()

def iofog_auth(controller_address, email, password):
    data = {}
    data["email"] = email
    data["password"] = password
    post_address = "{}/user/login".format(controller_address)
    jsonResponse = rest_call(data, post_address)
    auth_token = jsonResponse["accessToken"]
    return auth_token

auth_token = iofog_auth(controller_address, "user@domain.com", "myPassword")
flow_id = 1
current_microservice = microservice_service.get_microservice_by_name(controller_address, "my_microservice", flow_id, auth_token)

updated_microservice = current_microservice
updated_microservice.config = {"newKey": 42}

microservice_service.update_microservice(controller_address, updated_microservice, current_microservice.iofogUuid, catalog_id, auth_token)

```

#### Disclaimer

This module is very much a Work In Progress. It was first written as a set of helper functions used by a python script to deploy a set of microservices configured using yaml files.

Our [golang SDK](https://github.com/eclipse-iofog/iofog-go-sdk) is more adapted and modular for communicating with the Controller REST API
