## TL;DR 

If you serve your Tensorflow model as a Tensorflow Lite model you 
can drastically reduce cold start time when hosting in a Serverless environment. This repository
proves by how much - and it's more than you would think.

## Rationale

There's currently three microservices in this repository that serve the same Tensorflow model. There's:
 - `server_python_slow`, written in `python`, with dependencies `gunicorn`, `flask` and the full `tensorflow` 
 - `server_python_fast`, written in `python`, with dependencies `gunicorn`, `flask` and `tflite_runtime`
 - `server_rust_fastest`, written in `Rust`, with depencies `Rocket` and `tflitec`

which all serve a `MobileNet`, which is `~ 19 Mb` in size - aka a small model. We deploy each
of them to `GCP`'s `Cloud Run`, their Serverless environment. If we now call each in a "Cold Start" setting,
which means the microservice needs to be "spun up"
before it's able to receive a request, we see that the different microservices take a different amount of time to
process that first request:
```
Call to server_python_slow  took 47034.02 ms (Docker image size = 3.29 GB)
Call to server_python_fast  took 4222.86 ms (11 times faster than server_python_slow, Docker image size = 282 MB)
Call to server_rust_fastest took 1397.38 ms (35 times faster than server_python_slow, Docker image size = 59 MB)
```
Calling one of these microservices *not* from a "Cold Start", aka the `Cloud Run` instance is 
still running, will take about `~300 ms`, _no matter which one_.


## Serving your own model with Tensorflow Lite
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







