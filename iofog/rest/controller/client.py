from iofog.rest.controller.request import *
import yaml

class Client:
    """
    Iofog Controller REST API client.
    """


    def __init__(self, base_url , email, password, name="", surname=""):
        self.base_url = base_url
        try:
            self._login(email, password)
        except Exception:
            if name == "" or surname == "":
                raise Exception("Must provide name and surname if User does not already exist")
            self.create_user(email, password, name, surname)
            self._login(email, password)
        self.error_yaml_spec = "YAML file does not follow required specification. See https://iofog.org/docs/2/reference-iofogctl/reference-application.html"

    def create_user(self, email, password, name, surname):
        url = "{}/user/signup".format(self.base_url)
        body = {
            "email": email,
            "password": password,
            "lastName": name,
            "firstName": surname
        }
        return request("POST", url, "", body)

    def _login(self, email, password):
        url = "{}/user/login".format(self.base_url)
        body = {
            "email": email,
            "password": password
        }
        self.token = request("POST", url, "", body)["accessToken"]

    def get_status(self):
        url = "{}/status".format(self.base_url)
        return request("GET", url)

    def create_agent(self, name, host, arch=""):
        fog_type_id = 0
        if arch != "":
            if arch not in [ "x86", "arm" ]:
                raise Exception("Agent architecture {} not supported".format(arch))
            fog_type_id = 1 if arch == "x86" else 2
        url = "{}/iofog".format(self.base_url)
        body = {
            "name": name,
            "fogType": fog_type_id,
            "host": host
        }
        return request("POST", url, self.token, body)["uuid"]

    def _get_provision_key(self, agent_id):
        url = "{}/iofog/{}/provisioning-key".format(self.base_url, agent_id)
        return request("GET", url, self.token)["key"]
    
    def _delete_agent(self, agent_id):
        url = "{}/iofog/{}".format(self.base_url, agent_id)
        request("DELETE", url, self.token)
    
    def get_agent_uuid(self, name):
        url = "{}/iofog-list".format(self.base_url)
        resp = request("GET", url, self.token)
        for fog in resp["fogs"]:
            if fog["name"] == name:
                return fog["uuid"]

    def delete_agent(self, name):
        uuid = self.get_agent_uuid(name)
        if uuid is not None:
            self._delete_agent(uuid)
    
    def get_provision_key(self, agent_name):
        uuid = self.get_agent_uuid(agent_name)
        if uuid is None:
            raise Exception("Could not get Agent UUID")
        return self._get_provision_key(uuid)

    def upgrade_agent(self, agent_name):
        uuid = self.get_agent_uuid(agent_name)
        url = "{}/iofog/{}/version/upgrade".format(self.base_url, uuid)
        return request("POST", url, self.token)

    def patch_agent(self, agent_name, config):
        uuid = self.get_agent_uuid(agent_name)
        url = "{}/iofog/{}".format(self.base_url, uuid)
        return request("PATCH", url, self.token, config)

    def create_app(self, name, msvcs, routes):
        if routes is None:
            routes = []
        url = "{}/application/".format(self.base_url)
        body = {
            "name": name,
            "routes": routes,
            "microservices": msvcs,
            "isActivated": True,
            "isSystem": False
        }
        return request("POST", url, self.token, body)
    
    def create_app_from_yaml(self, file):
        with open(file) as file:
            doc = yaml.full_load(file)
        if "metadata" not in doc or "spec" not in doc or "microservices" not in doc["spec"]:
            raise Exception(self.error_yaml_spec)
        name = doc["metadata"]["name"]
        msvcs = doc["spec"]["microservices"]
        routes = None
        if "routes" in doc["spec"]:
            routes = doc["spec"]["routes"]
        json_msvcs = self._jsonify_yaml_msvcs(msvcs)
        json_routes = self._jsonify_yaml_routes(routes)
        return self.create_app(name, json_msvcs, json_routes)

    def delete_app(self, name):
        url = "{}/application/{}".format(self.base_url, name)
        return request("DELETE", url, self.token)

    def get_app(self, name):
        url = "{}/application/{}".format(self.base_url, name)
        return request("GET", url, self.token)

    def _jsonify_yaml_routes(self, routes):
        json_routes = []
        if routes is None:
            return json_routes
        for route in routes:
            json_route = route
            json_route["name"] = "{}-{}".format(route["from"], route["to"])
        return json_routes
    
    def _jsonify_yaml_msvcs(self, msvcs):
        json_msvcs = []
        for msvc in msvcs:
            json_msvc = dict()
            # images
            images = []
            for arch in [ "x86", "arm" ]:
                if arch in msvc["images"]:
                    fog_type_id = 1 if arch == "x86" else 2
                    imageDict = {
                        "fogTypeId": fog_type_id,
                        "containerImage": msvc["images"][arch]
                    }
                    images.append(imageDict)
            json_msvc["images"] = images
            # container
            for pasta in [ "env", "rootHostAccess", "ports", "volumes", "commands" ]:
                if pasta in msvc["container"]:
                    json_msvc[pasta] = msvc["container"][pasta]
            if "volumes" in json_msvc:
                json_msvc["volumeMappings"] = json_msvc["volumes"]
                json_msvc.pop("volumes")
            # msvc
            for pasta in [ "name" ]:
                if pasta in msvc:
                    json_msvc[pasta] = msvc[pasta]
            json_msvc["registryId"] = 1
            if "config" in msvc:
                json_msvc["config"] = json.dumps(msvc["config"])
            if "env" in json_msvc:
                for env in json_msvc["env"]:
                    env["value"] = str(env["value"])
            if "ports" in json_msvc:
                for port in json_msvc["ports"]:
                    if "public" in port:
                        port["publicPort"] = port["public"]
                        port.pop("public")
            json_msvc["iofogUuid"] = self.get_agent_uuid(msvc["agent"]["name"])
            json_msvcs.append(json_msvc)
    
        return json_msvcs
