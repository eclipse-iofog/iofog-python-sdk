from iofog_python_sdk.create_rest_call import rest_call
from iofog_python_sdk.pretty_print import print_info
from iofog_python_sdk.microservice_service import microservices as msv


class catalog_service:
    def create_catalog_curl_data(self, catalog_item):
        data = {}
        data["name"] = catalog_item["name"]
        data["images"] = []
        data["images"].append({'containerImage': '{}'.format(catalog_item["images"]["arm"]), 'fogTypeId': 2})
        data["images"].append({'containerImage': '{}'.format(catalog_item["images"]["x86"]), 'fogTypeId': 1})
        data["registryId"] = 1

        return data

    def update_catalog(self, controller_address, auth_token, catalog_item):
        # Delete all microservices that uses this specific catalog item
        print_info("====> Deleting all microservices currently using this catalog item")
        microself = msv()
        msv.delete_all_by_catalog_id(microself, controller_address, auth_token, catalog_item["id"])
        # Update catalog item
        data = catalog_service.create_catalog_curl_data(self, catalog_item)
        if data == {}:
            # If data has failed to be created, exit here, and echo which service failed
            return "{} failed to create curl data".format(catalog_item)
        post_address = "{}/catalog/microservices/{}".format(controller_address, catalog_item["id"])
        json_response = rest_call(data, post_address, auth_token, method="PATCH").response

    def add_to_catalog(self, controller_address, auth_token, catalog_item):
        data = catalog_service.create_catalog_curl_data(self, catalog_item)
        if data == {}:
            # If data has failed to be created, exit here, and echo which service failed
            return "{} failed to create curl data".format(catalog_item)
        post_address = "{}/catalog/microservices".format(controller_address)
        return rest_call(data, post_address, auth_token).response["id"]


    def delete_by_id(self, controller_address, catalog_id, auth_token):
        post_address = "{}/catalog/microservices/{}".format(controller_address, catalog_id)
        return rest_call({}, post_address, auth_token, method="DELETE").response


    def delete_items(self, controller_address, catalog_items, auth_token):
        for catalog_id in catalog_items:
            catalog_service.delete_by_id(self, controller_address, catalog_id, auth_token)

    def get_catalog(self, controller_address, auth_token):
        post_address = "{}/catalog/microservices".format(controller_address)
        return rest_call({}, post_address, auth_token, method="GET").response["catalogItems"]

    def get_catalog_item_by_name(self, controller_address, name, auth_token):
        catalog_items = catalog_service.get_catalog(self, controller_address, auth_token)
        return next((x for x in catalog_items if x["name"] == name), None)

    def is_same(self, yaml_item, existing_item):
        if len(yaml_item["images"]) != len(existing_item["images"]):
            return False
        for image_type in yaml_item["images"]:
            image = yaml_item["images"][image_type]
            same = next((x for x in existing_item["images"] if (image_type == "x86" and x["fogTypeId"] == 1 and x["containerImage"] == image) or (image_type == "arm" and x["fogTypeId"] == 2 and x["containerImage"] == image)), False)
            if same == False:
                return False
        return True

    def setup(self, controller_address, auth_token, microservices):
        # For each microservice check if catalog item exists
        print_info("====> Reading the catalog")
        updated = False
        existing_catalog_items = catalog_service.get_catalog(self, controller_address, auth_token)
        catalog_ids = {}
        for microserviceKey in microservices:
            microservice = microservices[microserviceKey]
            catalog_item = {
                "images": microservice["images"],
                "name": microservice["microservice"]["name"] + "_catalog"
            }
            catalog_id = ""
            existing_catalog_item = next((x for x in existing_catalog_items if x["name"] == catalog_item["name"]), None)
            # If it does not exists yet, create
            if  existing_catalog_item == None:
                print_info("====> Adding to the catalog")
                updated = True
                catalog_id = catalog_service.add_to_catalog(self, controller_address, auth_token, catalog_item)
            # Otherwise, patch to update images
            else:
                catalog_item["id"] = existing_catalog_item["id"]
                # Check if images have changed
                if catalog_service.is_same(self, catalog_item, existing_catalog_item) == False:
                    print_info("====> Updating a catalog item (Delete / Recreate)")
                    updated = True
                    # update_catalog(controller_address, auth_token, catalog_item)
                    catalog_service.delete_by_id(self, controller_address, existing_catalog_item["id"], auth_token)
                    catalog_id = catalog_service.add_to_catalog(self, controller_address, auth_token, catalog_item)
                else:
                    catalog_id = catalog_item["id"]
            catalog_ids[microserviceKey] = catalog_id
        if updated == False:
            print_info("====> Catalog is up-to-date")
        else:
            print_info("====> Catalog updated")
        return catalog_ids
