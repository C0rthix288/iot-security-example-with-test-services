# wireguard-provisioning-service/models.py

from pydantic import BaseModel

class DeviceRegistration(BaseModel):
    device_id: str
    public_key: str  # Public key from the Raspberry Pi

class DeviceResponse(BaseModel):
    device_id: str
    server_public_key: str  # Server's public key
    server_ip: str  # Server's IP address
    internal_ip: str  # Internal IP assigned to the Raspberry Pi

