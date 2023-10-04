PROJECT_NAME=$1
docker tag server_python_slow eu.gcr.io/${PROJECT_NAME}/server_python_slow
docker push eu.gcr.io/${PROJECT_NAME}/server_python_slow
gcloud run deploy \
  --platform managed \
  --region europe-west1 \
  --image eu.gcr.io/${PROJECT_NAME}/server_python_slow \
  --no-allow-unauthenticated \
  --memory 1Gi \
  server-python-slow