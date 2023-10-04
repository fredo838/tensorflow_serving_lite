import requests
import time
import sys

def print_speed(name, duration, status_code):
    print(f"Call to {name.ljust(30)} took {1000 * duration:.2f} ms, code {status_code}")

if __name__ == "__main__":
    server_python_slow = "https://server-python-slow-y22xrxockq-ew.a.run.app"
    server_python_fast = "https://server-python-fast-y22xrxockq-ew.a.run.app"
    server_rust_fastest = "https://server-rust-fastest-y22xrxockq-ew.a.run.app"
    
    with open("image_string.txt") as f:
        image_string = f.read().strip("\n")

    headers = {
        "Authorization": f"Bearer {sys.argv[-1]}"
    }

    kwargs = {"json":{"base64_image": image_string}, "headers":headers}

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


