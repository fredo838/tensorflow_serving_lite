PROJECT_NAME=$1
docker tag server_python_fast eu.gcr.io/${PROJECT_NAME}/server_python_fast
docker push eu.gcr.io/${PROJECT_NAME}/server_python_fast
gcloud run deploy \
  --platform managed \
  --region europe-west1 \
  --image eu.gcr.io/colab-keep-alive/server_python_fast \
  --no-allow-unauthenticated \
  --memory 1G \
  server-python-fast