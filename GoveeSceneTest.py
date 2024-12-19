import requests

class GoveeSceneQuery:
    def __init__(self, api_key):
        """
        Initialize the Govee Scene Query.
        :param api_key: Your Govee API key.
        """
        self.api_key = api_key
        self.diy_scenes_url = "https://openapi.api.govee.com/router/api/v1/device/diy-scenes"
        self.dynamic_scenes_url = "https://openapi.api.govee.com/router/api/v1/device/scenes"

    def query_diy_scenes(self, device_id, sku):
        """
        Query DIY scenes for the given device.
        :param device_id: The unique ID of the device.
        :param sku: The SKU/model of the device.
        :return: Response from the API or error message.
        """
        headers = {
            "Govee-API-Key": self.api_key,
            "Content-Type": "application/json",
        }
        payload = {
            "requestId": "unique-request-id",
            "payload": {
                "sku": sku,
                "device": device_id,
            },
        }

        try:
            response = requests.post(self.diy_scenes_url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def query_dynamic_scenes(self, device_id, sku):
        """
        Query dynamic scenes for the given device.
        :param device_id: The unique ID of the device.
        :param sku: The SKU/model of the device.
        :return: Response from the API or error message.
        """
        headers = {
            "Govee-API-Key": self.api_key,
            "Content-Type": "application/json",
        }
        payload = {
            "requestId": "unique-request-id",
            "payload": {
                "sku": sku,
                "device": device_id,
            },
        }

        try:
            response = requests.post(self.dynamic_scenes_url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

if __name__ == "__main__":
    # Your Govee API key
    API_KEY = "5e6a480a-716a-4ad9-bf9c-67413c645028"

    # Device details
    DEVICES = [
        {"device_id": "48:0E:D0:C9:07:BA:4D:A0", "sku": "H6008"},
        {"device_id": "7E:2C:D0:C9:07:BA:D0:A0", "sku": "H6008"},
    ]

    # Initialize the scene query
    scene_query = GoveeSceneQuery(api_key=API_KEY)

    # Query and print scenes for each device
    for device in DEVICES:
        print(f"Querying DIY scenes for Device ID: {device['device_id']}...")
        diy_scenes = scene_query.query_diy_scenes(device["device_id"], device["sku"])
        print("DIY Scenes Response:", diy_scenes)

        print(f"\nQuerying Dynamic scenes for Device ID: {device['device_id']}...")
        dynamic_scenes = scene_query.query_dynamic_scenes(device["device_id"], device["sku"])
        print("Dynamic Scenes Response:", dynamic_scenes)
        print("-" * 40)
