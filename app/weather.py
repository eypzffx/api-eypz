# app/weather.py
from flask import Blueprint
from info.weather import get_weather

weather_bp = Blueprint('weather', __name__)

@weather_bp.route('/info/weather', methods=['GET'])
def info_weather():
    return get_weather()
