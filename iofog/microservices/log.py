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
        json_log_object = {"timestamp": datetime.datetime.utcnow().isoformat(),
                           "level": record.levelname.lower(),
                           "message": record.getMessage(),
                           "hostname": hostname
                           }
        return json.dumps(json_log_object)

json_logging.init_non_web(custom_formatter=CustomJSONLog, enable_json=True)

class BaseLogger():

    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
    
    def info(self, msg):
        self.logger.info(msg)

    def debug(self, msg):
        self.logger.debug(msg)

    def warn(self, msg):
        self.logger.warn(msg)

    def error(self, msg):
        self.logger.error(msg)

class Logger(BaseLogger):

    def __init__(self, name):
        super().__init__(name)
        # Create log file
        self.file = "/var/log/iofog-microservices/{}.log".format(name)
        if not os.path.exists(self.file):
            with open(self.file, 'w+') as f:
                pass
        # Register log file
        self.logger.addHandler(RotatingFileHandler(filename=self.file, maxBytes=10*1024*1024, backupCount=5))

    def info(self, msg):
        super().info(msg)

    def debug(self, msg):
        super().debug(msg)

    def warn(self, msg):
        super().warn(msg)

    def error(self, msg):
        super().error(msg)

