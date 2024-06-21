from cairosvg import svg2png
import os

CWD = os.getcwd()

with open(CWD + "/light/Air.svg", "rb") as f:
    svg_code = f.read()

svg2png(bytestring=svg_code, write_to='test.png')
