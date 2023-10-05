bash server_python_slow/build.sh && 
docker run --env PORT=8080 --rm -it -p 8080:8080 --name server server_python_slow