from ..forecast_builder.WeatherData import WeatherData
from ....ink_display import InkDisplay
import RPi.GPIO as GPIO
import sys, os

GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN)
busy = GPIO.input(24)

if busy == 1:
    wd = WeatherData()
    ink = InkDisplay()
    wd.get_response()
    wd.create_forecast()
    ink.display_image("../../images/weather_forecast/forecast.png")
    ink.sleep()
    print(0)
else:
    print(1)
