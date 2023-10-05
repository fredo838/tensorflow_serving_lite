FROM python:3.9-slim
RUN python3 -m pip install pip --upgrade
RUN python3 -m pip install numpy gunicorn tflite_runtime flask pillow
COPY model.tflite /server/model.tflite
COPY server/run.py /server/run.py
WORKDIR /server
ENV PYTHONUNBUFFERED 1
ENTRYPOINT START_TIME=$(date +%s%N) gunicorn --bind 0.0.0.0:$PORT run:app



