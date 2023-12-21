# server/weather-data-service/main.py

from fastapi import FastAPI, HTTPException
from models import WeatherData, DeviceInfo
from routes import router as weather_router
from database import update_device_info, register_device_token_hash

app = FastAPI()

@app.post("/register_device_token/")
async def register_device_token(device_info: DeviceInfo):
    try:
        register_device_token_hash(device_info)
        return {"message": "Device token registered successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/update_device_info/")
async def update_device_info_endpoint(device_info: DeviceInfo):
    try:
        update_device_info(device_info)
        return {"message": "Device info updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Include router for weather data endpoints
app.include_router(weather_router)
