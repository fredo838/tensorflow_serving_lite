cd client && \
docker build -t client_local -f Dockerfile-local . && \
docker run -it --rm --name client_local client_local