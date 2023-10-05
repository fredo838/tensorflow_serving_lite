# This script saves libtensorflowlite_c.so on the host system so it can be used by rust-analyzer
bash server_rust_fastest/run.sh &
sleep 2
docker cp server:/usr/lib/libtensorflowlite_c.so libtensorflowlite_c.so
docker kill server