import os
from datetime import datetime
import requests
import json
from PIL import Image, ImageDraw, ImageFont

DEBUG = False

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
FONT_SIZE_HEADER = 28
FONT_SIZE_SUB = 22
FONT_HEADER = ImageFont.truetype(CWD + "/assets/fonts/Font.ttc", FONT_SIZE_HEADER)
FONT_SUB = ImageFont.truetype(CWD + "/assets/fonts/Helvetica.ttc", FONT_SIZE_SUB)


class WeatherData:
    def __init__(self) -> None:
        self.zip = "98022"
        self.cc = "US"
        self.api = os.environ["OPEN_WEATHER_API"]
        self.exclude = "hourly, minutely"
        self.unit = "standard"
        self.icons = {
            "clouds": "cloud.png",
            "partly_cloudy": "partly_cloudy.png",
            "partly_rainy": "partly_rainy.png",
            "rain": "rainy.png",
            "clear": "sun.png",
        }
        self.response = {}

    def get_icons(self) -> list:
        return [i for i in os.listdir(ICON_DIR)]

    def text_size(self, text) -> tuple:
        canvas = Image.new("RGB", (400, 100))
        draw = ImageDraw.Draw(canvas)
        draw.text((10, 10), text, font=FONT_HEADER, fill="white")
        bbox = canvas.getbbox()
        return (bbox[2] - bbox[0], bbox[3] - bbox[1])

    def create_forecast(self):
        # need to break this up
        pos = SPACING
        forecast_image = Image.new("RGB", (WIDTH, HEIGHT), 0xFFFFFF)
        for day in self.response[:5]:
            day_name = day["dt"]
            condition = day["weather"][0]["main"].lower()
            min_temp = str(day["temp"]["min"]) + "\u2109"
            max_temp = str(day["temp"]["max"]) + "\u2109"
            icon_image = Image.open(ICON_DIR + self.icons[condition]).convert("RGBA")
            w, h = icon_image.size
            text_w = self.text_size(day_name)[0]
            h_offset = int(CENTER_HEIGHT - h / 2)
            forecast_image.paste(icon_image, (pos, h_offset), mask=icon_image)
            draw = ImageDraw.Draw(forecast_image)
            draw.text(
                (pos + text_w / 2 + SPACING, HEIGHT / 4),
                day_name,
                font=FONT_HEADER,
                fill="black",
            )
            draw.text(
                (pos + text_w / 2 - SPACING, CENTER_HEIGHT + h / 2 + SPACING),
                max_temp,
                font=FONT_SUB,
                fill="black",
            )
            draw.text(
                (pos + text_w / 2 + SPACING * 6, CENTER_HEIGHT + h / 2 + SPACING),
                min_temp,
                font=FONT_SUB,
                fill="gray",
            )
            pos += SPACING + w
            forecast_image.convert("RGB")
            save_dir = FORECAST_DIR + "forecast.png"
            if os.path.exists(save_dir):
                os.remove(save_dir)
            forecast_image.save(save_dir)

    def get_coord(self) -> tuple:
        url = f"http://api.openweathermap.org/geo/1.0/zip?zip={self.zip},{self.cc}&appid={self.api}"
        resp = requests.get(url, timeout=60)
        return (resp.json()["lat"], resp.json()["lon"])

    def get_weather(self, coord):
        lat = coord[0]
        lon = coord[1]
        url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={self.exclude}&appid={self.api}&units={self.unit}"
        resp = requests.get(url, timeout=60)
        return resp.json()["daily"]

    def parse_response(self, response) -> dict:
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

    def get_response(self):
        weatherdata = WeatherData()
        coord = weatherdata.get_coord()
        forecast_r = weatherdata.get_weather(coord)
        weatherdata.parse_response(forecast_r)
        self.response = forecast_r


if DEBUG:
    wd = WeatherData()
    wd.get_response()
    print(json.dumps(wd.response[0], sort_keys=True, indent=4))
    wd.create_forecast()
