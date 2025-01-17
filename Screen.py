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
        self.connect_device()

    def connect_device(self):
        """
        Connect and authenticate with the BroadLink device.
        """
        try:
            print("Connecting to BroadLink device...")
            self.device = broadlink.gendevice(0x520b, (self.device_ip, 80), bytes.fromhex(self.device_mac.replace(':', '')))
            self.device.auth()  # Authenticate with the device
            self.connected = True
            print("Authentication successful!")
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
            print(f"Signal sent: {signal_code}")
        except Exception as e:
            print(f"Error sending signal: {e}")

    def set_mode(self, mode):
        """
        Set the mode for the screen (desk, projector, bedtime).
        :param mode: The desired mode (desk, projector, bedtime).
        :return: Results indicating success or failure.
        """
        if mode == "projector":
            # Lower the screen
            signal_down = self.signals.get("screen_down")
            signal_stop = self.signals.get("screen_stop")
            if signal_down and signal_stop:
                self._lower_screen(signal_down["code"], signal_stop["code"])
                return {"status": "success", "message": "Screen lowering for projector mode."}
            else:
                return {"status": "error", "message": "Down or Stop signal not found."}

        elif mode in ["desk", "bedtime"]:
            # Raise the screen
            signal_up = self.signals.get("screen_up")
            if signal_up:
                self.send_signal(signal_up["code"])
                return {"status": "success", "message": "Screen raised for desk or bedtime mode."}
            else:
                return {"status": "error", "message": "Up signal not found."}

        else:
            # Invalid mode
            return {"status": "error", "message": f"Invalid mode: {mode}"}

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
            print("Screen lowering process complete.")
        except Exception as e:
            print(f"Error during screen lowering process: {e}")

if __name__ == "__main__":
    # Path to the signal storage file
    SIGNAL_STORAGE = "signal_storage.json"

    # Replace with your device's IP and MAC address
    DEVICE_IP = "192.168.0.108"
    DEVICE_MAC = "e8:16:56:a1:70:db"

    screen = Screen(SIGNAL_STORAGE, DEVICE_IP, DEVICE_MAC)

    try:
        while True:
            print("\nSelect Mode:")
            print("1. Desk Setup")
            print("2. Projector Setup")
            print("3. Bed Setup")
            choice = input("Enter 1, 2, or 3: ").strip()

            if choice == "1":
                response = screen.set_mode("desk")
            elif choice == "2":
                response = screen.set_mode("projector")
            elif choice == "3":
                response = screen.set_mode("bedtime")
            else:
                response = {"status": "error", "message": "Invalid choice."}

            print(f"Response: {response}")

    except KeyboardInterrupt:
        print("Exiting script.")
