import broadlink

def discover_devices():
    """
    Discover all BroadLink devices on the network.
    :return: A list of discovered devices.
    """
    try:
        print("Discovering BroadLink devices on the network...")
        devices = broadlink.discover(timeout=5)
        if devices:
            for i, device in enumerate(devices):
                print(f"Device {i + 1}:\n  IP Address: {device.host[0]}\n  MAC Address: {':'.join(format(x, '02x') for x in device.mac)}\n  Device Type: {hex(device.devtype)}")
        else:
            print("No devices found.")
        return devices
    except Exception as e:
        print(f"Error discovering devices: {e}")
        return []

def discover_subdevices(device):
    """
    Discover subdevices for a given BroadLink device.
    :param device: A BroadLink device object.
    :return: A list of subdevices.
    """
    try:
        print(f"Discovering subdevices for device at {device.host[0]}...")
        device.auth()
        subdevices = device.get_subdevices()
        if subdevices:
            for sub in subdevices:
                print(f"  Subdevice ID: {sub['did']}, Type: {sub['type']}")
        else:
            print("  No subdevices found.")
        return subdevices
    except Exception as e:
        print(f"Error discovering subdevices: {e}")
        return []

def control_device(device, subdevice_id=None, state=None):
    """
    Control a BroadLink device or its subdevice.
    :param device: A BroadLink device object.
    :param subdevice_id: ID of the subdevice (optional).
    :param state: Desired state (1 to turn on, 0 to turn off).
    """
    try:
        if subdevice_id:
            print(f"Setting state for subdevice {subdevice_id} to {state}...")
            result = device.set_state(did=subdevice_id, pwr=state)
        else:
            print(f"Setting state for device at {device.host[0]} to {state}...")
            result = device.set_state(pwr=state)
        print(f"Response: {result}")
    except Exception as e:
        print(f"Error controlling device: {e}")

if __name__ == "__main__":
    # Discover all devices on the network
    devices = discover_devices()

    if not devices:
        exit("No devices found.")

    # Discover subdevices and control devices
    for device in devices:
        try:
            print(f"\nDevice: {device.host[0]}")
            subdevices = discover_subdevices(device)

            # Example control logic
            if subdevices:
                for subdevice in subdevices:
                    subdevice_id = subdevice['did']
                    control_device(device, subdevice_id=subdevice_id, state=1)  # Turn on subdevice
                    control_device(device, subdevice_id=subdevice_id, state=0)  # Turn off subdevice
            else:
                control_device(device, state=1)  # Turn on main device
                control_device(device, state=0)  # Turn off main device
        except Exception as e:
            print(f"Error with device {device.host[0]}: {e}")
