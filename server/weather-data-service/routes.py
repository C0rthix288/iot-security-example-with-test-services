# server/weather-data-service/routes.py

from fastapi import APIRouter, HTTPException, Depends
from models import WeatherData, DeviceInfo
from database import get_weather_data, save_weather_data, is_valid_token_hash

router = APIRouter()

@router.post("/data/")
async def submit_data(weather_data: WeatherData, device_info: DeviceInfo):
    if not is_valid_token_hash(device_info.device_id, device_info.special_device_token_hash):
        raise HTTPException(status_code=401, detail="Invalid token")

    save_weather_data(weather_data, device_info.device_id)

@router.get("/data/")
async def get_data():
    """
    Endpoint to retrieve the latest weather data.
    """
    data = get_weather_data()
    if data is None:
        raise HTTPException(status_code=404, detail="No data available")
    return data