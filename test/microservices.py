import pytest
from iofog.microservices.client import Client
from iofog.microservices.iomessage import IoMessage

class TestMicroservicesState:
    def __init__(self):
        self.msg = IoMessage()
        self.msg.infotype = "infotype"
        self.msg.infoformat = "infoformat"
        self.msg.tag = "tag"
        self.msg.groupid = "groupid"
        self.msg.authid = "authid"
        self.msg.authgroup = "authgroup"
        self.msg.hash = "hash"
        self.msg.previoushash = "previoushash"
        self.msg.nonce = "nonce"
        self.msg.contentdata = "python3"
        self.msg.contextdata = ""

state = TestMicroservicesState()

@pytest.fixture(autouse=True)
def _fixture():
    return state

@pytest.mark.dependency()
def test_send(_fixture):
    client = Client("sender")
    receipt = client.post_message(_fixture.msg)
    assert isinstance(receipt, dict)

@pytest.mark.dependency(depends=["test_send"])
def test_recieve(_fixture):
    client = Client("reciever")
    msgs = client.get_next_messages()
    for msg in msgs:
        assert isinstance(msg, bytes)
        assert msg == _fixture.msg.contentdata
