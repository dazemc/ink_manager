"""Retrieve weather data from open weather api and produce a forecast image

    Returns:
        None: ./assets/images/weather_forecast/forecast.png
    """
import os
from datetime import datetime, timedelta
import logging.config
import json
import requests
from PIL import Image, ImageDraw, ImageFont

# Test/Debug
DEBUG = True
SUNSET_TEST = False
SUNSET_DELTA = timedelta(hours=15)


CWD = os.getcwd()
ICON_DIR = CWD + "/assets/images/weather_icons/"
FORECAST_DIR = CWD + "/assets/images/weather_forecast/"
WIDTH = 800
HEIGHT = 480
CENTER_WIDTH = WIDTH / 2
CENTER_HEIGHT = HEIGHT / 2
CENTER = (CENTER_WIDTH, CENTER_HEIGHT)
SPACING = 8
FONT_SIZE_HEADER = 18
FONT_SIZE_SUB = 22
FONT_HEADER = ImageFont.truetype(
    CWD + "/assets/fonts/Font.ttc", FONT_SIZE_HEADER)
FONT_SUB = ImageFont.truetype(
    CWD + "/assets/fonts/Helvetica.ttc", FONT_SIZE_SUB)


def setup_logging() -> None:
    config_file = "logging.json"
    with open(config_file) as f:
        config = json.load(f)
    logging.config.dictConfig(config)


if DEBUG:
    LOGGER = logging.getLogger(__name__)
    setup_logging()


class WeatherData:
    def __init__(self) -> None:
        self.zip = "98022"
        self.cc = "US"
        self.state_code = "wa"
        self.city_name = "enumclaw"
        self.api = os.environ["OPEN_WEATHER_API"]
        self.exclude = "hourly, minutely"
        self.unit = "standard"
        self.bg = "light/"
        self.daymode = True
        self.response = {}
        self.icons = {}
        self.sunset = ""
        self.sunrise = ""

    def get_icons(self, icon_dir: str, background: str, daymode: bool) -> dict:
        if daymode is True:
            daytime = "DAY"
        else:
            daytime = "NIGHT"
        return {
            "clear sky": f"{icon_dir}{background}{daytime} clear sky.png",
            # clouds
            "few clouds": f"{icon_dir}{background}{daytime} few clouds.png",
            "scattered clouds": f"{icon_dir}{background}{daytime} few clouds.png",
            "broken clouds": f"{icon_dir}{background}{daytime} scattered clouds.png",
            "overcast clouds": f"{icon_dir}{background}{daytime} scattered clouds.png",
            # atmosphere
            "mist": f"{icon_dir}{background}{daytime} mist.png",
            "smoke": f"{icon_dir}{background}{daytime} mist.png",
            "haze": f"{icon_dir}{background}{daytime} mist.png",
            "sand/dust whirls": f"{icon_dir}{background}{daytime} mist.png",
            "fog": f"{icon_dir}{background}{daytime} mist.png",
            "sand": f"{icon_dir}{background}{daytime} mist.png",
            "dust": f"{icon_dir}{background}{daytime} mist.png",
            "volcanic ash": f"{icon_dir}{background}{daytime} mist.png",
            "squalls": f"{icon_dir}{background}{daytime} mist.png",
            "tornado": f"{icon_dir}{background}Air.png",
            "thunderstorm": f"{icon_dir}{background}{daytime} thunderstorm.png",
            # snow
            # TODO: all snow icons are same so parse instead of assign
            # rain
            "light rain": f"{icon_dir}{background}{daytime} shower rain.png",
            "moderate rain": f"{icon_dir}{background}{daytime} shower rain.png",
            "heavy intensity rain": f"{icon_dir}{background}{daytime} rain.png",
            "very heavy rain": f"{icon_dir}{background}{daytime} rain.png",
            "extreme rain": f"{icon_dir}{background}{daytime} rain.png",
            "freezing rain": f"{icon_dir}{background}{daytime} snow.png",
            "shower rain": f"{icon_dir}{background}{daytime} shower rain.png",
            "heavy intensity shower rain": f"{icon_dir}{background}{daytime} rain.png",
            "ragged shower rain": f"{icon_dir}{background}{daytime} rain.png",
            "rain": f"{icon_dir}{background}{daytime} rain.png",
            # TODO: drizzle
            # TODO: thunderstorm
        }

    def text_size(self, text) -> tuple:
        """Creates a boundary box to determine width and height of text

        Args:
            text (str): input text

        Returns:
            tuple: width, height
        """
        canvas = Image.new("RGB", (400, 100))
        draw = ImageDraw.Draw(canvas)
        draw.text((10, 10), text, font=FONT_HEADER, fill="white")
        bbox = canvas.getbbox()
        return (bbox[2] - bbox[0], bbox[3] - bbox[1])

    def create_forecast(self) -> None:
        # need to break this up
        now = datetime.today()
        if SUNSET_TEST:
            now += SUNSET_DELTA
        pos = SPACING
        forecast_image = Image.new("RGB", (WIDTH, HEIGHT), 0xFFFFFF)
        for i, day in enumerate(self.response[:5]):
            day_name = day["dt"]
            min_temp = str(day["temp"]["min"]) + "\u2109"
            max_temp = str(day["temp"]["max"]) + "\u2109"
            week_day = day["weekday"]
            sunset = day["sunset"]
            sunrise = day["sunrise"]
            is_day = sunrise <= now < sunset
            if DEBUG:
                LOGGER.debug("is_day: %s", is_day)
                LOGGER.debug("sunrise <= %s", sunrise <= now)
                LOGGER.debug("sunset < : %s", now < sunset)
                LOGGER.debug("sunrise: %s", sunrise)
                LOGGER.debug("sunset: %s", sunset)
                LOGGER.debug("now: %s", now)
                LOGGER.debug("mode 1: %s", self.daymode)
            if i == 0:
                # week_day = "Current"
                if not is_day:
                    self.daymode = False
                    max_temp = str(day["temp"]["night"]) + "\u2109"
            else:
                self.daymode = True
            if DEBUG:
                LOGGER.debug("mode 2: %s", self.daymode)
            self.icons = self.get_icons(ICON_DIR, self.bg, self.daymode)
            condition = self.icons[day["weather"][0]["description"]]
            icon_image = Image.open(condition).convert("RGBA")
            w, h = icon_image.size
            # used to set origin as center bottom
            text_w = self.text_size(day_name)[0]
            h_offset = int(CENTER_HEIGHT - h / 2)
            forecast_image.paste(icon_image, (pos, h_offset), mask=icon_image)
            draw = ImageDraw.Draw(forecast_image)
            draw.text(
                (pos + text_w / 2 + SPACING, HEIGHT / 4 + 20),
                day_name,
                font=FONT_HEADER,
                fill="gray",
            )
            draw.text(
                (pos + text_w / 2, HEIGHT / 4 + 40),
                week_day,
                font=FONT_SUB,
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
        url = f"http://api.openweathermap.org/geo/1.0/direct?q={
            self.city_name},{self.state_code},{self.cc}&appid={self.api}"
        resp = requests.get(url, timeout=60)
        return (resp.json()[0]["lat"], resp.json()[0]["lon"])

    def get_weather(self, coord) -> dict:
        lat = coord[0]
        lon = coord[1]
        url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={
            lon}&exclude={self.exclude}&appid={self.api}&units={self.unit}"
        resp = requests.get(url, timeout=60)
        return resp.json()["daily"]

    def parse_response(self, response) -> dict:
        for i in range(8):
            response[i]["weekday"] = datetime.fromtimestamp(
                int(response[i]["dt"])
            ).strftime("%A")
            response[i]["dt"] = datetime.fromtimestamp(int(response[i]["dt"])).strftime(
                "%m/%d"
            )
            response[i]["sunrise"] = datetime.fromtimestamp(
                int(response[i]["sunrise"]))
            response[i]["sunset"] = datetime.fromtimestamp(
                int(response[i]["sunset"]))
            response[i]["moonrise"] = datetime.fromtimestamp(
                int(response[i]["moonrise"])
            )
            response[i]["moonset"] = datetime.fromtimestamp(
                int(response[i]["moonset"]))
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

    def get_response(self) -> None:
        weatherdata = WeatherData()
        coord = weatherdata.get_coord()
        forecast_r = weatherdata.get_weather(coord)
        weatherdata.parse_response(forecast_r)
        self.response = forecast_r


if DEBUG:
    wd = WeatherData()
    wd.get_response()
    # print(json.dumps(wd.response, sort_keys=True, indent=4))
    wd.create_forecast()
