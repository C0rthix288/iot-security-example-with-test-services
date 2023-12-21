# server/weather-data-service/models.py
#
from pydantic import BaseModel
from datetime import datetime

class WeatherData(BaseModel):
    temperature: float
    wind_speed: float
    humidity: float
    date: datetime = datetime.now() # Default to current date/time

class DeviceInfo(BaseModel):
    device_id: str
    ip_address: str
    status: str  
    special_device_token_hash: str  # Hash of the special device token
