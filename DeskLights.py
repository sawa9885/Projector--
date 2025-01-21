import requests

class DeskLights:
    def __init__(self, api_key, device_id, model):
        """
        Initialize the Desk Lights controller.
        :param api_key: Your Govee API key.
        :param device_id: The unique ID of the device.
        :param model: The model of the Govee device.
        """
        self.api_key = api_key
        self.device_id = device_id
        self.model = model
        self.base_url = "https://developer-api.govee.com/v1/devices/control"
        self.state = "on"  # Track the current state of the device ('on' or 'off')

    def _send_command(self, command, value):
        """
        Send a command to the Govee device.
        :param command: The command to send (e.g., "turn").
        :param value: The value of the command (e.g., "on" or "off").
        :return: API response or error message.
        """
        headers = {
            "Govee-API-Key": self.api_key,
            "Content-Type": "application/json",
        }
        payload = {
            "device": self.device_id,
            "model": self.model,
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
        Set the mode for the Desk Lights (desk, projector, bedtime).
        :param mode: The desired mode (desk, projector, bedtime).
        :return: Results indicating success or failure.
        """
        try:
            desired_state = "on" if mode == "desk" else "off"

            if self.state == desired_state:
                return {
                    "status": "success",
                    "message": f"Desk Lights were already {desired_state}."
                }

            result = self._send_command("turn", desired_state)
            if "error" in result:
                return {"status": "error", "message": result["error"]}

            self.state = desired_state  # Update the current state
            return {
                "status": "success",
                "message": f"Desk Lights turned {desired_state}."
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
