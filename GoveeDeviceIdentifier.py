import requests

API_KEY = "5e6a480a-716a-4ad9-bf9c-67413c645028"
BASE_URL = "https://developer-api.govee.com/v1/devices"

headers = {
    "Govee-API-Key": API_KEY
}

response = requests.get(BASE_URL, headers=headers)

if response.status_code == 200:
    devices = response.json().get("data", {}).get("devices", [])
    for device in devices:
        print("Device Name:", device["deviceName"])
        print("Device ID:", device["device"])
        print("Model:", device["model"])
        print("---")
else:
    print("Failed to retrieve devices:", response.json())
