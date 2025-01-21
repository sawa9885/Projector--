import requests

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
        self.states = {device["device_id"]: None for device in devices}  # Track the state of each device

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
        desired_state = "on" if mode == "desk" else "off"

        for device in self.devices:
            device_id = device["device_id"]
            model = device["sku"]

            # Check if the device already has the desired state
            if self.states[device_id] == desired_state:
                results.append({
                    "device_id": device_id,
                    "status": "success",
                    "message": f"Ceiling Light {device_id} was already {desired_state}."
                })
                continue

            # Send the command to update the device state
            result = self._send_command(device_id, model, "turn", desired_state)
            if "error" in result:
                results.append({
                    "device_id": device_id,
                    "status": "error",
                    "message": result["error"]
                })
            else:
                self.states[device_id] = desired_state  # Update the state
                results.append({
                    "device_id": device_id,
                    "status": "success",
                    "message": f"Ceiling Light {device_id} turned {desired_state}."
                })

        return results
