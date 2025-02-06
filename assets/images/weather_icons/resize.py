"""Resize images"""

import os
import sys
from PIL import Image

CWD = os.getcwd()
ARG = sys.argv[1]
WIDTH = sys.argv[2]
HEIGHT = sys.argv[3]

if ARG == ".":
    ARG = CWD
PATH = CWD + "/" + ARG
IMGS = os.listdir(PATH)

for img in IMGS:
    img_r = Image.open(PATH + img)
    img_r.resize((WIDTH, HEIGHT)).save(PATH + img)
