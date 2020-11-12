#********************************************************************************
#  Copyright (c) 2018 Edgeworx, Inc.
#
#  This program and the accompanying materials are made available under the
#  terms of the Eclipse Public License v. 2.0 which is available at
#  http://www.eclipse.org/legal/epl-2.0
#
#  SPDX-License-Identifier: EPL-2.0
#********************************************************************************

import json

try:
    from urllib.error import HTTPError #for python 3
except ImportError:
    from urllib2 import HTTPError #for python 2

from iofog.microservices.definitions import *
from iofog.microservices.util import make_post_request
from iofog.microservices.iomessage import IoMessage
from iofog.microservices.exception import IoFogHttpException


class IoFogHttpClient:
    def __init__(self, container_id, ssl, host, port):
        protocol_rest = HTTP
        if ssl:
            protocol_rest = HTTPS

        self.url_base_rest = "{}://{}:{}".format(protocol_rest, host, port)
        self.url_get_config = self.url_base_rest + URL_GET_CONFIG
        self.url_get_edge_resources = self.url_base_rest + URL_GET_EDGE_RESOURCES
        self.url_get_next_messages = self.url_base_rest + URL_GET_NEXT_MESSAGES
        self.url_get_publishers_messages = self.url_base_rest + URL_GET_PUBLISHERS_MESSAGES
        self.url_post_message = self.url_base_rest + URL_POST_MESSAGE
        self.request_body_id = json.dumps({
            ID: container_id
        })

    def get_config(self):
        try:
            config_resp = make_post_request(self.url_get_config, APPLICATION_JSON, self.request_body_id)
        except HTTPError as e:
            raise IoFogHttpException(e.code, e.read())
        return json.loads(config_resp[CONFIG])
    
    def get_edge_resources(self):
        try:
            edge_resources_response = make_get_request(self.url_get_edge_resources, APPLICATION_JSON, self.request_body_id)
        except HTTPError as e:
            raise IoFogHttpException(e.code, e.read())
        return json.loads(edge_resources_response[EDGE_RESOURCES])

    def get_next_messages(self):
        try:
            next_messages_resp = make_post_request(self.url_get_next_messages, APPLICATION_JSON, self.request_body_id)
        except HTTPError as e:
            raise IoFogHttpException(e.code, e.read())
        messages = []
        for json_msg in next_messages_resp[MESSAGES]:
            messages.append(IoMessage.from_json(json_msg))
        return messages

    def get_next_messages_from_publishers_within_timeframe(self, query):
        try:
            next_messages_resp = make_post_request(self.url_get_publishers_messages, APPLICATION_JSON,
                                                   json.dumps(query))
        except HTTPError as e:
            raise IoFogHttpException(e.code, e.read())
        response = {
            TIME_FRAME_START: next_messages_resp[TIME_FRAME_START],
            TIME_FRAME_END: next_messages_resp[TIME_FRAME_END]
        }
        messages = []
        for json_msg in next_messages_resp[MESSAGES]:
            messages.append(IoMessage.from_json(json_msg))
        response[MESSAGES] = messages
        return response

    def post_message(self, io_msg):
        try:
            post_resp = make_post_request(self.url_post_message, APPLICATION_JSON, io_msg.to_json())
            del post_resp[STATUS]
            return post_resp
        except HTTPError as e:
            raise IoFogHttpException(e.code, e.read())
