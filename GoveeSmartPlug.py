import requests

class GoveeSmartPlug:
    def __init__(self, api_key, device_id, model):
        """
        Initialize the Govee Smart Plug controller.
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
        :return: Response from the API.
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

        response = requests.put(self.base_url, json=payload, headers=headers)
        return response.json()

    def enable(self):
        """
        Enable (turn on) the smart plug.
        :return: Response from the API.
        """
        return self._send_command("turn", "on")

    def disable(self):
        """
        Disable (turn off) the smart plug.
        :return: Response from the API.
        """
        return self._send_command("turn", "off")


if __name__ == "__main__":
    # Your Govee API key
    API_KEY = "5e6a480a-716a-4ad9-bf9c-67413c645028"

    # Device details
    devices = {
        "DeskPower": {"device_id": "31:A1:D0:C9:07:61:85:34", "model": "H5083"},
        "SkyProjector": {"device_id": "73:51:D0:C9:07:60:3E:B8", "model": "H5083"}
    }

    # Initialize smart plugs
    desk_plug = GoveeSmartPlug(api_key=API_KEY, device_id=devices["DeskPower"]["device_id"], model=devices["DeskPower"]["model"])
    sky_plug = GoveeSmartPlug(api_key=API_KEY, device_id=devices["SkyProjector"]["device_id"], model=devices["SkyProjector"]["model"])

    # Test the DeskPower plug
    print("Turning on DeskPower...")
    response = desk_plug.enable()
    print("Response:", response)

    # Test the SkyProjector plug
    print("Turning on SkyProjector...")
    response = sky_plug.enable()
    print("Response:", response)
