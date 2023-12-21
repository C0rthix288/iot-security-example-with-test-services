# wireguard-provisioning-service/wireguard.py

import subprocess
import socket
from database import create_device_record, get_next_internal_ip

def get_server_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()

def get_server_public_key():
    try:
        with open("publickey", "r") as file:
            return file.read().strip()
    except Exception as e:
        print(f"Error reading server public key: {e}")
        return None


def register_client(device_id, client_public_key):
    internal_ip = get_next_internal_ip()
    create_device_record(device_id, client_public_key, internal_ip)
    update_server_config(client_public_key, internal_ip)
    return internal_ip

def update_server_config(client_public_key, client_internal_ip):
    with open("/etc/wireguard/wg0.conf", "a") as config_file:
        config_file.write(f"\n[Peer]\nPublicKey = {client_public_key}\nAllowedIPs = {client_internal_ip}/32\n")
