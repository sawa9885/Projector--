from pynput import keyboard

class KeyDebugger:
    """Class to display pressed keys."""

    current_keys = set()  # Tracks currently pressed keys

    @classmethod
    def on_press(cls, key):
        """Handler for key press events."""
        cls.current_keys.add(key)
        cls.display_pressed_keys()

    @classmethod
    def on_release(cls, key):
        """Handler for key release events."""
        cls.current_keys.discard(key)
        cls.display_pressed_keys()

    @classmethod
    def display_pressed_keys(cls):
        """Display all currently pressed keys."""
        print(f"Currently pressed keys: {[str(k) for k in cls.current_keys]}")

    @classmethod
    def listen(cls):
        """Start listening for key events."""
        print("Press keys to see which ones are detected. Release them to update.")
        print("Press 'Q' to exit.")
        with keyboard.Listener(on_press=cls.on_press, on_release=cls.on_release) as listener:
            listener.join()

if __name__ == "__main__":
    KeyDebugger.listen()
