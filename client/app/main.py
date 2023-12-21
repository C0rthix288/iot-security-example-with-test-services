# client/app/main.py
import requests
import hashlib
from data_generator import generate_sensor_data
from utils import get_server_url, get_device_id_and_token
import socket
from datetime import datetime
import time

def hash_token(token):
    """
    Hashes the special device token using SHA-256.
    """
    return hashlib.sha256(token.encode()).hexdigest()

def get_ip_address():
    """ Get the local IP address of the Raspberry Pi """
    try:
        # Create a dummy socket to connect to an external server
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # Use Google's public DNS server to find out our IP
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception as e:
        print(f"Error obtaining IP address: {str(e)}")
        return "Unknown"

def send_data_to_server(data):
    device_id, special_device_token = get_device_id_and_token()
    special_device_token_hash = hash_token(special_device_token)
    url = get_server_url() + ":8443/data/"
    ip_address = get_ip_address()  # Dynamically get the Raspberry Pi's IP address
    status = "online"  # Assuming the device is online when sending data
    current_datetime = datetime.now().isoformat()
    
    data_with_device_info = {
        "weather_data": {
            **data, 
            "date": current_datetime
        },
        "device_info": {
            "device_id": device_id,
            "ip_address": ip_address,
            "status": status,
            "special_device_token_hash": special_device_token_hash
        }
    }

    try:
        response = requests.post(url, json=data_with_device_info)
        print("Data sent: ", response.json())
    except Exception as e:
        print("Error sending data: ", str(e))

def main():
    while True:
        data = generate_sensor_data()
        send_data_to_server(data)
        print(data)
        time.sleep(10)

if __name__ == "__main__":
    main()
