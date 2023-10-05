cp -r assets/saved_model/* server_tfserving/saved_model/ && \
cd server_tfserving && \
docker build -t server_tfserving .