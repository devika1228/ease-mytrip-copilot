# mock_services.py
import random

def get_mock_weather(destination):
    # Return simple mock: clear or rainy
    choices = [
        {"condition": "clear", "temp_c": 25},
        {"condition": "rainy", "temp_c": 18},
        {"condition": "windy", "temp_c": 20}
    ]
    return random.choice(choices)

def get_mock_flight_status():
    choices = [
        {"status": "on-time"},
        {"status": "delayed", "delay_minutes": 75},
        {"status": "cancelled"}
    ]
    return random.choice(choices)
