from pynput import keyboard

class MacroButton:
    """Class to handle the macro button press."""

    # Define the key combinations
    ACTION_KEYS = {
        keyboard.Key.ctrl_l,
        keyboard.Key.shift,
        keyboard.Key.alt_l,
        49  # ASCII code for '1'
    }
    EXIT_KEYS = {
        keyboard.Key.ctrl_l,
        keyboard.Key.shift,
        keyboard.Key.alt_l,
        81  # ASCII code for 'Q'
    }
    current_keys = set()  # Tracks currently pressed keys

    @classmethod
    def on_action(cls):
        """Action triggered when the action key combination is pressed."""
        print("Macro action triggered: Ctrl + Shift + Alt + 1")

    @classmethod
    def exit_script(cls):
        """Action triggered to exit the script."""
        print("Exiting script...")
        exit(0)

    @classmethod
    def listen(cls):
        """Start listening for key presses."""
        def handle_press(key):
            # Add key to the set, handling raw key codes and Key objects
            cls.current_keys.add(key.vk if hasattr(key, 'vk') else key)
            # Check for the action keys
            if cls.ACTION_KEYS.issubset(cls.current_keys):
                cls.on_action()
            # Check for the exit keys
            if cls.EXIT_KEYS.issubset(cls.current_keys):
                cls.exit_script()

        def handle_release(key):
            # Remove key from the set, handling raw key codes and Key objects
            cls.current_keys.discard(key.vk if hasattr(key, 'vk') else key)

        print("Listening for Ctrl + Shift + Alt + 1 (action) and Ctrl + Shift + Alt + Q (exit)...")
        with keyboard.Listener(on_press=handle_press, on_release=handle_release) as listener:
            listener.join()

if __name__ == "__main__":
    # Start the macro button listener
    MacroButton.listen()
