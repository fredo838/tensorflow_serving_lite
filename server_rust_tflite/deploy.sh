PROJECT_NAME=$1
docker tag server_rust_fastest eu.gcr.io/${PROJECT_NAME}/server_rust_fastest
docker push eu.gcr.io/${PROJECT_NAME}/server_rust_fastest
gcloud run deploy \
  --platform managed \
  --region europe-west1 \
  --memory 1G \
  --image eu.gcr.io/${PROJECT_NAME}/server_rust_fastest \
  --no-allow-unauthenticated \
  server-rust-fastest 