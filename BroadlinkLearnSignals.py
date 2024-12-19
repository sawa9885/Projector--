import broadlink

def connect_to_broadlink(device_ip, device_mac):
    """
    Connect to the BroadLink device and authenticate.
    :param device_ip: IP address of the BroadLink device.
    :param device_mac: MAC address of the BroadLink device.
    :return: Authenticated BroadLink device object.
    """
    try:
        print("Connecting to BroadLink device...")
        device = broadlink.gendevice(0x520b, (device_ip, 80), bytes.fromhex(device_mac.replace(':', '')))
        device.auth()  # Authenticate with the device
        print("Authentication successful!")
        return device
    except broadlink.exceptions.AuthenticationError:
        print("Error: Authentication failed. Check device IP, MAC, and network settings.")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return None

if __name__ == "__main__":
    # Replace with your device's IP and MAC address
    DEVICE_IP = "192.168.0.108"
    DEVICE_MAC = "e8:16:56:a1:70:db"

    # Attempt to connect and authenticate
    device = connect_to_broadlink(DEVICE_IP, DEVICE_MAC)
    if device:
        print("Device is ready for further commands.")
    else:
        print("Failed to connect to the BroadLink device.")
