# wireguard-provisioning-service/main.py

from fastapi import Depends, FastAPI, HTTPException
from models import DeviceRegistration, DeviceResponse
from wireguard import register_client, get_server_public_key, get_server_ip
from database import init_db, delete_token
from wg_token import validate_token, generate_token

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    init_db()

@app.post("/register_device/", response_model=DeviceResponse)
async def register_device(device: DeviceRegistration, token: str = Depends(validate_token)):
    internal_ip = register_client(device.device_id, device.public_key)
    server_public_key = get_server_public_key()
    server_ip = get_server_ip()
    delete_token(token) # Delete the token after it's been used
    return {"device_id": device.device_id, "server_public_key": server_public_key, "server_ip": server_ip, "internal_ip": internal_ip}

@app.get("/generate_token/")
async def get_token():
    return {"token": generate_token()}
