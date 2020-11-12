#********************************************************************************
#  Copyright (c) 2018 Edgeworx, Inc.
#
#  This program and the accompanying materials are made available under the
#  terms of the Eclipse Public License v. 2.0 which is available at
#  http://www.eclipse.org/legal/epl-2.0
#
#  SPDX-License-Identifier: EPL-2.0
#********************************************************************************

IOFOG = 'iofog'

PORT_IOFOG = 54321
SELFNAME = 'SELFNAME'
SSL = 'SSL'
SSL_DEFAULT = False
HOST_DEFAULT = '127.0.0.1'
IOFOG_LOGGER = 'iofog_logger'

URL_GET_CONFIG = '/v2/config/get'
URL_GET_EDGE_RESOURCES = '/v2/edgeResources'
URL_GET_NEXT_MESSAGES = '/v2/messages/next'
URL_GET_PUBLISHERS_MESSAGES = '/v2/messages/query'
URL_POST_MESSAGE = '/v2/messages/new'
URL_GET_CONTROL_WS = '/v2/control/socket/id/'
URL_GET_MESSAGE_WS = '/v2/message/socket/id/'

APPLICATION_JSON = 'application/json'
HTTP = 'http'
HTTPS = 'https'
WS = 'ws'
WSS = 'wss'

CODE_ACK = 0xB
CODE_CONTROL_SIGNAL = 0xC
CODE_MSG = 0xD
CODE_RECEIPT = 0xE
CODE_EDGE_RESOURCE_SIGNAL = 0xF

WS_ATTEMPT_LIMIT = 5
IO_MESSAGE_VERSION = 4

WS_CONNECT_TIMEOUT = 1
PING_INTERVAL_SECONDS = 5
CODE_BAD_REQUEST = 400

ID = 'id'
TAG = 'tag'
GROUP_ID = 'groupid'
VERSION = 'version'
SEQUENCE_NUMBER = 'sequencenumber'
SEQUENCE_TOTAL = 'sequencetotal'
PRIORITY = 'priority'
TIMESTAMP = 'timestamp'
PUBLISHER = 'publisher'
AUTH_ID = 'authid'
AUTH_GROUP = 'authgroup'
CHAIN_POSITION = 'chainposition'
HASH = 'hash'
PREVIOUS_HASH = 'previoushash'
NONCE = 'nonce'
DIFFICULTY_TARGET = 'difficultytarget'
INFO_TYPE = 'infotype'
INFO_FORMAT = 'infoformat'
CONTEXT_DATA = 'contextdata'
CONTENT_DATA = 'contentdata'

TIME_FRAME_START = 'timeframestart'
TIME_FRAME_END = 'timeframeend'
PUBLISHERS = 'publishers'
CONFIG = 'config'
EDGE_RESOURCES = 'edgeResources'
MESSAGES = 'messages'
STATUS = 'status'
COUNT = 'count'
