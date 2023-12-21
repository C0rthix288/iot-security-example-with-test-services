# client/app/data_generator.py

import random
import time

def generate_sensor_data():
    """
    Generates realistic sensor data for temperature, wind, and humidity.
    Temperature (in Celsius): Simulates day/night and seasonal variation.
    Wind (in km/h): Simulates random gusts and calm periods.
    Humidity (in %): Varies with simulated temperature (higher temp -> lower humidity).
    """
    # Simulating temperature with day/night and seasonal variation
    base_temp = 10  # Average base temperature
    day_temp_variation = random.uniform(-5, 5)  # Day-to-day variation
    seasonal_variation = 15 * (0.5 - random.random())  # Seasonal variation
    temperature = base_temp + day_temp_variation + seasonal_variation

    # Simulating wind speed with random gusts
    wind_speed = random.uniform(0, 20)  # 0 to 20 km/h

    # Simulating humidity inversely related to temperature
    humidity = random.uniform(30, 100) - (temperature - base_temp) * 0.5

    return {
        'temperature': round(temperature, 2),
        'wind_speed': round(wind_speed, 2),
        'humidity': round(humidity, 2)
    }

def main():
    while True:
        data = generate_sensor_data()
        print(f"Generated Data: {data}")
        time.sleep(5)  # Simulate data generation every 5 seconds

if __name__ == "__main__":
    main()
