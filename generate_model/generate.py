import os
import tensorflow as tf
import shutil
import sys
import numpy as np

if __name__ == "__main__":
    paths = os.listdir("saved_model")
    for name in paths:
        path = os.path.join("saved_model", name)
        if not name.startswith("."):
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
    
    model = tf.keras.applications.mobilenet.MobileNet()
    model(np.zeros(shape=(1, 224, 224, 3), dtype=np.float32))
    model.save("saved_model")
