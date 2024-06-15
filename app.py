# import subprocess
# import json
# import time
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


@app.route("/", methods=["GET"])
def test() -> None:
    try:
        # INIT/CLEAR
        ink.init()
        ink.clear()

        # DISPLAY IMAGE
        ink.display_image(image)
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
        ink.clear()

        # SLEEP
        ink.sleep()

    except IOError as e:
        logging.info(e)


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
