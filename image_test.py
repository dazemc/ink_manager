import requests
import os

cwd = os.getcwd()
image = cwd + "/assets/images/raspilogo.bmp"

with open(image, "rb") as f:
    img_data = f.read()

files = {"image": ("raspilogo.bmp", img_data)}
test_url = "http://192.168.0.213/test_image"
r = requests.post(test_url, files=files)
