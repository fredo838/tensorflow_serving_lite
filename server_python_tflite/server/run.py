import os
import time
from flask import Flask, request
import tflite_runtime.interpreter as tflite
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
    interpreter.invoke()
    output_data = interpreter.get_tensor(interpreter.get_output_details()[0]['index'])[0]
    data_as_list = output_data.tolist()
    return data_as_list

start_time = time.time()
interpreter = load_model_in_interpreter()
print(time.time() - start_time)
print(f"**** Loading model took {(time.time() - start_time) * 1000} ms")
env_start_time = float(os.environ['START_TIME']) / 1000000000
print(f"**** Booted in {(time.time() - env_start_time) * 1000} ms")


@app.route('/predict', methods=['POST'])
def hello():
    image_array = np.asarray(request.json, dtype=np.float32)
    start_time = time.time()
    data_as_list = call_interpreter(interpreter, image_array)
    # The first request will be slower, as per documentation:
    # https://www.tensorflow.org/tfx/serving/saved_model_warmup#usage
    print(f"**** Inference took {(time.time() - start_time) * 1000} ms")
    return data_as_list