import requests
from enum import Enum
from datetime import datetime
import os
import base64

with open("./.API_KEY.txt", 'r') as f:
    API_KEY = f.read().strip()
with open("./prompt.txt", 'r', encoding='utf-8') as f:
    prompt = f.read()


class AspectRatio(Enum):
    aspect_ratio_11 = "1:1"
    ar_16_9 = "16:9"
    ar_21_9 = "21:9"
    ar_2_3 = "2:3"
    ar_3_2 = "3:2"
    ar_3_4 = "3:4"
    ar_4_3 = "4:3"
    ar_4_5 = "4:5"
    ar_5_4 = "5:4"
    ar_9_16 = "9:16"


class ImageSize(Enum):
    is_1k = "1K"
    is_2k = "2K"
    is_4k = "4K"


with open("./input_image/leilei.JPG", "rb") as img_file:
    input_img = base64.b64encode(img_file.read()).decode("utf-8")


def save_image(data):
    os.makedirs("./result", exist_ok=True)
    if data.get("data"):
        img_url = data["data"][0].get("url")
        if img_url:
            ts = datetime.now().strftime("%y%m%d_%H-%M-%S")
            filename = f"./result/{ts}.png"

            img = requests.get(img_url)
            img.raise_for_status()

            with open(filename, "wb") as f:
                f.write(img.content)
        else:
            print("No image url found.")
            print(f"data: {data}")
    else:
        print("No image data returned.")
        print(f"data: {data}")


payload = {
    "prompt": f"{prompt}",
    "model": "nano-banana-2-4k",
    "response_format": "url",
    "aspect_ratio": AspectRatio.ar_4_3.value,
    "image_size": ImageSize.is_4k.value,
    "image": [input_img]
}

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

url = "https://api.gptbest.vip/v1/images/generations"

response = requests.request("POST", url, headers=headers, json=payload)

response.raise_for_status()
save_image(response.json())
