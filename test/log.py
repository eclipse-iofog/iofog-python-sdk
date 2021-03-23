import pytest
import random
import string
from iofog.microservices.log import Logger

@pytest.fixture(autouse=True)
def _fixture():
    return {}

@pytest.mark.dependency()
def test_first_logger(_fixture):
    id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    logger = Logger(name, device_id=id, log_dir="/tmp")
    logger.info("hello")
    logger.debug("world")
    logger.warning("good")
    logger.error("bye")
    with open("/tmp/{}.log".format(name)) as log_file:
        for line in log_file:
            assert id in line
            assert "deviceId" in line
            assert "message" in line
            assert "level" in line
            assert "hostname" in line
            assert "timestamp" in line


@pytest.mark.dependency()
def test_second_logger(_fixture):
    name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    logger = Logger(name, log_dir="/tmp/")
    logger.info("hello")
    logger.debug("world")
    logger.warning("good")
    logger.error("bye")
    with open("/tmp/{}.log".format(name)) as log_file:
        for line in log_file:
            assert "deviceId" not in line
            assert "message" in line
            assert "level" in line
            assert "hostname" in line
            assert "timestamp" in line