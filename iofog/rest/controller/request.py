import requests
import json
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def request(method, address, auth_token="", body={}):
    retry_strategy = Retry(total=4,
                           backoff_factor=2,
                           status_forcelist=[429, 500, 502, 503, 504],
                           method_whitelist=["HEAD", "GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"])
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)
    switch = {
        "HEAD":     http.head,
        "OPTIONS":  http.options,
        "POST":     http.post,
        "PUT":      http.put,
        "GET":      http.get,
        "DELETE":   http.delete,
        "PATCH":    http.patch,
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

    if method in { "HEAD", "OPTIONS", "GET" }:
        response = switch[method](address, headers=headers, timeout=10)
    else:
        response = switch[method](address, data=data, headers=headers, timeout=10)

    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        print(e.response.content)
        raise e
    responseDict = {}
    if response.content:
        responseDict = json.loads(response.content)
    return responseDict