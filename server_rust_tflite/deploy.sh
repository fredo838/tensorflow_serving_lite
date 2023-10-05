PROJECT_NAME=$1
docker tag server_rust_tflite eu.gcr.io/${PROJECT_NAME}/server_rust_tflite
docker push eu.gcr.io/${PROJECT_NAME}/server_rust_tflite
gcloud run deploy \
  --platform managed \
  --region europe-west1 \
  --memory 1G \
  --image eu.gcr.io/${PROJECT_NAME}/server_rust_tflite \
  --no-allow-unauthenticated \
  server-rust-tflite