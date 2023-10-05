cp assets/saved_model_tflite/model.tflite server_rust_tflite/model.tflite && \
cd server_rust_tflite && \
docker build -t server_rust_tflite .