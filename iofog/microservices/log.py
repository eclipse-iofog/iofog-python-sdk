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
import json_logging, logging
import datetime
import json
import os
import socket

DEVICE_KEY="deviceId"
MSG_KEY="msg"
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
                           "message": content[MSG_KEY]}
        if DEVICE_KEY in content:
            json_log_object[DEVICE_KEY] = content[DEVICE_KEY]
        return json.dumps(json_log_object)

json_logging.init_non_web(custom_formatter=CustomJSONLog, enable_json=True)

def encode_content(msg, id):
    if id is None:
        return json.dumps({MSG_KEY: msg})
    return json.dumps({MSG_KEY: msg, DEVICE_KEY: id})

class Logger:

    def __init__(self, name, device_id=None, log_dir=None):
        self.logger = logging.getLogger(name)
        self.device_id = device_id
        # Create log file
        if log_dir is None:
            log_dir = "/var/log/iofog-microservices"
        else:
            log_dir = log_dir.rstrip('/')
        self.file = "{}/{}.log".format(log_dir, name)
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

