import ctypes

class VoiceMeeter:
    def __init__(self):
        try:
            self.vm_remote = ctypes.CDLL("C:\\Program Files (x86)\\VB\\Voicemeeter\\VoicemeeterRemote64.dll")
        except FileNotFoundError:
            print("Error: VoicemeeterRemote64.dll not found. Ensure the DLL path is correct.")
            exit(1)

        self.initialize_voicemeeter()
        self.current_mode = None  # Tracks the current mode

    def initialize_voicemeeter(self):
        result = self.vm_remote.VBVMR_Login()
        if result != 0:
            print(f"Error: Unable to login to Voicemeeter Remote API. Error code: {result}")
            exit(1)

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
        except Exception as e:
            print(f"Exception occurred while restarting audio engine: {e}")

    def set_mode(self, mode):
        """
        Sets the audio configuration mode (desk, projector, or bedtime).
        :param mode: The desired mode ("desk", "projector", or "bedtime").
        :return: Status indicating success or failure.
        """
        try:
            if self.current_mode == mode:
                return {
                    "status": "success", 
                    "message": f"VoiceMeeter is already in {mode} mode."
                }

            if mode == "desk":
                self.set_bus_mute(0, 0)  # Unmute desk speakers (Bus A1)
                self.set_bus_mute(1, 0)  # Unmute desk speakers (Bus A2)
                self.set_bus_mute(2, 1)  # Mute projector speakers (Bus A3)
            elif mode == "projector":
                self.set_bus_mute(0, 1)  # Mute desk speakers (Bus A1)
                self.set_bus_mute(1, 1)  # Mute desk speakers (Bus A2)
                self.set_bus_mute(2, 0)  # Unmute projector speakers (Bus A3)
            elif mode == "bedtime":
                self.set_bus_mute(0, 1)  # Mute desk speakers (Bus A1)
                self.set_bus_mute(1, 1)  # Mute desk speakers (Bus A2)
                self.set_bus_mute(2, 1)  # Mute projector speakers (Bus A3)
            else:
                return {"status": "error", "message": f"Invalid mode: {mode}"}

            self.restart_audio_engine()
            self.current_mode = mode
            return {"status": "success", "message": f"Mode set to {mode}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def logout(self):
        self.vm_remote.VBVMR_Logout()