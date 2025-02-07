from WeatherData import WeatherData
from ink_display import InkDisplay
import RPi.GPIO as GPIO
import os

GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN)
busy = GPIO.input(24)
file_path = os.path.abspath(__file__)
cwd = os.path.dirname(file_path)
print(cwd)
if busy == 0:
    wd = WeatherData()
    ink = InkDisplay()
    ink.init()
    wd.get_response()
    wd.create_forecast()
    ink.display_image(cwd + "/assets/images/weather_forecast/forecast.png")
    ink.sleep()
    print(1)
else:
    print(0)
