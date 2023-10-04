FROM python
RUN python3 -m pip install tensorflow
RUN mkdir /app
WORKDIR /app
COPY convert.py /app/convert.py
ENTRYPOINT python3 convert.py