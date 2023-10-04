##Introduction

TL;DR: If you serve your Tensorflow model as a Tensorflow Lite model you 
can drastically reduce cold start time when hosting in a Serverless environment.

There's currently three microservices in this repository that serve the same Tensorflow model. There's:
 - `server_python_slow`, which has dependencies `gunicorn`, `flask` and the full `tensorflow` 
 - `server_python_fast`, which has dependencies `gunicorn`, `flask` and `tflite_runtime` aka Tensorflow Lite
 - `server_rust_fastest`, which has depencies `Rocket` and `tflitec`

All microservices and dependencies are built inside `Docker` containers.

The purpose of these microservices is to show you the impact of Docker image size on cold start times
in a serverless environment. In this case, GCP's serverless solution `Google Cloud Run`.

### Steps
1) First we need a `SavedModel`. You can use your own `SavedModel`, but we'll generate one
by running `bash generate/run.sh`. This will run a docker container that saves a `MobileNet` model
to the `saved_model`folder (locally).
2) For `server_python_fast` and  `server_rust_fastest`, which use `Tensorflow Lite` models, we'll need
to convert the `saved_model` into a `model.tflite` under `saved_model_tflite`. We do that by running
`bash convert_to_tflite/run.sh`. 
3) To build each microservice we run `bash server_x_x/build.sh`, e.g. `bash server_python_slow/build.sh`
4a) To run and test the microservice locally, we can run `bash server_x_x/run.sh`, and to call it, 
in a new terminal, run `bash run_client_local.sh`. This won't show 
4b) To run and test in 







