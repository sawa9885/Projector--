import requests
import time

class CeilingLights:
    def __init__(self, api_key, devices):
        """
        Initialize the Ceiling Lights controller.
        :param api_key: Your Govee API key.
        :param devices: A list of dictionaries with device details (ID and SKU/model).
        """
        self.api_key = api_key
        self.devices = devices
        self.base_url = "https://developer-api.govee.com/v1/devices/control"

    def _send_command(self, device_id, model, command, value):
        """
        Send a command to the Govee device.
        :param device_id: The unique ID of the device.
        :param model: The SKU/model of the device.
        :param command: The command to send (e.g., "turn").
        :param value: The value of the command (e.g., "on" or "off").
        :return: API response or error message.
        """
        headers = {
            "Govee-API-Key": self.api_key,
            "Content-Type": "application/json",
        }
        payload = {
            "device": device_id,
            "model": model,
            "cmd": {
                "name": command,
                "value": value,
            },
        }

        try:
            response = requests.put(self.base_url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def set_mode(self, mode):
        """
        Set the mode for the Ceiling Lights (desk, projector, bedtime).
        :param mode: The desired mode (desk, projector, bedtime).
        :return: Results for each device.
        """
        results = []
        for device in self.devices:
            device_id = device["device_id"]
            model = device["sku"]

            if mode == "desk":
                # Turn on the lights
                result_on = self._send_command(device_id, model, "turn", "on")
                results.append({"device_id": device_id, "mode": mode, "result": result_on})

            elif mode in ["projector", "bedtime"]:
                # Turn off the lights
                result_off = self._send_command(device_id, model, "turn", "off")
                results.append({"device_id": device_id, "mode": mode, "result": result_off})

            else:
                # Invalid mode
                results.append({"device_id": device_id, "mode": mode, "result": {"error": f"Invalid mode: {mode}"}})

        return results


if __name__ == "__main__":
    # Your Govee API key
    API_KEY = "5e6a480a-716a-4ad9-bf9c-67413c645028"

    # Device details
    DEVICES = [
        {"device_id": "48:0E:D0:C9:07:BA:4D:A0", "sku": "H6008"},
        {"device_id": "7E:2C:D0:C9:07:BA:D0:A0", "sku": "H6008"},
    ]

    # Initialize Ceiling Lights
    ceiling_lights = CeilingLights(api_key=API_KEY, devices=DEVICES)

    # Test modes
    modes = ["projector", "desk", "bedtime", "invalid"]
    for mode in modes:
        print(f"Setting mode to {mode}...")
        responses = ceiling_lights.set_mode(mode)
        for response in responses:
            print("Response:", response)
        print("-" * 40)
        time.sleep(2)  # Delay between tests
