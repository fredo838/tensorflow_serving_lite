cp -r assets/saved_model/* server_python_tensorflow/saved_model/ && \
cd server_python_tensorflow && \
docker build -t server_python_tensorflow .