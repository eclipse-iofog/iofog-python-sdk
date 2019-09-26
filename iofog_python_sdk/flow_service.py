from iofog_python_sdk.create_rest_call import rest_call
import time


class Flow:

    def __init__(self):
        self.id = ""

    def create_flow(self, controller_address, auth_token, flow):
        data = {}

        data["name"] = flow
        post_address = "{}/flow".format(controller_address)
        jsonResponse = rest_call(data, post_address, auth_token).response
        self.id = jsonResponse["id"]

    def create_flow_if_not_exist(self, controller_address, auth_token, flow):
        try:
          id = Flow.get_id(self, controller_address, flow, auth_token)
          return id
        except StopIteration:
          return Flow.create_flow(self, controller_address, auth_token, flow)

    def restart_flow(self, controller_address, flow_id, flow_name, auth_token):
      flow = Flow.get_flow_by_id(self, controller_address, flow_id, auth_token)
      if flow.get("isActivated", False) == True:
        Flow.stop_flow(self, controller_address, flow_id, flow_name, auth_token)
        time.sleep(3)
      Flow.start_flow(self, controller_address, flow_id, flow_name, auth_token)

    def start_flow(self, controller_address, flow_id, flow_name, auth_token):
        data = {}
        data["name"] = flow_name
        data["isActivated"] = True
        post_address = "{}/flow/{}".format(controller_address, flow_id)
        jsonRespone = rest_call(data, post_address, auth_token, method="PATCH").response

    def stop_flow(self, controller_address, flow_id, flow_name, auth_token):
        data = {}
        data["name"] = flow_name
        data["isActivated"] = False
        post_address = "{}/flow/{}".format(controller_address, flow_id)
        jsonRespone = rest_call(data, post_address, auth_token, method="PATCH").response

    def delete_flow(self, controller_address, flow_id, auth_token):
        data = {}
        post_address = "{}/flow/{}".format(controller_address, flow_id)
        jsonRespone = rest_call(data, post_address, auth_token, method="DELETE").response

    def get_flow_by_name(self, controller_address, flow_name, auth_token):
        flows = Flow.get_all(self, controller_address, auth_token)
        return next(x for x in flows if x["name"] == flow_name)

    def get_flow_by_id(self, controller_address, flow_id, auth_token):
        data = {}
        post_address = "{}/flow/{}".format(controller_address, flow_id)
        json_response = rest_call(data, post_address, auth_token, method="GET").response
        return json_response

    def get_id(self, controller_address, flow_name, auth_token):
        self.id = Flow.get_flow_by_name(self, controller_address, flow_name, auth_token)["id"]

    def get_all(self, controller_address, auth_token):
        data = {}
        flow_ids = {}
        post_address = "{}/flow".format(controller_address)
        json_response = rest_call(data, post_address, auth_token, method="GET").response
        return json_response["flows"]
