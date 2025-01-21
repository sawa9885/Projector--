from pynput import keyboard
import threading


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
    on_action = None  # Callback to trigger room mode actions
    listener_thread = None  # Track the listener thread
    stop_event = threading.Event()  # Event to stop the listener thread

    @classmethod
    def _listen(cls):
        """Internal method to handle key listening."""
        def handle_press(key):
            cls.current_keys.add(key.vk if hasattr(key, 'vk') else key)
            # Check for each action key combination
            for mode, keys in cls.ACTION_KEYS.items():
                if keys.issubset(cls.current_keys):
                    if cls.on_action:
                        cls.on_action(mode)  # Trigger the action immediately

        def handle_release(key):
            cls.current_keys.discard(key.vk if hasattr(key, 'vk') else key)

        # Start the listener
        with keyboard.Listener(on_press=handle_press, on_release=handle_release) as listener:
            cls.stop_event.wait()  # Wait until the stop event is set
            listener.stop()

    @classmethod
    def listen(cls):
        """Start listening for key presses in a separate thread."""
        if cls.listener_thread and cls.listener_thread.is_alive():
            print("Listener is already running.")
            return

        cls.stop_event.clear()  # Reset the stop event
        cls.listener_thread = threading.Thread(target=cls._listen, daemon=True)
        cls.listener_thread.start()
        print("Listening for key combinations in a separate thread.")

    @classmethod
    def stop_listening(cls):
        """Stop listening for key presses."""
        if cls.listener_thread and cls.listener_thread.is_alive():
            cls.stop_event.set()  # Signal the listener thread to stop
            cls.listener_thread.join()  # Wait for the thread to finish
            cls.listener_thread = None
            print("Stopped listening for key combinations.")

    @classmethod
    def reset_listening(cls):
        """Stop and restart the listener."""
        cls.stop_listening()
        cls.listen()
        
    from time import sleep

def handle_action(mode):
    """Callback function to handle key actions."""
    print(f"Action triggered: {mode}")
    if mode == "quit":
        MacroButton.stop_listening()
        print("Exiting listener...")

from time import sleep

if __name__ == "__main__":
    from MacroButton import MacroButton

    # Set the callback for key actions
    MacroButton.on_action = handle_action

    # Start the listener
    print("Starting MacroButton listener test. Press the key combinations to test:")
    MacroButton.listen()

    # Simulate a main application loop
    try:
        while MacroButton.listener_thread and MacroButton.listener_thread.is_alive():
            sleep(1)  # Keep the main thread running
    except KeyboardInterrupt:
        MacroButton.stop_listening()
        print("Exiting program via keyboard interrupt.")
