bash server_rust_tflite/build.sh && 
docker run --env=PORT=8080 --cpus 1 --memory 1G --rm --name server -p 8080:8080 -t server_rust_tflite