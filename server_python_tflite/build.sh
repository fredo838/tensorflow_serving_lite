cp -r assets/saved_model_tflite/model.tflite server_python_tflite/model.tflite && \
cd server_python_tflite && \
docker build -t server_python_tflite .