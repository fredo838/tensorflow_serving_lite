cd convert_to_tflite && \
docker build -t convert_to_tflite . && \
docker run \
  --mount type=bind,source=$(pwd)/../assets,target=/app/assets \
  convert_to_tflite