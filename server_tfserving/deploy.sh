PROJECT_NAME=$1
docker tag server_tfserving eu.gcr.io/${PROJECT_NAME}/server_python_tfserving
docker push eu.gcr.io/${PROJECT_NAME}/server_tfserving
gcloud run deploy \
  --platform managed \
  --region europe-west1 \
  --image eu.gcr.io/${PROJECT_NAME}/server_tfserving \
  --no-allow-unauthenticated \
  --memory 1Gi \
  server-tfserving