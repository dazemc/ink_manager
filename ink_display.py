import sys
import os
import logging.config
from lib import epd7in3f
import time
import json
from PIL import Image, ImageDraw, ImageFont

IMG_DIR = "assets/images"
FONT_DIR = "assets/fonts"
LIB_DIR = "lib/"
LOGGER = logging.getLogger(__name__)

file_path = os.path.abspath(__file__)
cwd = os.path.dirname(file_path)
config_file = f"{cwd}/logging.json"
with open(config_file) as f:
    config = json.load(f)
logging.config.dictConfig(config)


class InkDisplay:
    def __init__(self) -> None:
        self.ink = epd7in3f.EPD()
        self.draw_image = self.blank_image()

    def init(self) -> None:
        LOGGER.info("initialising")
        if os.path.exists(LIB_DIR):
            sys.path.append(LIB_DIR)
        self.ink.init()

    def clear(self) -> None:
        LOGGER.info("clearing screen")
        self.ink.Clear()

    def sleep(self) -> None:
        LOGGER.info("putting to sleep")
        self.ink.sleep()

    def exit(self) -> None:
        LOGGER.info("ctrl + c:")
        epd7in3f.epdconfig.module_exit()

    def display_image(self, image) -> None:
        LOGGER.info("displaying image")
        Himage = Image.open(os.path.join(IMG_DIR, image))
        self.ink.display(self.ink.getbuffer(Himage))

    def blank_image(self) -> Image:
        LOGGER.info("creating new draw image")
        return Image.new("RGB", (self.ink.width, self.ink.height), self.ink.WHITE)

    def draw(self, image) -> ImageDraw:
        return ImageDraw.Draw(image)

    def draw_text(self, location, text, font, size, color, draw) -> None:
        LOGGER.info("drawing text to draw image: %s", text)
        draw.text(
            (location),
            text=text,
            font=ImageFont.truetype(os.path.join(FONT_DIR, font), size),
            fill=color,
        )

    def display_draw(self, image) -> None:
        LOGGER.info("displaying draw image")
        self.ink.display(self.ink.getbuffer(image))
