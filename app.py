import time
import os
from flask import Flask, request
from flask_cors import CORS
import ink_display as ink
import logging
from PIL import Image

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.DEBUG)
ink = ink.InkDisplay()
cwd = os.getcwd()
image = "zelda00.bmp"
font = "Font.ttc"

DEBUG = True


@app.route("/test", methods=["GET"])
def test() -> str:
    try:
        # INIT/CLEAR
        ink.init()
        ink.clear()

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
        logging.info("drawing draw image")
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
        ink.sleep()
        reset()

    except IOError as e:
        logging.info(e)
    return "Success"


@app.route("/text", methods=["GET"])
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
            logging.info("Displaying text: %s", text)
            logging.info("Displaying color: %s", color)
            logging.info("Displaying position: %s", pos)
            logging.info("Displaying size: %s", size)
            logging.info("Displaying center: %s", center)
        # draw_image = ink.blank_image()
        draw = ink.draw(ink.draw_image)
        ink.draw_text(pos, text=text, font=font, size=size, color=color, draw=draw)
        # ink.display_draw(ink.draw_image)
    except IOError as e:
        return logging.info(e)
    return "Success"


@app.route("/display", methods=["GET"])
def display() -> str:
    ink.init()
    ink.display_draw(ink.draw_image)
    ink.sleep()
    return "Success"


@app.route("/reset", methods=["GET"])
def reset() -> str:
    ink.draw_image = ink.blank_image()
    return "Success"


@app.route("/test_image", methods=["GET", "POST"])
def display_image() -> str:
    ink.init()
    if request.method == "GET":
        if DEBUG:
            logging.info("Displaying image: %s", image)
    if request.method == "POST":
        img_name = request.form["image"][0]
        logging.info("POST image name: %s", img_name)
        r = request.files["image"]
        image = Image.open(r)
        image.save(f"{cwd}/tmp/{img_name}")
        if DEBUG:
            logging.info("Displaying image from POST")
    ink.display_image(image)
    ink.sleep()

    return "Success"


@app.route("/clear", methods=["GET"])
def clear() -> str:
    ink.init()
    ink.clear()
    ink.sleep()
    return "Success"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
