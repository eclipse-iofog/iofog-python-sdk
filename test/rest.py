import pytest
from iofog.rest.controller.client import Client

class TestFullState:
    def __init__(self):
        self.email = "serge@edgeworx.io"
        self.password = "wfhoi982bv1sfdjoi"
        self.name = "Serge"
        self.surname = "Radinovich"
        self.controller_address = "localhost"
        self.controller_port = 51121

state = TestFullState()

@pytest.fixture(autouse=True)
def _fixture():
    return state

@pytest.mark.dependency()
def test_create_user(_fixture):
    _fixture.client = Client(_fixture.controller_address,
                             _fixture.controller_port,
                             _fixture.email,
                             _fixture.password,
                             _fixture.name,
                             _fixture.surname)

@pytest.mark.dependency(depends=["test_create_user"])
def test_get_status(_fixture):
    status = _fixture.client.get_status()
    assert isinstance(status, dict)
    assert status["status"] == "online"
    assert isinstance(status["timestamp"], int)
    assert isinstance(status["uptimeSec"], float)
    assert isinstance(status["versions"], dict)
    assert isinstance(status["versions"]["controller"], str)
    assert isinstance(status["versions"]["ecnViewer"], str)

@pytest.mark.dependency(depends=["test_create_user"])
def test_create_agent(_fixture):
    name = "agent-1"
    uuid = _fixture.client.create_agent(name, "localhost", "x86")
    assert isinstance(uuid, str)
    assert(_fixture.client.get_agent_uuid(name) == uuid)

@pytest.mark.dependency(depends=["test_create_agent"])
def test_create_app(_fixture):
    resp = _fixture.client.create_app_from_yaml("test/conf/app.yaml")
    assert isinstance(resp, dict)
    print(resp)

@pytest.mark.dependency(depends=["test_create_app"])
def test_delete_app(_fixture):
    _fixture.client.delete_app("func-app")

@pytest.mark.dependency(depends=["test_delete_app"])
def test_delete_agent(_fixture):
    name = "agent-1"
    _fixture.client.delete_agent(name)
