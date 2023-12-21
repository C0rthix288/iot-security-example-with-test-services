# client/app/utils.py

def get_device_id_and_token():
    """
    Reads the device ID and special device token from the credentials file.
    Returns a tuple (device_id, special_device_token).
    """
    try:
        with open('/opt/gProVision/secrets/device_credentials', 'r') as file:
            lines = file.readlines()
            device_id = lines[0].strip().split('=')[1]
            special_device_token = lines[1].strip().split('=')[1]
            return device_id, special_device_token
    except Exception as e:
        print(f"Error reading device credentials: {str(e)}")
        return None, None

def get_server_url():
    """
    Reads the server URL from the credentials file.
    Returns the server URL.
    """
    try:
        with open('/opt/gProVision/secrets/server_url', 'r') as file:
            return file.read().strip()
    except Exception as e:
        print(f"Error reading server URL: {str(e)}")
        return None