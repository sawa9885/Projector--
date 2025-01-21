from pynput import keyboard
from multiprocessing import Process
from time import sleep
import os

class MacroButton:
    """Class to handle the macro button press."""

    # Define the key combinations
    ACTION_KEYS = {
        "process1": {keyboard.Key.ctrl_l, keyboard.Key.shift, keyboard.Key.alt_l, 49},  # ASCII code for '1'
        "process2": {keyboard.Key.ctrl_l, keyboard.Key.shift, keyboard.Key.alt_l, 50},  # ASCII code for '2'
        "quit": {keyboard.Key.ctrl_l, keyboard.Key.shift, keyboard.Key.alt_l, 81},  # ASCII code for 'Q'
    }

    current_keys = set()  # Tracks currently pressed keys
    active_process = None  # Tracks the currently active process

    @classmethod
    def _listen(cls):
        """Internal method to handle key listening."""
        def handle_press(key):
            cls.current_keys.add(key.vk if hasattr(key, 'vk') else key)
            # Check for each action key combination
            for mode, keys in cls.ACTION_KEYS.items():
                if keys.issubset(cls.current_keys):
                    cls.handle_action(mode)

        def handle_release(key):
            cls.current_keys.discard(key.vk if hasattr(key, 'vk') else key)

        # Start the listener
        with keyboard.Listener(on_press=handle_press, on_release=handle_release) as listener:
            listener.join()

    @classmethod
    def handle_action(cls, mode):
        """Callback function to handle key actions."""
        if mode == "quit":
            print("Exiting listener...")
            if cls.active_process and cls.active_process.is_alive():
                cls.active_process.terminate()
                cls.active_process.join()
            os._exit(0)
        elif mode == "process1":
            cls.start_process("Process 1", 5)
        elif mode == "process2":
            cls.start_process("Process 2", 10)

    @classmethod
    def start_process(cls, name, seconds):
        """Starts a new process if none is running, or waits for the current process to finish."""
        if cls.active_process:
            if cls.active_process.is_alive():
                print(f"A process is already running. Please wait for it to finish.")
                return
            else:
                cls.active_process.join()  # Ensure the previous process has fully terminated

        # Start the new process
        cls.active_process = Process(target=countdown, args=(name, seconds))
        cls.active_process.start()

def countdown(name, seconds):
    """Function to perform a countdown."""
    print(f"{name} starting a countdown of {seconds} seconds.")
    for i in range(seconds, 0, -1):
        print(f"{name}: {i} seconds remaining...")
        sleep(1)
    print(f"{name} countdown complete.")

if __name__ == "__main__":
    print("Starting MacroButton listener test. Press the key combinations to test:")
    MacroButton._listen()
