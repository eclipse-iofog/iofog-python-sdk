#********************************************************************************
#  Copyright (c) 2018 Edgeworx, Inc.
#
#  This program and the accompanying materials are made available under the
#  terms of the Eclipse Public License v. 2.0 which is available at
#  http://www.eclipse.org/legal/epl-2.0
#
#  SPDX-License-Identifier: EPL-2.0
#********************************************************************************

from logging.handlers import RotatingFileHandler
import json_logging, logging, sys
import datetime
import traceback
import json
import os
import socket

hostname = socket.gethostname()

class CustomJSONLog(logging.Formatter):
    """
    Customized logger
    """

    def format(self, record):
        content = json.loads(record.getMessage())
        json_log_object = {"timestamp": datetime.datetime.utcnow().isoformat(),
                           "hostname": hostname,
                           "level": record.levelname.lower(),
                           "message": content["msg"],
                           "device": content["deviceId"]
                           }
        return json.dumps(json_log_object)

json_logging.init_non_web(custom_formatter=CustomJSONLog, enable_json=True)

def encode_content(msg, id):
    content = {
        "msg": msg,
        "deviceId": id
    }
    return json.dumps(content)

class Logger:

    def __init__(self, name, device_id):
        self.logger = logging.getLogger(name)
        self.device_id = device_id
        # Create log file
        self.file = "/var/log/iofog-microservices/{}.log".format(name)
        if not os.path.exists(self.file):
            with open(self.file, 'w+') as f:
                pass
        # Register log file
        self.logger.addHandler(RotatingFileHandler(filename=self.file, maxBytes=10*1024*1024, backupCount=5))

    def info(self, msg):
        self.logger.setLevel(logging.INFO)
        self.logger.info(encode_content(msg, self.device_id))

    def debug(self, msg):
        self.logger.setLevel(logging.DEBUG)
        self.logger.debug(encode_content(msg, self.device_id))

    def warning(self, msg):
        self.logger.setLevel(logging.WARN)
        self.logger.warning(encode_content(msg, self.device_id))

    def error(self, msg):
        self.logger.setLevel(logging.ERROR)
        self.logger.error(encode_content(msg, self.device_id))


if __name__=="__main__": 
    logger = Logger("serge", "123142123")
    logger.info("hellow")
    logger.debug("hellow")
    logger.warning("hellow")
    logger.error("hellow")