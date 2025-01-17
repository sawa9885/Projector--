import broadlink
import time
import json
import os


class BroadlinkSignalLearner:
    def __init__(self, device_ip, device_mac, storage_file="signal_storage.json"):
        """
        Initialize the BroadLink signal learner.
        :param device_ip: IP address of the BroadLink device.
        :param device_mac: MAC address of the BroadLink device.
        :param storage_file: File path for storing learned signals.
        """
        self.device_ip = device_ip
        self.device_mac = device_mac
        self.device = None
        self.connected = False
        self.storage_file = storage_file

        # Load or create storage
        if os.path.exists(self.storage_file):
            with open(self.storage_file, "r") as f:
                self.signals = json.load(f)
        else:
            self.signals = {}

    def save_signals(self):
        """
        Save the signals dictionary to the storage file.
        """
        with open(self.storage_file, "w") as f:
            json.dump(self.signals, f, indent=4)
        print(f"Signals saved to {self.storage_file}.")

    def connect(self):
        """
        Connect and authenticate with the BroadLink device.
        """
        try:
            print("Connecting to BroadLink device...")
            self.device = broadlink.gendevice(0x520b, (self.device_ip, 80), bytes.fromhex(self.device_mac.replace(':', '')))
            self.device.auth()  # Authenticate with the device
            self.connected = True
            print("Authentication successful!")
        except broadlink.exceptions.AuthenticationError:
            print("Error: Authentication failed. Check device IP, MAC, and network settings.")
            self.connected = False
        except Exception as e:
            print(f"Unexpected error during connection: {e}")
            self.connected = False

    def learn_ir_signal(self, button_name):
        """
        Learn a single IR signal and store it with the given button name.
        :param button_name: Name of the button (e.g., "projector_power").
        """
        if not self.connected:
            print("Device not connected. Cannot learn signals.")
            return None

        try:
            print("Entering IR learning mode. Send the signal now...")
            self.device.enter_learning()

            while True:
                try:
                    learned_code = self.device.check_data()
                    if learned_code:
                        print(f"IR signal for '{button_name}' learned successfully!")
                        self.signals[button_name] = {
                            "type": "IR",
                            "code": learned_code.hex()
                        }
                        self.save_signals()
                        break
                except broadlink.exceptions.StorageError:
                    # No signal captured yet; keep polling
                    continue
        except Exception as e:
            print(f"Error learning IR signal: {e}")

    def learn_rf_signal(self, button_name, frequency=315.0):
        """
        Learn a single RF signal and store it with the given button name.
        :param button_name: Name of the button (e.g., "screen_up").
        :param frequency: The RF frequency to tune to (default 315 MHz).
        """
        if not self.connected:
            print("Device not connected. Cannot learn signals.")
            return None

        try:
            print(f"Tuning to {frequency} MHz and entering RF learning mode...")
            self.device.find_rf_packet(frequency)
            print("Press the button on your RF remote...")

            while True:
                try:
                    learned_code = self.device.check_data()
                    if learned_code:
                        print(f"RF signal for '{button_name}' learned successfully!")
                        self.signals[button_name] = {
                            "type": "RF",
                            "frequency": frequency,
                            "code": learned_code.hex()
                        }
                        self.save_signals()
                        break
                except broadlink.exceptions.StorageError:
                    # Keep polling for signal
                    continue
        except Exception as e:
            print(f"Error learning RF signal: {e}")

    def list_signals(self):
        """
        List all saved signals with their types and names.
        """
        if not self.signals:
            print("No signals saved.")
        else:
            print("Saved signals:")
            for name, details in self.signals.items():
                print(f"- {name}: Type={details['type']}")

    def get_signal(self, button_name):
        """
        Retrieve the signal data for a specific button name.
        :param button_name: Name of the button.
        :return: Signal data if found, else None.
        """
        return self.signals.get(button_name)


if __name__ == "__main__":
    # Replace with your device's IP and MAC address
    DEVICE_IP = "192.168.0.108"
    DEVICE_MAC = "e8:16:56:a1:70:db"

    learner = BroadlinkSignalLearner(DEVICE_IP, DEVICE_MAC)
    learner.connect()

    if learner.connected:
        print("Device connected successfully.")
        while True:
            action = input("Enter 'IR' to learn IR signal, 'RF' to learn RF signal, 'LIST' to list signals, or 'EXIT' to quit: ").strip().upper()
            if action == "IR":
                button_name = input("Enter a name for this IR button: ").strip()
                learner.learn_ir_signal(button_name)
            elif action == "RF":
                button_name = input("Enter a name for this RF button: ").strip()
                learner.learn_rf_signal(button_name)
            elif action == "LIST":
                learner.list_signals()
            elif action == "EXIT":
                print("Exiting...")
                break
            else:
                print("Invalid action. Please try again.")
    else:
        print("Failed to connect to the BroadLink device. Please check your configuration.")
