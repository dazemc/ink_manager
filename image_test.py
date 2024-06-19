import requests
import os

cwd = os.getcwd()
image = cwd + "/assets/images/weather_icons/raining_test.png"

with open(image, "rb") as f:
    img_data = f.read()

files = {"image": ("raining_test.png", img_data)}
test_url = "http://192.168.0.213/test_image"
r = requests.post(test_url, files=files)
