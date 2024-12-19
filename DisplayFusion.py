import subprocess

class DisplayFusion:
    def __init__(self):
        self.current_mode = "desk"  # Tracks the current mode, defaults to desk

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

# Example usage
if __name__ == "__main__":
    displayfusion = DisplayFusion()
    try:
        while True:
            print("\nSelect Mode:")
            print("1. Desk Setup")
            print("2. Projector Setup")
            print("3. Bed Setup")
            choice = input("Enter 1, 2, or 3: ").strip()

            if choice == "1":
                response = displayfusion.set_mode("desk")
            elif choice == "2":
                response = displayfusion.set_mode("projector")
            elif choice == "3":
                response = displayfusion.set_mode("bed")
            else:
                response = {"status": "error", "message": "Invalid choice."}

            print(f"Response: {response}")

    except KeyboardInterrupt:
        print("Exiting script.")
