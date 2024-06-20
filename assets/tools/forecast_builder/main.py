import os
from datetime import datetime
import requests
from PIL import Image

CWD = os.getcwd()
ICON_DIR = CWD + "/assets/images/weather_icons/"
FORECAST_DIR = CWD + "/assets/images/weather_forecast/"
WIDTH = 800
HEIGHT = 480
CENTER_WIDTH = WIDTH / 2
CENTER_HEIGHT = HEIGHT / 2
CENTER = (CENTER_WIDTH, CENTER_HEIGHT)
SPACING = 8
TODAY = datetime.today().strftime("%m-%d-%Y")
ZIP = "98022"
CC = "US"
API = os.environ["OPEN_WEATHER_API"]
EXCLUDE = "hourly, minutely"
UNIT = "standard"


def get_icons() -> list:
    return [i for i in os.listdir(ICON_DIR)]


def create_forecast(icon):
    pos = SPACING
    forecast_image = Image.new("RGB", (WIDTH, HEIGHT), 0xFFFFFF)
    for _ in range(5):
        icon_image = Image.open(ICON_DIR + icon).convert("RGBA")
        w, h = icon_image.size
        h_offset = int(CENTER_HEIGHT - h / 2)
        forecast_image.paste(icon_image, (pos, h_offset), mask=icon_image)
        pos += SPACING + w
        forecast_image.convert("RGB")
        save_dir = FORECAST_DIR + f"forecast_{TODAY}.png"
        if os.path.exists(save_dir):
            os.remove(save_dir)
        forecast_image.save(save_dir)


def get_coord() -> tuple:
    url = f"http://api.openweathermap.org/geo/1.0/zip?zip={ZIP},{CC}&appid={API}"
    resp = requests.get(url, timeout=60)
    return (resp.json()["lat"], resp.json()["lon"])


def get_weather(coord):
    lat = coord[0]
    lon = coord[1]
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={EXCLUDE}&appid={API}&units={UNIT}"
    resp = requests.get(url, timeout=60)
    return resp.json()["daily"]


def parse_response(response):
    for i in range(8):
        response[i]["dt"] = datetime.fromtimestamp(int(response[i]["dt"])).strftime(
            "%m/%d"
        )
        response[i]["sunrise"] = datetime.fromtimestamp(
            int(response[i]["sunrise"])
        ).strftime("%H:%M")
        response[i]["sunset"] = datetime.fromtimestamp(
            int(response[i]["sunset"])
        ).strftime("%H:%M")
        response[i]["moonrise"] = datetime.fromtimestamp(
            int(response[i]["moonrise"])
        ).strftime("%H:%M")
        response[i]["moonset"] = datetime.fromtimestamp(
            int(response[i]["moonset"])
        ).strftime("%H:%M")
        response[i]["dew_point"] = int(
            (float(response[i]["dew_point"]) - 273.15) * 1.8 + 32
        )

        for key in response[i]["temp"]:
            response[i]["temp"][key] = int(
                (float(response[i]["temp"][key]) - 273.15) * 1.8 + 32
            )

        for key in response[i]["feels_like"]:
            response[i]["feels_like"][key] = int(
                (float(response[i]["feels_like"][key]) - 273.15) * 1.8 + 32
            )
        # print(response[i]["weather"][0]["main"])
        # print(response[i]["dt"])


r = get_weather(get_coord())
parse_response(r)
# print(r)

# create_forecast(get_icons()[0])
