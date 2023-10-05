cp assets/saved_model_tflite/model.tflite server_rust_fastest/model.tflite && \
cd server_rust_fastest && \
docker build -t server_rust_fastest .