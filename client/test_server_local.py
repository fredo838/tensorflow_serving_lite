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
    base_url = "http://server:8080"
    image_array = load_image()

    url = f"{base_url}/predict"
    payload = image_array.tolist()
    start_time = time.time()
    # for tfserving
    # payload = {"instances": image_array.tolist()}
    # url = f"{base_url}/v1/models/model:predict"

    result = requests.post(f"{url}", json=payload)
    print(f"$$$$ Inference took {1000 * (time.time() - start_time)} ms, status {result.status_code}")
    if result.status_code != 200:
        print(result.text)

