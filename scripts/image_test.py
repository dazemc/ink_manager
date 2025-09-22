#!/usr/bin/env python

import requests
import os

cwd = os.getcwd()
image = cwd + "/../assets/images/test/raspilogo.bmp"
test_url = "http://0.0.0.0:8000/upload_image"

with open(image, "rb") as f:
    img_data = f.read()

files = {"image": (image, img_data)}
r = requests.post(test_url, files=files)
