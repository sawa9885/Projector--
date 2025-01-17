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
        Set the mode for the projector (desk, projector, bedtime).
        :param mode: The desired mode (desk, projector, bedtime).
        :return: Results indicating success or failure.
        """
        if mode == "projector":
            # Turn on the projector (press power button once)
            signal = self.signals.get("projector_power")
            if signal:
                self.send_signal(signal["code"])
                return {"status": "success", "message": "Projector turned on for projector mode."}
            else:
                return {"status": "error", "message": "Power signal not found."}

        elif mode in ["desk", "bedtime"]:
            # Turn off the projector (press power button twice with a delay)
            signal = self.signals.get("projector_power")
            if signal:
                self.send_signal(signal["code"])
                time.sleep(0.25)
                self.send_signal(signal["code"])
                return {"status": "success", "message": "Projector turned off for desk or bedtime mode."}
            else:
                return {"status": "error", "message": "Power signal not found."}

        else:
            # Invalid mode
            return {"status": "error", "message": f"Invalid mode: {mode}"}

if __name__ == "__main__":
    # Path to the signal storage file
    SIGNAL_STORAGE = "signal_storage.json"

    # Replace with your device's IP and MAC address
    DEVICE_IP = "192.168.0.108"
    DEVICE_MAC = "e8:16:56:a1:70:db"

    projector = Projector(SIGNAL_STORAGE, DEVICE_IP, DEVICE_MAC)

    try:
        while True:
            print("\nSelect Mode:")
            print("1. Desk Setup")
            print("2. Projector Setup")
            print("3. Bed Setup")
            choice = input("Enter 1, 2, or 3: ").strip()

            if choice == "1":
                response = projector.set_mode("desk")
            elif choice == "2":
                response = projector.set_mode("projector")
            elif choice == "3":
                response = projector.set_mode("bedtime")
            else:
                response = {"status": "error", "message": "Invalid choice."}

            print(f"Response: {response}")

    except KeyboardInterrupt:
        print("Exiting script.")
