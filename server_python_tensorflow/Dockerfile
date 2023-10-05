FROM python:3
RUN python3 -m pip install numpy gunicorn tensorflow flask pillow
COPY server/run.py /server/run.py
COPY saved_model /server/saved_model
WORKDIR /server
ENV PYTHONUNBUFFERED 1
ENTRYPOINT START_TIME=$(date +%s%N) gunicorn --bind 0.0.0.0:$PORT run:app



