FROM python:alpine

LABEL Name=BuscaLibrePersigueDescuentosServerBot Version=0.0.1

WORKDIR /app

ADD . /app

RUN python3 -m pip install -r requirements.txt

CMD python3 /app/server.py
