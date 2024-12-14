import ctypes

class VoiceMeeter:
    def __init__(self):
        try:
            self.vm_remote = ctypes.CDLL("C:\\Program Files (x86)\\VB\\Voicemeeter\\VoicemeeterRemote64.dll")
        except FileNotFoundError:
            print("Error: VoicemeeterRemote64.dll not found. Ensure the DLL path is correct.")
            exit(1)

        self.initialize_voicemeeter()
        self.current_setup = "desk"  # Tracks the current setup, defaults to desk

    def initialize_voicemeeter(self):
        result = self.vm_remote.VBVMR_Login()
        if result != 0:
            print(f"Error: Unable to login to Voicemeeter Remote API. Error code: {result}")
            exit(1)
        else:
            print("Successfully logged into VoiceMeeter Remote API.")

    def set_bus_mute(self, bus_index, mute_state):
        """
        Mutes or unmutes a given bus.
        :param bus_index: Index of the bus (e.g., 0 for A1, 1 for A2, 2 for A3).
        :param mute_state: 1 to mute, 0 to unmute.
        """
        try:
            param_name = f"Bus[{bus_index}].mute".encode("utf-8")  # Encode the parameter name
            mute_value = ctypes.c_float(mute_state)
            result = self.vm_remote.VBVMR_SetParameterFloat(ctypes.c_char_p(param_name), mute_value)
            if result != 0:
                print(f"Error: Failed to set parameter {param_name.decode()} with error code {result}")
            else:
                print(f"Successfully set {param_name.decode()} to {mute_state}")
        except Exception as e:
            print(f"Exception occurred while setting mute state for Bus[{bus_index}]: {e}")

    def restart_audio_engine(self):
        """
        Restarts the audio engine in VoiceMeeter.
        """
        try:
            result = self.vm_remote.VBVMR_SetParameterFloat(b"Command.Restart", ctypes.c_float(1.0))
            if result != 0:
                print(f"Error: Failed to restart audio engine. Error code: {result}")
            else:
                print("Audio engine restarted successfully.")
        except Exception as e:
            print(f"Exception occurred while restarting audio engine: {e}")

    def activate_desk_setup(self):
        print("Activating Desk Setup")
        self.set_bus_mute(0, 0)  # Unmute desk speakers (Bus A1)
        self.set_bus_mute(1, 0)  # Unmute desk speakers (Bus A2)
        self.set_bus_mute(2, 1)  # Mute projector speakers (Bus A3)
        self.restart_audio_engine()  # Restart audio engine
        self.current_setup = "desk"

    def activate_projector_setup(self):
        print("Activating Projector Setup")
        self.set_bus_mute(0, 1)  # Mute desk speakers (Bus A1)
        self.set_bus_mute(1, 1)  # Mute desk speakers (Bus A2)
        self.set_bus_mute(2, 0)  # Unmute projector speakers (Bus A3)
        self.restart_audio_engine()  # Restart audio engine
        self.current_setup = "projector"

    def toggle_setup(self):
        """
        Toggles between Desk and Projector setups.
        """
        if self.current_setup == "desk":
            self.activate_projector_setup()
        else:
            self.activate_desk_setup()

    def logout(self):
        self.vm_remote.VBVMR_Logout()
        print("Logged out of VoiceMeeter Remote API.")

# Example usage
if __name__ == "__main__":
    voicemeeter = VoiceMeeter()
    try:
        while True:
            print("Select Setup:")
            print("1. Desk Setup")
            print("2. Projector Setup")
            print("3. Toggle Setup")
            choice = input("Enter 1, 2, or 3: ").strip()

            if choice == "1":
                voicemeeter.activate_desk_setup()
            elif choice == "2":
                voicemeeter.activate_projector_setup()
            elif choice == "3":
                voicemeeter.toggle_setup()
            else:
                print("Invalid choice.")

    except KeyboardInterrupt:
        print("Exiting script.")
    finally:
        voicemeeter.logout()