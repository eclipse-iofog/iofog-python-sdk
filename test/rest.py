from iofog_python_sdk.rest.controller.client import *
import sys


def main():
    client = Client(host=sys.argv[1],
                    port=sys.argv[2],
                    email=sys.argv[3],
                    password=sys.argv[4])
    
    status = client.get_status()
    print(status)

    name = "name"
    client.delete_agent(name)

    client.create_agent(name, "localhost")

    key = client.get_provision_key(name)
    print(key)

    client.delete_agent(name)

if __name__ == "__main__":
    main()