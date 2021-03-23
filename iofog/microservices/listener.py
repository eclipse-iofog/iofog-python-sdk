#********************************************************************************
#  Copyright (c) 2018 Edgeworx, Inc.
#
#  This program and the accompanying materials are made available under the
#  terms of the Eclipse Public License v. 2.0 which is available at
#  http://www.eclipse.org/legal/epl-2.0
#
#  SPDX-License-Identifier: EPL-2.0
#********************************************************************************

class IoFogControlWsListener:
    def __init__(self):
        pass

    def on_control_signal(self):
        pass

    def on_edge_resources_signal(self):
        pass


class IoFogMessageWsListener:
    def __init__(self):
        pass

    def on_message(self, io_msg):
        pass

    def on_receipt(self, message_id, timestamp):
        pass
