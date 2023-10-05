## TL;DR 

If you serve your Tensorflow model as a Tensorflow Lite model you 
can drastically reduce cold start time when hosting in a Serverless environment.

## Rationale

There's currently three microservices in this repository that serve the same Tensorflow model. There's:
 - `server_python_slow`, written in `python`, with dependencies `gunicorn`, `flask` and the full `tensorflow` 
 - `server_python_fast`, written in `python`, with dependencies `gunicorn`, `flask` and `tflite_runtime`
 - `server_rust_fastest`, written in `Rust`, with depencies `Rocket` and `tflitec`

which all serve a `MobileNet`. If we deploy them to `GCP`'s `Cloud Run`,
we see that a request to each of them takes a different amount of time to complete if we 
are calling them from a "Cold Start", aka the microservice has not been called for >15 minutes:
```
Call to server_python_slow  took 47034.02 ms
Call to server_rust_fastest took 1397.38 ms
Call to server_python_fast  took 4222.86 ms
```
Which in short means:
 - Serving a model in `python` which `import`s the full `tensorflow` library takes `~ 47 seconds` on cold start.
 - Serving a model in `python` which `import`s the `tflite_runtime` library takes `~ 4.2 seconds` on cold start.
 - Serving a model in `rust` which `use`s the `tflitec` crate takes `~ 1.4 seconds` on cold start.
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







