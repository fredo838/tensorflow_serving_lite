bash server_python_fast/build.sh &&
docker run --env PORT=8080 --cpus 1 --memory 4G --rm -it -p 8080:8080 --name server server_python_fast