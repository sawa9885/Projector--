import requests
import time

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
        if mode == "desk":
            # Turn on the Desk Lights
            result = self._send_command("turn", "on")
        elif mode in ["projector", "bedtime"]:
            # Turn off the Desk Lights
            result = self._send_command("turn", "off")
        else:
            # Invalid mode
            return {"status": "error", "message": f"Invalid mode: {mode}"}

        if "error" in result:
            return {"status": "error", "message": result["error"]}

        return {"status": "success", "message": f"Desk Lights mode set to {mode}"}

if __name__ == "__main__":
    # Your Govee API key
    API_KEY = "5e6a480a-716a-4ad9-bf9c-67413c645028"

    # Device details for Desk Lights
    DEVICE_ID = "D4:CA:D5:0E:C2:06:5C:5C"
    MODEL = "H6056"

    # Initialize Desk Lights
    desk_lights = DeskLights(api_key=API_KEY, device_id=DEVICE_ID, model=MODEL)

    # Test modes
    modes = ["projector", "desk", "bedtime", "invalid"]
    for mode in modes:
        print(f"Setting mode to {mode}...")
        response = desk_lights.set_mode(mode)
        print("Response:", response)
        time.sleep(2)  # Delay between tests
