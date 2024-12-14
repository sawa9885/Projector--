import subprocess

class DisplayFusion:
    def __init__(self):
        self.current_setup = "desk"  # Tracks the current setup, defaults to desk

    def switch_displayfusion_profile(self, profile_name):
        try:
            subprocess.run(["C:\Program Files\DisplayFusion\DisplayFusionCommand.exe", "-monitorloadprofile", profile_name], check=True)
            print(f"Switched to profile: {profile_name}")
        except FileNotFoundError:
            print("Error: DisplayFusionCommand.exe not found. Ensure DisplayFusion is installed and the path is correct.")
        except subprocess.CalledProcessError as e:
            print(f"Error switching to profile: {profile_name}. Details: {e}")

    def activate_desk_setup(self):
        print("Activating Desk Setup")
        self.switch_displayfusion_profile("DeskSetup")
        self.current_setup = "desk"

    def activate_projector_setup(self):
        print("Activating Projector Setup")
        self.switch_displayfusion_profile("ProjectorSetup")
        self.current_setup = "projector"

    def toggle_setup(self):
        """
        Toggles between Desk and Projector setups.
        """
        if self.current_setup == "desk":
            self.activate_projector_setup()
        else:
            self.activate_desk_setup()

# Example usage
if __name__ == "__main__":
    displayfusion = DisplayFusion()
    try:
        while True:
            print("Select Setup:")
            print("1. Desk Setup")
            print("2. Projector Setup")
            print("3. Toggle Setup")
            choice = input("Enter 1, 2, or 3: ").strip()

            if choice == "1":
                displayfusion.activate_desk_setup()
            elif choice == "2":
                displayfusion.activate_projector_setup()
            elif choice == "3":
                displayfusion.toggle_setup()
            else:
                print("Invalid choice.")

    except KeyboardInterrupt:
        print("Exiting script.")
