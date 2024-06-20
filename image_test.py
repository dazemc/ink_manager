import requests
import os

cwd = os.getcwd()
image_name = "forecast.png"
image = cwd + f"/assets/images/test/{image_name}"
test_url = "http://192.168.0.213/test_image"

with open(image, "rb") as f:
    img_data = f.read()

files = {"image": (image_name, img_data)}
r = requests.post(test_url, files=files)
