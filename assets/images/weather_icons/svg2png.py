from cairosvg import svg2png
import os

CWD = os.getcwd()
SVG_PATH = CWD + "/light"
SVG = os.listdir(SVG_PATH)

for icon in SVG:
    with open(SVG_PATH + icon, "rb") as f:
        svg_code = f.read()
    svg2png(bytestring=svg_code, write_to=SVG_PATH + icon.split('.')[0] + ".png")
