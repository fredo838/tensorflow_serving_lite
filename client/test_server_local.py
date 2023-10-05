import requests
import time
from PIL import Image
import io
import numpy as np
import base64


def load_image():
    image = Image.open("small.png").convert('RGB')
    image = image.resize((224, 224))
    image_array = np.expand_dims(np.asarray(image, dtype=np.float32), axis=0)
    return image_array

if __name__ == "__main__":
    # url = "http://localhost:8000"
    url = "http://server:8080"
    image_array = load_image()
    print(image_array.shape)
    payload = {"image_array": image_array.tolist()}
    # print(payload)
    result = requests.post(f"{url}/predict", json=image_array.tolist())
    print(result.status_code)
    if result.status_code != 200:
        print(result.text)