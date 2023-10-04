import os
import tensorflow as tf

if __name__ == "__main__":
    # cleanup assets/saved_model_tflite if there's anything in it already
    paths = os.listdir("assets/saved_model_tflite")
    for name in paths:
        path = os.path.join("assets/saved_model_tflite", name)
        if not name.startswith("."):
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)

    # Convert the SavedModel to TFLite
    converter = tf.lite.TFLiteConverter.from_saved_model("assets/saved_model")
    tflite_model = converter.convert()

    # Save the TFLite model to a file
    with open("assets/saved_model_tflite/model.tflite", 'wb') as f:
        f.write(tflite_model)
            