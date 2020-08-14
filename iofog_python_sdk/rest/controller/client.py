from iofog_python_sdk.rest.controller.request import *


class Client:
    """
    Iofog Controller REST API client.
    """

    def __init__(self, host, port, email, password):
        self.base_path = "http://" + host + ":" + str(port) + "/api/v3"
        self._login(email, password)
    
    def _login(self, email, password):
        url = "{}/user/login".format(self.base_path)
        body = {
            "email": email,
            "password": password
        }
        self.token = request("POST", url, "", body)["accessToken"]
    
    def get_status(self):
        url = "{}/status".format(self.base_path)
        return request("GET", url)

    def create_agent(self, name, host):
        url = "{}/iofog".format(self.base_path)
        body = {
            "name": name,
            "fogType": 0,
            "host": host
        }
        return request("POST", url, self.token, body)["uuid"]

    def _get_provision_key(self, agent_id):
        url = "{}/iofog/{}/provisioning-key".format(self.base_path, agent_id)
        return request("GET", url, self.token)["key"]
    
    def _delete_agent(self, agent_id):
        url = "{}/iofog/{}".format(self.base_path, agent_id)
        request("DELETE", url, self.token)
    
    def _get_agent_id(self, name):
        url = "{}/iofog-list".format(self.base_path)
        resp = request("GET", url, self.token)
        for fog in resp["fogs"]:
            if fog["name"] == name:
                return fog["uuid"]

    def delete_agent(self, name):
        id = self._get_agent_id(name)
        if id is not None:
            self._delete_agent(id)
    
    def get_provision_key(self, agent_name):
        id = self._get_agent_id(agent_name)
        if id is not None:
            return self._get_provision_key(id)