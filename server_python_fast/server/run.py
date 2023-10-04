import time
from flask import Flask, request
import tflite_runtime.interpreter as tflite
from PIL import Image
import os
import io
import base64
import numpy as np

app = Flask(__name__)
ready_time = time.time()



def load_model_in_interpreter():
    interpreter = tflite.Interpreter('model.tflite')
    interpreter.allocate_tensors()
    return interpreter

def call_interpreter(interpreter, input_data):
    interpreter.set_tensor(interpreter.get_input_details()[0]['index'], input_data)
    interpreter.allocate_tensors()
    t1 = time.time()
    interpreter.invoke()
    
    t2 = time.time()
    print(f"** Invoke took {t2 - t1}")
    output_data = interpreter.get_tensor(interpreter.get_output_details()[0]['index'])[0]
    data_as_list = output_data.tolist()
    return data_as_list
    return "test"

def decode_image(input_data):
    base64_decoded = base64.b64decode(input_data)
    image = Image.open(io.BytesIO(base64_decoded)).convert('RGB')
    image = image.resize((224, 224))
    image_array = np.expand_dims(np.asarray(image, dtype=np.float32), axis=0)
    return image_array

start_time = time.time()
interpreter = load_model_in_interpreter()
print(time.time() - start_time)
print(f"**** Loading model took {(time.time() - start_time) * 1000} ms")
env_start_time = float(os.environ['START_TIME']) / 1000000000
print(f"**** Booted in {(time.time() - env_start_time) * 1000} ms")


@app.route('/predict', methods=['POST'])
def hello():
    input_data = decode_image(request.json['base64_image'])
    global interpreter
    start_time = time.time()
    data_as_list = call_interpreter(interpreter, input_data)
    # The first request will be slower, as per documentation:
    # https://www.tensorflow.org/tfx/serving/saved_model_warmup#usage
    print(f"**** Inference took {(time.time() - start_time) * 1000} ms")
    return data_as_list