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

class Logger():
    """
    ioFog Logging Client
    """

    def __init__(self, name, handlers = [logging.StreamHandler(sys.stdout)]):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        for handler in handlers:
            self.logger.addHandler(handler)
    
    def info(self, msg):
        self.logger.info(msg)

    def debug(self, msg):
        self.logger.debug(msg)

    def warn(self, msg):
        self.logger.warn(msg)

    def error(self, msg):
        self.logger.error(msg)

#if __name__ == "__main__":
#    log = Logger("serge")
#    log.info("hi")
#    log2 = Logger("serge2", [logging.FileHandler("/tmp/log.txt")])
#    log2.debug("hi")
