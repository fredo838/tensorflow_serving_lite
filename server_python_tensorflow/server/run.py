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

@app.route('/predict', methods=['POST'])
def hello():
    image = request.json
    image = np.asarray(image)
    start_time = time.time()
    # The first request will be slower, as per documentation:
    # https://www.tensorflow.org/tfx/serving/saved_model_warmup#usage    
    output = model(image)
    print(f"**** Inference took {(time.time() - start_time) * 1000} ms")
    return output.numpy().tolist()