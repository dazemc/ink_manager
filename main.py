import time
import os
import subprocess
import json
from lib import ink_display as ink
import logging.config
import shutil
import requests
import utils
import qrcode
from PIL import Image
from WeatherData import WeatherData
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from models import Text, TextBoundary, TextBoundaryLine, Coord

app = FastAPI()
logging.basicConfig(level=logging.DEBUG)
ink = ink.InkDisplay()
cwd = os.getcwd()
image = "assets/images/test/raspilogo.bmp"
font = "Inktype.ttf"
upload_dir = "./assets/images/uploads"
os.makedirs(upload_dir, exist_ok=True)
wd = WeatherData()

DEBUG = True


def setup_logging() -> None:
    config_file = "./lib/logging.json"
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
        # ink.display_image(image)
        # time.sleep(5)
        # ink.clear()

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


@app.post("/text")
async def display_text(contents: Text) -> str:
    """Creates text on an image to render, uses hex color values.

    Returns:
        str: "Success"
    """
    try:
        text = contents.text
        color = "#" + contents.color
        pos = tuple([int(i) for i in contents.pos.split(",")])
        size = contents.size
        center = bool(contents.center)
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


@app.post("/upload_image")
async def display_upload_image(file: UploadFile = File(...)):
    clean(False)
    file_loc = f"{upload_dir}/{file.filename}"
    with open(file_loc, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    image_bmp = file.filename.split(".")[0] + ".bmp"
    ink.convert_24bmp(file_loc, f"{upload_dir}/{image_bmp}")
    ink.display_image(f"uploads/{image_bmp}")
    if DEBUG:
        LOGGER.info("Displaying image from POST: %s", file.filename)
    ink.sleep()

    return JSONResponse(
        content={"filename": file.filename, "message": "File uploaded and displaying"}
    )


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


@app.get("/quote")
async def get_quote():
    clean(False)
    resp: requests.Response = requests.get("https://zenquotes.io/api/today")
    data = resp.json()
    quote = str(data[0]["q"])
    # quote = "Time is too slow for those who wait, too swift for those who fear, too long for those who grieve, too short for those who rejoice, but for those who love, time is eternity."
    LOGGER.info(quote)
    author = "- " + str(data[0]["a"])
    font_size: int = 56
    author_size: int = 44
    quote_font: str = f"./assets/fonts/{font}"
    quote_process: TextBoundary = utils.center_text(quote, quote_font, font_size)
    quote_pos = quote_process.origin_coord
    quote_lines: list[TextBoundaryLine] = quote_process.text_lines
    author_process = utils.center_text(author, quote_font, author_size)
    author = author_process.text_lines[0].text
    author_pos = author_process.origin_coord
    author_pos_offset = Coord(x=author_pos.x + 172, y=author_pos.y + 192)
    LOGGER.info(quote_lines)
    x = quote_pos.x
    y = quote_pos.y
    for line in quote_lines:
        LOGGER.info(f"Setting quote line coords: {x, y}")
        try:
            LOGGER.info(line)
            color = "#000000"
            draw = ink.draw(ink.draw_image)
            ink.draw_text(
                (x, y),
                text=line.text,
                font=font,
                size=quote_process.font_size,
                color=color,
                draw=draw,
            )
            y += quote_process.max_line_height
        except IOError as e:
            print("IO ERROR")
            return LOGGER.error(e)
    try:
        ink.draw_text(
            (author_pos_offset.x, author_pos_offset.y),
            text=author,
            font=font,
            size=author_size,
            color=color,
            draw=draw,
        )

        ink.display_draw(ink.draw_image)
        ink.sleep()

    except IOError as e:
        print("IO ERROR")
        return LOGGER.info(e)
    return "Success"


@app.get("/random_fact")
async def random_fact():
    clean(False)
    resp: requests.Response = requests.get("https://thefact.space/random")
    data = resp.json()
    LOGGER.info(f"/random_fact response: {data}")
    fact = data["text"]
    LOGGER.info(f"Building image for random fact: {fact}")
    fact_source = data["source"]
    qr_source_img = qrcode.make(fact_source).convert("L")
    qr_source_img = qr_source_img.resize((100, 100), Image.Resampling.LANCZOS)
    qr_coord = Coord(x=ink.width - 110, y=ink.height - 110)
    font_size: int = 56  # this is a 'target' size it will be changed if too large
    fact_font: str = f"./assets/fonts/{font}"
    fact_boundary: TextBoundary = utils.center_text(fact, fact_font, font_size)
    fact_origin_coord = fact_boundary.origin_coord
    fact_lines = fact_boundary.text_lines
    for line in fact_lines:
        LOGGER.info(
            f"Setting fact line coords: {fact_origin_coord.x, fact_origin_coord.y}"
        )
        try:
            LOGGER.info(line)
            color = "#000000"
            draw = ink.draw(ink.draw_image)
            ink.draw_text(
                (line.center_x, fact_origin_coord.y),
                text=line.text,
                font=font,
                size=fact_boundary.font_size,
                color=color,
                draw=draw,
            )
            fact_origin_coord.y += fact_boundary.max_line_height
        except IOError as e:
            print("IO ERROR")
            return LOGGER.error(e)
    try:
        canvas = ink.draw_image
        canvas.paste(qr_source_img, (qr_coord.x, qr_coord.y))
        ink.display_draw(ink.draw_image)
        ink.sleep()

    except IOError as e:
        print("IO ERROR")
        return LOGGER.info(e)
    return "Success"


@app.get("/qr-code/wifi")
async def generate_wifi_qr():
    clean(False)
    ssid = (
        subprocess.check_output(
            [
                "iwgetid",
                "-r",
            ]
        )
        .decode("utf-8")
        .strip()
    )
    # This will not work if you let rpi imager populate the psk because it hashes it,
    # however, if you manually enter the psk in the imager it will populate the conf with plaintext.
    get_psk = "sh ./scripts/get_psk.sh"
    psk = (
        subprocess.check_output([cmd for cmd in get_psk.split(" ")])
        .decode("utf-8")
        .strip()
    )
    psk = psk[psk.find("=") + 1 :]
    wifi = f"WIFI:S:{ssid};T:WPA;P:{psk};H:false;;"
    qr = qrcode.make(wifi).convert("L")
    qr = qr.resize(
        (ink.height, ink.height), Image.Resampling.LANCZOS
    )  # contain the qr code using the dimensions of the screen
    # qr.show()
    # qr.save("wifi.png")
    image_width, image_height = qr.size
    image_center = (image_width // 2, image_height // 2)
    offset_origin = (ink.center[0] - image_center[0], ink.center[1] - image_center[1])
    canvas = ink.draw_image
    # print(f"{qr=}")
    # print(f"{image_center=}")
    # print(qr.mode, canvas.mode)
    canvas.paste(qr, offset_origin)
    ink.display_draw(ink.draw_image)
    ink.sleep()


@app.get("/qr-code/ssh")
async def generate_ssh_qr():
    ssh_cmd = "cat /home/daze/.ssh/id_rsa.pub"
    ssh = (
        subprocess.check_output([cmd for cmd in ssh_cmd.split(" ")])
        .decode("utf-8")
        .strip()
    )
    # qr_contents = f"SSH Key:{ssh}"
    generate_qr(ssh)
    ink.sleep()


def generate_qr(contents):
    clean(False)
    qr = qrcode.make(contents).convert("L")
    qr = qr.resize((ink.height, ink.height), Image.Resampling.LANCZOS)
    image_width, image_height = qr.size
    image_center = (image_width // 2, image_height // 2)
    offset_origin = (ink.center[0] - image_center[0], ink.center[1] - image_center[1])
    canvas = ink.draw_image
    canvas.paste(qr, offset_origin)
    ink.display_draw(ink.draw_image)
