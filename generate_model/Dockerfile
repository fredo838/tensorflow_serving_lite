FROM python
RUN python3 -m pip install tensorflow
RUN python3 -m pip install transformers
RUN mkdir /app /app/saved_model
WORKDIR /app
COPY generate.py /app/generate.py
ENTRYPOINT [ "python3", "generate.py" ]