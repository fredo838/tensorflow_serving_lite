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
    server_python_tensorflow = "https://server-python-tensorflow-y22xrxockq-ew.a.run.app/predict"
    server_python_tflite = "https://server-python-tflite-y22xrxockq-ew.a.run.app/predict"
    server_rust_tflite = "https://server-rust-tflite-y22xrxockq-ew.a.run.app/predict"
    server_tfserving = "https://server-tfserving-y22xrxockq-ew.a.run.app/v1/models/model:predict"

    headers = {"Authorization": f"Bearer {sys.argv[-1]}"}
    kwargs = {"json":{"image_array": load_image()}, "headers":headers}
    kwargs_tfserving = {"json":{"instances": load_image()}, "headers":headers}

    start_time = time.time()
    result = requests.post(server_python_tensorflow, **kwargs)
    end_time = time.time()
    print_speed("server_python_tensorflow", end_time - start_time, result.status_code)

    start_time = time.time()
    result = requests.post(server_tfserving, **kwargs_tfserving)
    end_time = time.time()
    print_speed("server_tfserving", end_time - start_time, result.status_code)
    
    start_time = time.time()
    result = requests.post(server_python_tflite, **kwargs)
    end_time = time.time()
    print_speed("server_python_tflite", end_time - start_time, result.status_code)

    start_time = time.time()
    result = requests.post(server_rust_tflite, **kwargs)
    end_time = time.time()
    print_speed("server_rust_tflite", end_time - start_time, result.status_code)


