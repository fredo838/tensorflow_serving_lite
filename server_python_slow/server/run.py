import time
from flask import Flask, request
import tensorflow as tf
import os
from PIL import Image
import numpy as np
import io
import base64

app = Flask(__name__)


def load_model():
    model = tf.keras.models.load_model("saved_model")
    return model

start_time = time.time()
model = load_model()
print(f"**** Loading model took {(time.time() - start_time) * 1000} ms")
env_start_time = float(os.environ['START_TIME']) / 1000000000
print(f"**** Booted in {(time.time() - env_start_time) * 1000} ms")

def decode_image(input_data):
    base64_decoded = base64.b64decode(input_data)
    image = Image.open(io.BytesIO(base64_decoded)).convert('RGB')
    image = image.resize((224, 224))
    image_array = np.expand_dims(np.asarray(image, dtype=np.float32), axis=0)
    return image_array

@app.route('/predict', methods=['POST'])
def hello():
    decoded_image = decode_image(request.json['base64_image'])
    start_time = time.time()
    # The first request will be slower, as per documentation:
    # https://www.tensorflow.org/tfx/serving/saved_model_warmup#usage    
    output = model(decoded_image)
    print(f"**** Inference took {(time.time() - start_time) * 1000} ms")
    return output.numpy().tolist()