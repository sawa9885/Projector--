import time
import broadlink
import json

class Projector:
    def __init__(self, signal_storage, device_ip, device_mac):
        """
        Initialize the Projector controller.
        :param signal_storage: Path to the JSON file storing learned signals.
        :param device_ip: IP address of the BroadLink device.
        :param device_mac: MAC address of the BroadLink device.
        """
        with open(signal_storage, "r") as f:
            self.signals = json.load(f)
        self.device_ip = device_ip
        self.device_mac = device_mac
        self.device = None
        self.connected = False
        self.state = "off"  # Track the current state ('on' or 'off')
        self.connect_device()

    def connect_device(self):
        """
        Connect and authenticate with the BroadLink device.
        """
        try:
            self.device = broadlink.gendevice(0x520b, (self.device_ip, 80), bytes.fromhex(self.device_mac.replace(':', '')))
            self.device.auth()  # Authenticate with the device
            self.connected = True
        except Exception as e:
            print(f"Error connecting to BroadLink device: {e}")

    def send_signal(self, signal_code):
        """
        Send an IR or RF signal using the BroadLink device.
        :param signal_code: The code to send.
        """
        if not self.connected:
            print("Device not connected. Cannot send signals.")
            return

        try:
            signal_bytes = bytes.fromhex(signal_code)
            self.device.send_data(signal_bytes)
        except Exception as e:
            print(f"Error sending signal: {e}")

    def set_mode(self, mode):
        """
        Set the mode for the projector (desk, projector, bedtime).
        :param mode: The desired mode (desk, projector, bedtime).
        :return: Results indicating success or failure.
        """
        try:
            signal = self.signals.get("projector_power")

            if not signal:
                return {"status": "error", "message": "Power signal not found."}

            if mode == "projector":
                if self.state == "on":
                    return {"status": "success", "message": "Projector is already on."}

                self.send_signal(signal["code"])
                self.state = "on"
                return {"status": "success", "message": "Projector turned on for projector mode."}

            elif mode in ["desk", "bedtime"]:
                if self.state == "off":
                    return {"status": "success", "message": "Projector is already off."}

                self.send_signal(signal["code"])
                time.sleep(0.25)
                self.send_signal(signal["code"])
                self.state = "off"
                return {"status": "success", "message": "Projector turned off for desk or bedtime mode."}

            else:
                return {"status": "error", "message": f"Invalid mode: {mode}"}

        except Exception as e:
            return {"status": "error", "message": str(e)}
