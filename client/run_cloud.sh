cd client && \
docker build -t client_cloud -f Dockerfile-cloud . && \
docker run -it --rm --name client_cloud client_cloud $(gcloud auth print-identity-token)