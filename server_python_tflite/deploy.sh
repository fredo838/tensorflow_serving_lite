PROJECT_NAME=$1
bash server_python_tflite/build.sh && \
docker tag server_python_fast eu.gcr.io/${PROJECT_NAME}/server_python_tflite && \
docker push eu.gcr.io/${PROJECT_NAME}/server_python_tflite && \
gcloud run deploy \
  --platform managed \
  --region europe-west1 \
  --image eu.gcr.io/colab-keep-alive/server_python_tflite \
  --no-allow-unauthenticated \
  --memory 1G \
  server-python-tflite