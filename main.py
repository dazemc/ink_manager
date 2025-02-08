import time
import os
import subprocess
import json
import ink_display as ink
import logging.config
from PIL import Image
from WeatherData import WeatherData
from fastapi import FastAPI

app = FastAPI()
logging.basicConfig(level=logging.DEBUG)
ink = ink.InkDisplay()
cwd = os.getcwd()
image = r"/assets/images/test/raspilogo.bmp"
font = "Font.ttc"
wd = WeatherData()

DEBUG = True


def setup_logging() -> None:
    config_file = "logging.json"
    with open(config_file) as f:
        config = json.load(f)
    logging.config.dictConfig(config)


if DEBUG:
    LOGGER = logging.getLogger(__name__)
    setup_logging()
    LOGGER.info("Logger started")


# @app.route("/favicon.ico")
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, "static"), "favicon.ico")


@app.get("/")
def home():
    return "Nothing here yet"


@app.get("/test")
def test() -> str:
    try:
        # INIT/CLEAR
        clean(sleep=False)

        # DISPLAY IMAGE
        ink.display_image(image)
        time.sleep(5)
        ink.clear()

        # CREATE DRAW
        ink.draw_image = ink.blank_image()
        draw = ink.draw(ink.draw_image)
        ink.draw_text(
            (5, 0), text="hello", font=font, size=24, color="#FF0000", draw=draw
        )
        ink.draw_text(
            (5, 30), text="world", font=font, size=16, color="#FF0000", draw=draw
        )
        LOGGER.info("drawing draw image")
        draw.line([(5, 170), (80, 245)], fill="#0000FF")
        ink.display_draw(ink.draw_image)
        time.sleep(5)
        ink.clear()

        # CREATE NEW DRAW
        ink.draw_image = ink.blank_image()
        draw = ink.draw(ink.draw_image)
        ink.draw_text(
            (5, 0),
            text="goodbye world",
            font=font,
            size=36,
            color="#00FF00",
            draw=draw,
        )
        ink.display_draw(ink.draw_image)
        time.sleep(5)
        ink.clear()

        # SLEEP
        reset()
        clean(sleep=True)

    except IOError as e:
        LOGGER.exception(e)
    return "Success"


@app.get("/text")
def display_text() -> str:
    """Creates text on an image

    Returns:
        str: "Success"
    """
    try:
        text = str(request.args["text"])
        color = "#" + str(request.args["color"])
        pos = tuple([int(i) for i in str(request.args["pos"]).split(",")])
        size = int(request.args["size"])
        center = str(request.args["center"]).lower()
        if center != "false":
            px = size / 72 * 96
            px_total = len(text) * px
            pos = (pos[0] - px_total / 4, pos[1] - px / 2.66)
        if DEBUG:
            LOGGER.info("Displaying text: %s", text)
            LOGGER.info("Displaying color: %s", color)
            LOGGER.info("Displaying position: %s", pos)
            LOGGER.info("Displaying size: %s", size)
            LOGGER.info("Displaying center: %s", center)
        # draw_image = ink.blank_image()
        draw = ink.draw(ink.draw_image)
        ink.draw_text(pos, text=text, font=font, size=size, color=color, draw=draw)
        # ink.display_draw(ink.draw_image)
    except IOError as e:
        return LOGGER.info(e)
    return "Success"


@app.get("/display")
def display() -> str:
    ink.init()
    ink.display_draw(ink.draw_image)
    ink.sleep()
    return "Success"


@app.get("/reset")
def reset() -> str:
    ink.draw_image = ink.blank_image()
    return "Success"


@app.get("/ip")
def get_ip() -> str:
    ip = subprocess.check_output(
        [
            "sh",
            "get_ip.sh",
        ]
    ).decode("utf-8")
    clean(False)
    draw = ink.draw(ink.draw_image)
    ink.draw_text((200, 240), text=ip, font=font, size=64, color="#000000", draw=draw)
    ink.display_draw(ink.draw_image)
    ink.sleep()
    return ip


# @app.get("/upload_image", methods=["GET", "POST"])
# def display_upload_image() -> str:
#     clean(False)
#     if request.method == "GET":
#         if DEBUG:
#             LOGGER.info("Displaying image: %s", image)
#     if request.method == "POST":
#         r = request.files["image"]
#         image_name = r.filename
#         post_image = Image.open(r)
#         save_loc = f"{cwd}/assets/images/upload/{image_name}"
#         if os.path.exists(save_loc):
#             os.remove(save_loc)
#         post_image.save(save_loc)
#         image = save_loc
#         if DEBUG:
#             LOGGER.info("Displaying image from POST: %s", image_name)
#     ink.display_image(image)
#     ink.sleep()
#
#     return "Success"


@app.get("/update_weather")
def update_weather():
    clean(False)
    wd.get_response()
    wd.create_forecast()
    ink.display_image(cwd + "/assets/images/weather_forecast/forecast.png")
    ink.sleep()
    return "Success"


@app.get("/clear")
def clean(sleep: bool = True) -> str:
    ink.init()
    reset()
    ink.clear()
    if sleep:
        ink.sleep()
    return "Success"
