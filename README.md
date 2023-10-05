## TL;DR 

If you serve your Tensorflow model as a Tensorflow Lite model you 
can drastically reduce cold start time when hosting in a Serverless environment.

## Rationale

There's currently three microservices in this repository that serve the same Tensorflow model. There's:
 - `server_python_slow`, written in `python`, with dependencies `gunicorn`, `flask` and the full `tensorflow` 
 - `server_python_fast`, written in `python`, with dependencies `gunicorn`, `flask` and `tflite_runtime`
 - `server_rust_fastest`, written in `Rust`, with depencies `Rocket` and `tflitec`

which all serve a `MobileNet`, which is `~ 19 Mb` in size - aka a small model. We deploy each
of them to `GCP`'s `Cloud Run`, their Serverless environment. If we now call each in a  a "Cold Start" setting,
which means the microservice is not ready to serve traffic in the Serverless environment and needs to be "spun up"
before it's able to receive a request, we see that the different microservices take a different amount of time:
```
Call to server_python_slow  took 47034.02 ms
Call to server_python_fast  took 4222.86 ms (11 times faster than server_python_slow)
Call to server_rust_fastest took 1397.38 ms (35 times faster than server_python_slow)
```
Calling each of these microservices *not* from a "Cold Start", aka `Cloud Run` instance is 
still running, then a call to _each_ of these microservicestakes about `~300 ms`.

*Conclusion*: If we want to deploy our `Tensorflow` model in a Serverless environment, we can 
increase the responsiveness of the model by exploiting `Tensorflow Lite`. The smaller the model, 
the bigger the relative gain, but always a gain - nothing to lose - unless the model uses 
operations not supported by `Tensorflow Lite`, which is still almost all operations.

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







