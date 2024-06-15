# import subprocess
# import json
import time
from flask import Flask, request
from flask_cors import CORS
import ink_display as ink
import logging

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.DEBUG)
ink = ink.InkDisplay()
image = "zelda00.bmp"
font = "Font.ttc"

ink.init()


@app.route("/test", methods=["GET"])
def test() -> str:
    try:
        # INIT/CLEAR
        # ink.init()
        ink.clear()

        # DISPLAY IMAGE
        ink.display_image(image)
        time.sleep(5)
        ink.clear()

        # CREATE DRAW
        draw_image = ink.blank_image()
        draw = ink.draw(draw_image)
        ink.draw_text(
            (5, 0), text="hello", font=font, size=24, color="#FF0000", draw=draw
        )
        ink.draw_text(
            (5, 30), text="world", font=font, size=16, color="#FF0000", draw=draw
        )
        logging.info("drawing draw image")
        draw.line([(5, 170), (80, 245)], fill="#0000FF")
        ink.display_draw(draw_image)
        time.sleep(5)
        ink.clear()

        # CREATE NEW DRAW
        draw_image = ink.blank_image()
        draw = ink.draw(draw_image)
        ink.draw_text(
            (5, 0),
            text="goodbye world",
            font=font,
            size=36,
            color="#00FF00",
            draw=draw,
        )
        ink.display_draw(draw_image)
        time.sleep(5)
        ink.clear()

        # SLEEP
        ink.sleep()

    except IOError as e:
        logging.info(e)
    return "Success"


@app.route("/", methods=["GET"])
def display_text() -> str:
    try:
        text = str(request.args["text"])
        color = "#" + str(request.args["color"])
        pos = tuple([int(i) for i in str(request.args["pos"]).split(",")])
        size = int(request.args["size"])
        logging.info("Displaying text: %s", text)
        logging.info("Displaying color: %s", color)
        logging.info("Displaying position: %s", pos)
        logging.info("Displaying size: %s", pos)
        draw_image = ink.blank_image()
        draw = ink.draw(draw_image)
        ink.draw_text(pos, text=text, font=font, size=size, color=color, draw=draw)
        ink.display_draw(draw_image)
    except IOError as e:
        return logging.info(e)
    return "Success"


@app.route("/clear", methods=["GET"])
def clear() -> str:
    ink.clear()
    return "Success"


# @app.route("/send_creds", methods=["POST"])
# def save_credentials() -> str:
#     if request.method == "POST":
#         r = json.loads(request.data)
#         time.sleep(3)
#         if connect_wifi(r["SSID"], r["PASS"]):
#             if DEBUG_HOTSPOT:
#                 enable_hotspot()
#             # will not be able to return because wifi connection gets lost, will send it with credentials instead
#             # return {"local_ip": get_local_ip()}
#             return "Connected"
#         return "Error connecting"
#     return "Not a POST method"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
