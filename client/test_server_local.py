import requests
import time

if __name__ == "__main__":
    # url = "http://localhost:8000"
    url = "http://server:8080"
    with open("image_string.txt") as f:
        image_string = f.read().strip("\n")
    result = requests.post(f"{url}/predict", json={"base64_image": image_string})
    print(result.status_code)
    if result.status_code != 200:
        print(result.text)