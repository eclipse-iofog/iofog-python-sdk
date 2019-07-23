#********************************************************************************
#  Copyright (c) 2018 Edgeworx, Inc.
#
#  This program and the accompanying materials are made available under the
#  terms of the Eclipse Public License v. 2.0 which is available at
#  http://www.eclipse.org/legal/epl-2.0
#
#  SPDX-License-Identifier: EPL-2.0
#********************************************************************************

from iofog_python_sdk.create_rest_call import rest_call

class agent_service:
    def get_agent_per_microservice(controller_address, auth_token, microservices):
        data = {}
        agent_uuids = {}
        post_address = "{}/iofog-list".format(controller_address)
        json_response = rest_call(data, post_address, auth_token, method="GET")
        for microserviceKey in microservices:
            microservice = microservices[microserviceKey]
            agent_uuids[microserviceKey] = next(x for x in json_response["fogs"] if x["name"] == microservice["agent-name"])
        return agent_uuids


    def get_agent_info(agent):
        config = {}
        config.update(agent)
        return config


    def update_agent(controller_address, uuid, fog_info, auth_token):
        url = "{}/iofog/{}".format(controller_address, uuid)
        return rest_call(fog_info, url, auth_token, method="PATCH").response
