cp -r assets/saved_model/* server_python_slow/saved_model/ && \
cd server_tfserving && \
docker build -t server_tfserving .