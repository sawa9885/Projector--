import subprocess

class DisplayFusion:
    def __init__(self):
        self.current_mode = None  # Tracks the current mode

    def _switch_displayfusion_profile(self, profile_name):
        try:
            subprocess.run([
                "C:\\Program Files\\DisplayFusion\\DisplayFusionCommand.exe", 
                "-monitorloadprofile", 
                profile_name
            ], check=True)
            return {"status": "success", "message": f"Switched to profile: {profile_name}"}
        except FileNotFoundError:
            return {"status": "error", "message": "DisplayFusionCommand.exe not found. Ensure DisplayFusion is installed and the path is correct."}
        except subprocess.CalledProcessError as e:
            return {"status": "error", "message": f"Error switching to profile: {profile_name}. Details: {e}"}

    def set_mode(self, mode):
        """
        Sets the display configuration mode (desk, projector, or bed).
        :param mode: The desired mode ("desk", "projector", or "bed").
        :return: Status indicating success or failure.
        """
        if self.current_mode == mode:
            return {
                "status": "success", 
                "message": f"DisplayFusion is already in {mode} mode."
            }

        if mode == "desk":
            result = self._switch_displayfusion_profile("DeskSetup")
        elif mode == "projector":
            result = self._switch_displayfusion_profile("ProjectorSetup")
        elif mode == "bed":
            result = self._switch_displayfusion_profile("BedSetup")
        else:
            return {"status": "error", "message": f"Invalid mode: {mode}"}

        if result["status"] == "success":
            self.current_mode = mode

        return result
