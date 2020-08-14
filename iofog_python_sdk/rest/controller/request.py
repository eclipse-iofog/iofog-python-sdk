import requests
import json


def request(method, address, auth_token="", body={}):
    switch = {
        "POST": requests.post,
        "GET": requests.get,
        "DELETE": requests.delete,
        "PATCH": requests.patch,
    }
    headers = {}
    data = {}
    if body:
        headers["Content-Type"] = 'application/json'
        data = json.dumps(body, indent=4)

    if auth_token:
        headers["Authorization"] = auth_token
    else:
        headers["cache-control"] = "no-cache"

    response = switch[method](address, data=data, headers=headers, timeout=30)
    response.raise_for_status()
    responseDict = {}
    if response.content:
        responseDict = json.loads(response.content)
    return responseDict