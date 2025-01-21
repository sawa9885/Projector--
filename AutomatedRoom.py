from pynput import keyboard
from multiprocessing import Process
import os
import sys
from BedPlug import BedPlug
from CeilingLights import CeilingLights
from Screen import Screen
from VoiceMeeter import VoiceMeeter
from DeskLights import DeskLights
from DeskPlug import DeskPlug
from DisplayFusion import DisplayFusion
from Projector import Projector

class MacroButton:
    """Class to handle the macro button press."""

    # Define the key combinations
    ACTION_KEYS = {
        "projector": {keyboard.Key.ctrl_l, keyboard.Key.shift, keyboard.Key.alt_l, 49},  # ASCII code for '1'
        "desk": {keyboard.Key.ctrl_l, keyboard.Key.shift, keyboard.Key.alt_l, 50},  # ASCII code for '2'
        "bedtime": {keyboard.Key.ctrl_l, keyboard.Key.shift, keyboard.Key.alt_l, 51},  # ASCII code for '3'
        "quit": {keyboard.Key.ctrl_l, keyboard.Key.shift, keyboard.Key.alt_l, 81},  # ASCII code for 'Q'
    }

    current_keys = set()  # Tracks currently pressed keys

    @classmethod
    def listen(cls, automated_room):
        """Method to handle key listening and trigger actions."""

        def handle_press(key):
            cls.current_keys.add(key.vk if hasattr(key, 'vk') else key)
            # Check for each action key combination
            for mode, keys in cls.ACTION_KEYS.items():
                if keys.issubset(cls.current_keys):
                    cls.handle_action(mode, automated_room)

        def handle_release(key):
            cls.current_keys.discard(key.vk if hasattr(key, 'vk') else key)

        # Start the listener
        with keyboard.Listener(on_press=handle_press, on_release=handle_release) as listener:
            listener.join()

    @classmethod
    def handle_action(cls, mode, automated_room):
        """Callback function to handle key actions."""
        if mode == "quit":
            print("Exiting system...")
            sys.exit(0)
        else:
            automated_room.set_mode(mode)

class AutomatedRoom:
    def __init__(self):
        # Initialize all devices
        self.bed_plug = BedPlug(
            api_key="5e6a480a-716a-4ad9-bf9c-67413c645028",
            device_id="73:51:D0:C9:07:60:3E:B8",
            model="H5083"
        )
        self.ceiling_lights = CeilingLights(
            api_key="5e6a480a-716a-4ad9-bf9c-67413c645028",
            devices=[
                {"device_id": "48:0E:D0:C9:07:BA:4D:A0", "sku": "H6008"},
                {"device_id": "7E:2C:D0:C9:07:BA:D0:A0", "sku": "H6008"},
            ]
        )
        self.desk_lights = DeskLights(
            api_key="5e6a480a-716a-4ad9-bf9c-67413c645028",
            device_id="D4:CA:D5:0E:C2:06:5C:5C",
            model="H6056"
        )
        self.desk_plug = DeskPlug(
            api_key="5e6a480a-716a-4ad9-bf9c-67413c645028",
            device_id="31:A1:D0:C9:07:61:85:34",
            model="H5083"
        )
        self.voice_meeter = VoiceMeeter()
        self.display_fusion = DisplayFusion()
        self.projector = Projector(
            signal_storage="signal_storage.json",
            device_ip="192.168.0.108",
            device_mac="e8:16:56:a1:70:db"
        )
        self.screen = Screen(
            signal_storage="signal_storage.json",
            device_ip="192.168.0.108",
            device_mac="e8:16:56:a1:70:db"
        )

    def set_mode(self, mode):
        """
        Set the entire room to the given mode.
        :param mode: The desired mode (desk, projector, bedtime).
        """
        print(f"Setting room to {mode} mode...")

        try:
            # Trigger devices based on the mode
            print(self.bed_plug.set_mode(mode).get("message"))
            results = self.ceiling_lights.set_mode(mode)
            for result in results:
                print(result["message"])
            print(self.desk_lights.set_mode(mode).get("message"))
            print(self.desk_plug.set_mode(mode).get("message"))
            print(self.voice_meeter.set_mode(mode).get("message"))
            print(self.display_fusion.set_mode(mode).get("message"))
            print(self.projector.set_mode(mode).get("message"))
            print(self.screen.set_mode(mode).get("message"))

            print(f"Room set to {mode} mode.")
        except Exception as e:
            print(f"Error occurred while setting mode: {e}")

if __name__ == "__main__":
    automated_room = AutomatedRoom()
    print("Starting MacroButton listener with Automated Room system.")
    print("Press the key combinations to switch modes:")
    print("Ctrl + Shift + Alt + 1: Projector Mode")
    print("Ctrl + Shift + Alt + 2: Desk Mode")
    print("Ctrl + Shift + Alt + 3: Bedtime Mode")
    print("Ctrl + Shift + Alt + Q: Quit")

    MacroButton.listen(automated_room)
