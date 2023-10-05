PROJECT_NAME=$1
docker tag server_python_tensorflow eu.gcr.io/${PROJECT_NAME}/server_python_tensorflow
docker push eu.gcr.io/${PROJECT_NAME}/server_python_tensorflow
gcloud run deploy \
  --platform managed \
  --region europe-west1 \
  --image eu.gcr.io/${PROJECT_NAME}/server_python_tensorflow \
  --no-allow-unauthenticated \
  --memory 1Gi \
  server-python-tensorflow