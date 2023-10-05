bash server_rust_fastest/build.sh && 
docker run --env=PORT=8080 --cpus 1 --memory 2G --rm --name server -p 8080:8080 -t server_rust_fastest