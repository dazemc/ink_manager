"""SVG to PNG conversion"""

import os
import sys
from cairosvg import svg2png


CWD = os.getcwd()
ARG = sys.argv[1]
if ARG == ".":
    ARG = CWD
SVG_PATH = CWD + "/" + ARG
SVG = os.listdir(SVG_PATH)

for img in SVG:
    with open(SVG_PATH + img, "rb") as f:
        svg_code = f.read()
    svg2png(bytestring=svg_code, write_to=SVG_PATH + img.split(".")[0] + ".png")
