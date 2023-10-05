cp -r assets/saved_model_tflite/model.tflite server_python_fast/model.tflite && \
cd server_python_fast && \
docker build -t server_python_fast .