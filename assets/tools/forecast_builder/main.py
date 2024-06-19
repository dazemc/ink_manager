from PIL import Image, ImageDraw
import os
from datetime import datetime

CWD = os.getcwd()
ICON_DIR = CWD + "/assets/images/weather_icons/"
FORECAST_DIR = CWD + "/assets/images/weather_forecast/"
WIDTH = 800
HEIGHT = 480
CENTER_WIDTH = WIDTH / 2
CENTER_HEIGHT = HEIGHT / 2
CENTER = (CENTER_WIDTH, CENTER_HEIGHT)
SPACING = 7
TODAY = datetime.today().strftime('%m-%d-%Y')


def get_icons() -> list:
    return [i for i in os.listdir(ICON_DIR)]
    


def create_forecast(icon):
    pos = SPACING
    forecast_image = Image.new("RGB", (WIDTH, HEIGHT), 0xFFFFFF)
    for i in range(5):
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


create_forecast(get_icons()[0])
