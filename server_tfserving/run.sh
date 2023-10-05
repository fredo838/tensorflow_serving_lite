bash server_tfserving/build.sh && 
docker run --env PORT=8080 --rm -it --name server server_tfserving