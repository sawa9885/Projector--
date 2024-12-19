from pynput import keyboard

class MacroButton:
    """Class to handle the macro button press."""

    # Define the key combinations
    ACTION_KEYS = {
        "desk": {keyboard.Key.ctrl_l, keyboard.Key.shift, keyboard.Key.alt_l, 49},  # ASCII code for '1'
        "bed": {keyboard.Key.ctrl_l, keyboard.Key.shift, keyboard.Key.alt_l, 50},  # ASCII code for '2'
        "projector": {keyboard.Key.ctrl_l, keyboard.Key.shift, keyboard.Key.alt_l, 51},  # ASCII code for '3'
        "quit": {keyboard.Key.ctrl_l, keyboard.Key.shift, keyboard.Key.alt_l, 81},  # ASCII code for 'Q'
    }

    current_keys = set()  # Tracks currently pressed keys

    @classmethod
    def on_action(cls, mode):
        """Action triggered when a key combination is pressed."""
        if mode == "quit":
            print("Exiting script...")
            exit(0)
        print(f"Macro action triggered: {mode} mode")

    @classmethod
    def listen(cls):
        """Start listening for key presses."""
        def handle_press(key):
            # Add key to the set, handling raw key codes and Key objects
            cls.current_keys.add(key.vk if hasattr(key, 'vk') else key)
            # Check for each action key combination
            for mode, keys in cls.ACTION_KEYS.items():
                if keys.issubset(cls.current_keys):
                    cls.on_action(mode)

        def handle_release(key):
            # Remove key from the set, handling raw key codes and Key objects
            cls.current_keys.discard(key.vk if hasattr(key, 'vk') else key)

        print("Listening for key combinations: Ctrl+Shift+Alt+1 (Desk), Ctrl+Shift+Alt+2 (Bed), Ctrl+Shift+Alt+3 (Projector), Ctrl+Shift+Alt+Q (Quit)...")
        with keyboard.Listener(on_press=handle_press, on_release=handle_release) as listener:
            listener.join()

if __name__ == "__main__":
    # Start the macro button listener
    MacroButton.listen()