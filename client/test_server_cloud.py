import requests
import time
import sys
from PIL import Image
import numpy as np
import io

def load_image():
    image = Image.open("small.png").convert('RGB')
    image = image.resize((224, 224))
    image_array = np.expand_dims(np.asarray(image, dtype=np.float32), axis=0)
    return image_array

def print_speed(name, duration, status_code):
    print(f"Call to {name.ljust(30)} took {1000 * duration:.2f} ms, code {status_code}")

if __name__ == "__main__":
    server_python_slow = "https://server-python-slow-y22xrxockq-ew.a.run.app"
    server_python_fast = "https://server-python-fast-y22xrxockq-ew.a.run.app"
    server_rust_fastest = "https://server-rust-fastest-y22xrxockq-ew.a.run.app"

    headers = {"Authorization": f"Bearer {sys.argv[-1]}"}
    kwargs = {"json":{"image_array": load_image()}, "headers":headers}

    start_time = time.time()
    result = requests.post(f"{server_python_slow}/predict", **kwargs)
    end_time = time.time()
    print_speed("server_python_slow", end_time - start_time, result.status_code)

    start_time = time.time()
    result = requests.post(f"{server_rust_fastest}/predict", **kwargs)
    end_time = time.time()
    print_speed("server_rust_fastest", end_time - start_time, result.status_code)
    
    start_time = time.time()
    result = requests.post(f"{server_python_fast}/predict", **kwargs)
    end_time = time.time()
    print_speed("server_python_fast", end_time - start_time, result.status_code)


