# server/weather-data-service/database.py

import sqlite3
from models import WeatherData, DeviceInfo

def db_connection():
    return sqlite3.connect('weather.db')

def init_db():
    conn = db_connection()
    try:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS weather_data (
                id INTEGER PRIMARY KEY,
                temperature REAL,
                wind_speed REAL,
                humidity REAL,
                date TEXT,
                device_id TEXT
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS device_info (
                device_id TEXT PRIMARY KEY,
                ip_address TEXT,
                status TEXT,
                special_device_token_hash TEXT
            )
        ''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

def save_weather_data(weather_data: WeatherData, device_id: str):
    conn = db_connection()
    try:
        c = conn.cursor()
        c.execute('''
            INSERT INTO weather_data (temperature, wind_speed, humidity, date, device_id) 
            VALUES (?, ?, ?, ?, ?)
        ''', (weather_data.temperature, weather_data.wind_speed, weather_data.humidity, weather_data.date, device_id))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

def get_weather_data() -> WeatherData:
    conn = db_connection()
    try:
        c = conn.cursor()
        c.execute('SELECT * FROM weather_data ORDER BY date DESC LIMIT 1')
        data = c.fetchone()
        if data:
            return WeatherData(temperature=data[0], wind_speed=data[1], humidity=data[2], date=data[3])
        return None
    finally:
        conn.close()

def is_valid_token_hash(device_id: str, token_hash: str) -> bool:
    conn = db_connection()
    try:
        c = conn.cursor()
        c.execute('SELECT special_device_token_hash FROM device_info WHERE device_id = ?', (device_id,))
        result = c.fetchone()
        return result and result[0] == token_hash
    finally:
        conn.close()

def update_device_info(device_info: DeviceInfo):
    conn = db_connection()
    try:
        c = conn.cursor()
        c.execute('''
            UPDATE device_info 
            SET ip_address = ?, status = ?
            WHERE device_id = ?
        ''', (device_info.ip_address, device_info.status, device_info.device_id))

        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

def register_device_token_hash(device_info: DeviceInfo):
    conn = db_connection()
    try:
        c = conn.cursor()
        # Insert or update the device information with the token hash
        c.execute('''
            INSERT INTO device_info (device_id, ip_address, status, special_device_token_hash)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(device_id)
            DO UPDATE SET ip_address = ?, status = ?, special_device_token_hash = ?
        ''', (device_info.device_id, device_info.ip_address, device_info.status, device_info.special_device_token_hash, 
              device_info.ip_address, device_info.status, device_info.special_device_token_hash))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()


init_db()