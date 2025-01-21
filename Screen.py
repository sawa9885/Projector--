import time
import broadlink
import json

class Screen:
    def __init__(self, signal_storage, device_ip, device_mac):
        """
        Initialize the Screen controller.
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
        self.state = "off"  # Track the current state ('up' or 'down')
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
        Set the mode for the screen (desk, projector, bedtime).
        :param mode: The desired mode (desk, projector, bedtime).
        :return: Results indicating success or failure.
        """
        try:
            if mode == "projector":
                if self.state == "down":
                    return {"status": "success", "message": "Screen is already down."}

                signal_down = self.signals.get("screen_down")
                signal_stop = self.signals.get("screen_stop")
                if signal_down and signal_stop:
                    self._lower_screen(signal_down["code"], signal_stop["code"])
                    self.state = "down"
                    return {"status": "success", "message": "Screen lowered for projector mode."}
                else:
                    return {"status": "error", "message": "Down or Stop signal not found."}

            elif mode in ["desk", "bedtime"]:
                if self.state == "up":
                    return {"status": "success", "message": "Screen is already up."}

                signal_up = self.signals.get("screen_up")
                if signal_up:
                    self.send_signal(signal_up["code"])
                    self.state = "up"
                    return {"status": "success", "message": "Screen raised for desk or bedtime mode."}
                else:
                    return {"status": "error", "message": "Up signal not found."}

            else:
                return {"status": "error", "message": f"Invalid mode: {mode}"}

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _lower_screen(self, down_signal, stop_signal):
        """
        Lower the screen by sending the down signal followed by the stop signal after a delay.
        :param down_signal: Signal to lower the screen.
        :param stop_signal: Signal to stop the screen.
        """
        try:
            self.send_signal(down_signal)
            time.sleep(31)  # Adjust the delay as needed
            self.send_signal(stop_signal)
        except Exception as e:
            print(f"Error during screen lowering process: {e}")
