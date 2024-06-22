from PIL import Image
import os, sys

CWD = os.getcwd()
ARG = sys.argv[1]
if ARG == ".":
    ARG = CWD
PATH = CWD + "/" + ARG
IMGS = os.listdir(PATH)

for img in IMGS:
    img_r = Image.open(PATH + img)
    img_r.resize((150, 150)).save(PATH + img)
