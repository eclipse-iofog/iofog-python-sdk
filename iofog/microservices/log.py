#********************************************************************************
#  Copyright (c) 2018 Edgeworx, Inc.
#
#  This program and the accompanying materials are made available under the
#  terms of the Eclipse Public License v. 2.0 which is available at
#  http://www.eclipse.org/legal/epl-2.0
#
#  SPDX-License-Identifier: EPL-2.0
#********************************************************************************

import json_logging, logging, sys
import datetime
import traceback
import json
import os

class CustomJSONLog(logging.Formatter):
    """
    Customized logger
    """

    def format(self, record):
        json_log_object = {"timestamp": datetime.datetime.utcnow().isoformat(),
                           "level": record.levelname.lower(),
                           "message": record.getMessage(),
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
        log_file = "/var/log/iofog-microservices/{}.log".format(name)
        if not os.path.exists(log_file):
            with open(log_file, 'w'):
                pass
        # Register log file
        self.logger.addHandler(logging.FileHandler(log_file))

if __name__ == "__main__":
    log = Logger("werserge")
    log.info("hi")
