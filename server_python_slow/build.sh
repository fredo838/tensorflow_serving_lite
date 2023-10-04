cp -r assets/saved_model/* server_python_slow/saved_model/ && \
cd server_python_slow && \
docker build -t server_python_slow .